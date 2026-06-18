import json
import os
import urllib.error
import urllib.request
from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Avg, Count, Max, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Attendance, Department, Employee, LeaveRequest, Payroll
from .serializers import (
    AttendanceSerializer,
    DepartmentSerializer,
    EmployeeSerializer,
    LeaveRequestSerializer,
    PayrollSerializer,
)


def home(request):
    return render(request, "index.html")


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.select_related("manager", "department_ref")
        search = self.request.query_params.get("search")
        department = self.request.query_params.get("department")
        employee_status = self.request.query_params.get("status")
        location = self.request.query_params.get("location")
        ordering = self.request.query_params.get("ordering", "employee_id")
        allowed_ordering = {"full_name", "-full_name", "salary", "-salary", "date_of_joining", "-date_of_joining"}
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
                | Q(employee_id__icontains=search)
                | Q(email__icontains=search)
                | Q(designation__icontains=search)
            )
        if department:
            queryset = queryset.filter(department=department)
        if employee_status:
            queryset = queryset.filter(status=employee_status)
        if location:
            queryset = queryset.filter(location=location)
        return queryset.order_by(ordering if ordering in allowed_ordering else "employee_id")


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.annotate(
            employee_count=Count("employees"),
            average_salary=Avg("employees__salary"),
            highest_salary=Max("employees__salary"),
        )


class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.select_related("employee")
        for param, field in (("date", "date"), ("status", "status"), ("employee", "employee_id")):
            value = self.request.query_params.get(param)
            if value:
                queryset = queryset.filter(**{field: value})
        return queryset


class LeaveRequestViewSet(ModelViewSet):
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        queryset = LeaveRequest.objects.select_related("employee", "approver")
        leave_status = self.request.query_params.get("status")
        if leave_status:
            queryset = queryset.filter(status=leave_status)
        return queryset


class PayrollViewSet(ModelViewSet):
    serializer_class = PayrollSerializer

    def get_queryset(self):
        queryset = Payroll.objects.select_related("employee")
        month = self.request.query_params.get("month")
        if month:
            queryset = queryset.filter(month__startswith=month)
        return queryset


def _money(value):
    return float(value or Decimal("0"))


def _second_highest_by_department():
    rows = []
    for department in Department.objects.all():
        salaries = list(
            Employee.objects.filter(department=department.name, status__in=["Active", "On Leave"])
            .values_list("salary", flat=True)
            .distinct()
            .order_by("-salary")
        )
        if len(salaries) >= 2:
            for employee in Employee.objects.filter(department=department.name, salary=salaries[1]):
                rows.append(
                    {
                        "department": department.name,
                        "employee": employee.full_name,
                        "employee_id": employee.employee_id,
                        "salary": _money(employee.salary),
                    }
                )
    return rows


def _absent_more_than_five():
    today = date.today()
    return list(
        Employee.objects.filter(
            attendance__date__year=today.year,
            attendance__date__month=today.month,
            attendance__status="Absent",
        )
        .annotate(absence_count=Count("attendance"))
        .filter(absence_count__gt=5)
        .values("employee_id", "full_name", "department", "absence_count")
    )


@api_view(["GET"])
def dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)
    month_end = today.replace(day=monthrange(today.year, today.month)[1])
    employees = Employee.objects.all()
    current_payroll = Payroll.objects.filter(month__year=today.year, month__month=today.month)

    department_headcount = list(
        employees.exclude(status="Resigned")
        .values("department")
        .annotate(value=Count("id"))
        .order_by("-value")
    )
    leave_distribution = list(
        LeaveRequest.objects.values(name=models_f("leave_type")).annotate(value=Count("id")).order_by("-value")
    )
    attendance_trend = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        records = Attendance.objects.filter(date=day)
        attendance_trend.append(
            {
                "date": day.strftime("%a"),
                "present": records.filter(status__in=["Present", "Work From Home"]).count(),
                "absent": records.filter(status="Absent").count(),
            }
        )
    hiring_trend = list(
        employees.filter(date_of_joining__gte=today - timedelta(days=365))
        .annotate(month=TruncMonth("date_of_joining"))
        .values("month")
        .annotate(value=Count("id"))
        .order_by("month")
    )
    salary_by_department = list(
        employees.exclude(status="Resigned")
        .values("department")
        .annotate(value=Avg("salary"))
        .order_by("-value")
    )
    for item in hiring_trend:
        item["month"] = item["month"].strftime("%b")
    for collection in (salary_by_department,):
        for item in collection:
            item["value"] = _money(item["value"])

    return Response(
        {
            "metrics": {
                "total_employees": employees.count(),
                "active_employees": employees.filter(status="Active").count(),
                "on_leave_today": LeaveRequest.objects.filter(
                    status="Approved", from_date__lte=today, to_date__gte=today
                ).count(),
                "monthly_absences": Attendance.objects.filter(
                    date__range=(month_start, month_end), status="Absent"
                ).count(),
                "payroll_total": _money(current_payroll.aggregate(total=Sum("net_salary"))["total"]),
                "average_salary": _money(
                    employees.exclude(status="Resigned").aggregate(value=Avg("salary"))["value"]
                ),
                "department_count": Department.objects.count(),
                "new_joiners": employees.filter(
                    date_of_joining__range=(month_start, month_end)
                ).count(),
                "attrition_count": employees.filter(status="Resigned").count(),
            },
            "department_headcount": department_headcount,
            "attendance_trend": attendance_trend,
            "leave_distribution": leave_distribution,
            "salary_by_department": salary_by_department,
            "hiring_trend": hiring_trend,
            "recent_employees": EmployeeSerializer(
                employees.order_by("-date_of_joining")[:5], many=True
            ).data,
        }
    )


def models_f(field_name):
    from django.db.models import F

    return F(field_name)


@api_view(["GET"])
def reports(request):
    today = date.today()
    month_start = today.replace(day=1)
    current_payroll = Payroll.objects.filter(month__year=today.year, month__month=today.month)
    department_headcount = list(
        Employee.objects.exclude(status="Resigned")
        .values("department")
        .annotate(employee_count=Count("id"))
        .order_by("-employee_count")
    )
    payroll_summary = list(
        current_payroll.values("employee__department")
        .annotate(total=Sum("net_salary"), average=Avg("net_salary"), employees=Count("employee"))
        .order_by("-total")
    )
    for row in payroll_summary:
        row["department"] = row.pop("employee__department")
        row["total"], row["average"] = _money(row["total"]), _money(row["average"])
    return Response(
        {
            "absent_more_than_five": _absent_more_than_five(),
            "second_highest_salary": _second_highest_by_department(),
            "new_joiners": EmployeeSerializer(
                Employee.objects.filter(date_of_joining__gte=month_start), many=True
            ).data,
            "on_leave_today": LeaveRequestSerializer(
                LeaveRequest.objects.filter(
                    status="Approved", from_date__lte=today, to_date__gte=today
                ).select_related("employee", "approver"),
                many=True,
            ).data,
            "department_headcount": department_headcount,
            "payroll_summary": payroll_summary,
            "attendance_summary": list(
                Attendance.objects.filter(date__gte=month_start)
                .values("status")
                .annotate(count=Count("id"))
                .order_by("-count")
            ),
        }
    )


def _chat_query(question):
    normalized = question.lower().strip()
    if not any(
        word in normalized
        for word in [
            "employee", "staff", "salary", "payroll", "department", "leave", "absent",
            "attendance", "joined", "manager", "hr", "performance", "workforce",
        ]
    ):
        return None, "I can only help with HRMS and staff-data questions."

    if "absent" in normalized and ("5" in normalized or "five" in normalized):
        rows = _absent_more_than_five()
        return rows, f"{len(rows)} employees were absent more than five times this month."
    if "second" in normalized and ("salary" in normalized or "highest" in normalized):
        rows = _second_highest_by_department()
        return rows, "Here are the second-highest salary earners by department."
    if "joined" in normalized or "joiner" in normalized:
        today = date.today()
        rows = list(
            Employee.objects.filter(
                date_of_joining__year=today.year, date_of_joining__month=today.month
            ).values("employee_id", "full_name", "department", "designation", "date_of_joining")
        )
        return rows, f"{len(rows)} employees joined this month."
    if "currently on leave" in normalized or "on leave today" in normalized:
        today = date.today()
        rows = list(
            LeaveRequest.objects.filter(
                status="Approved", from_date__lte=today, to_date__gte=today
            ).values("employee__employee_id", "employee__full_name", "leave_type", "to_date")
        )
        return rows, f"{len(rows)} employees are currently on leave."
    if "pending" in normalized and "leave" in normalized:
        rows = list(
            LeaveRequest.objects.filter(status="Pending").values(
                "employee__employee_id", "employee__full_name", "leave_type", "from_date", "to_date"
            )
        )
        return rows, f"There are {len(rows)} pending leave requests."
    if "under" in normalized and "manager" in normalized:
        manager = next(
            (e for e in Employee.objects.all() if e.full_name.lower() in normalized), None
        )
        if not manager:
            return [], "Please include the manager's full name."
        rows = list(manager.direct_reports.values("employee_id", "full_name", "department", "designation"))
        return rows, f"{len(rows)} employees report to {manager.full_name}."
    if "average salary" in normalized:
        department = next((d for d in Department.objects.all() if d.name.lower() in normalized), None)
        queryset = Employee.objects.exclude(status="Resigned")
        if department:
            queryset = queryset.filter(department=department.name)
        average = _money(queryset.aggregate(value=Avg("salary"))["value"])
        scope = department.name if department else "the company"
        return [{"scope": scope, "average_salary": average}], f"The average salary for {scope} is AED {average:,.0f}."
    if "highest payroll" in normalized or ("payroll" in normalized and "department" in normalized):
        rows = list(
            Payroll.objects.filter(month__year=date.today().year, month__month=date.today().month)
            .values("employee__department")
            .annotate(payroll_cost=Sum("net_salary"))
            .order_by("-payroll_cost")
        )
        for row in rows:
            row["department"] = row.pop("employee__department")
            row["payroll_cost"] = _money(row["payroll_cost"])
        return rows, f"{rows[0]['department']} has the highest payroll cost." if rows else "No payroll data found."
    if "absenteeism" in normalized:
        rows = list(
            Attendance.objects.filter(
                date__year=date.today().year, date__month=date.today().month, status="Absent"
            )
            .values("employee__department")
            .annotate(absences=Count("id"))
            .order_by("-absences")
        )
        return rows, f"{rows[0]['employee__department']} has the highest absenteeism." if rows else "No absences found."
    if "summary" in normalized or "performance" in normalized:
        absent = Attendance.objects.filter(
            date__year=date.today().year, date__month=date.today().month, status="Absent"
        ).count()
        pending = LeaveRequest.objects.filter(status="Pending").count()
        active = Employee.objects.filter(status="Active").count()
        data = [{"active_employees": active, "monthly_absences": absent, "pending_leave_requests": pending}]
        return data, f"This month: {active} active employees, {absent} absences, and {pending} pending leave requests."
    return [], "I understand HR questions about employees, attendance, leave, payroll, managers, and department analytics. Try one of the suggested prompts."


def _gemini_polish(question, summary, data):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return summary
    prompt = (
        "You are PeopleOps AI. Rewrite the deterministic HRMS result below in at most 3 concise "
        "professional sentences. Do not invent facts. Question: "
        f"{question}\nResult: {summary}\nData: {json.dumps(data, default=str)}"
    )
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            result = json.loads(response.read())
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError):
        return summary


@api_view(["POST"])
def chat(request):
    question = str(request.data.get("message", ""))[:500]
    if not question.strip():
        return Response({"error": "A message is required."}, status=status.HTTP_400_BAD_REQUEST)
    data, summary = _chat_query(question)
    if data is None:
        return Response({"answer": summary, "data": [], "type": "guardrail"})
    return Response(
        {
            "answer": _gemini_polish(question, summary, data),
            "data": data,
            "type": "table" if data else "summary",
        }
    )
