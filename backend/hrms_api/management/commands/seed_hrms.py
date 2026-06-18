import random
from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from hrms_api.models import Attendance, Department, Employee, LeaveRequest, Payroll


class Command(BaseCommand):
    help = "Seed a recruiter-demo HR dataset"

    def handle(self, *args, **options):
        random.seed(42)
        Attendance.objects.all().delete()
        LeaveRequest.objects.all().delete()
        Payroll.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()

        department_data = [
            ("Engineering", "ENG", "Product engineering and platform delivery"),
            ("HR", "HR", "People operations and talent"),
            ("Finance", "FIN", "Financial planning and governance"),
            ("Sales", "SAL", "Revenue growth and partnerships"),
            ("Operations", "OPS", "Business operations and service delivery"),
        ]
        departments = {
            name: Department.objects.create(name=name, code=code, description=description)
            for name, code, description in department_data
        }

        names = [
            "Aarav Mehta", "Aisha Khan", "Zain Ahmed", "Diya Nair", "Omar Farooq",
            "Maya Iyer", "Rohan Desai", "Sara Ali", "Arjun Kapoor", "Noor Hassan",
            "Kabir Malhotra", "Leena Joseph", "Rehan Siddiqui", "Ananya Rao", "Yusuf Khan",
            "Meera Menon", "Adil Shaikh", "Nadia Rahman", "Vikram Singh", "Hiba Faisal",
            "Ishaan Patel", "Fatima Noor", "Sameer Kulkarni", "Priya Sharma", "Hamza Tariq",
            "Riya Das", "Imran Qureshi", "Sana Mirza", "Dev Bhatia", "Mariam Abbas",
            "Karan Verma", "Layla Saeed", "Nikhil Jain", "Zoya Akhtar", "Fahad Malik",
            "Neha Gupta", "Bilal Ansari", "Tara Krishnan", "Adeel Raza", "Kavya Pillai",
            "Rayyan Bashir", "Simran Kaur", "Abdul Rahim", "Pooja Shetty", "Aliya Merchant",
        ]
        designations = {
            "Engineering": ["VP Engineering", "Engineering Manager", "Senior Software Engineer", "Software Engineer", "QA Engineer"],
            "HR": ["Head of People", "HR Manager", "Talent Partner", "HR Executive", "People Analyst"],
            "Finance": ["Finance Director", "Finance Manager", "Senior Accountant", "Financial Analyst", "Accountant"],
            "Sales": ["Sales Director", "Sales Manager", "Account Executive", "Business Development Executive", "Sales Analyst"],
            "Operations": ["COO", "Operations Manager", "Project Coordinator", "Operations Analyst", "Service Executive"],
        }
        locations = ["Dubai", "Abu Dhabi", "Sharjah", "Bengaluru", "Mumbai"]
        skills = {
            "Engineering": "Python, React, Cloud",
            "HR": "Talent Management, HRIS, Employee Relations",
            "Finance": "FP&A, Excel, Financial Reporting",
            "Sales": "CRM, Negotiation, Account Management",
            "Operations": "Process Design, Delivery, Analytics",
        }
        colors = ["#4f46e5", "#0f766e", "#0369a1", "#c2410c", "#7c3aed"]
        today = date.today()
        employees = []

        for index, name in enumerate(names):
            department_name = department_data[index % 5][0]
            level = min(index // 10, 4)
            joining_date = today - timedelta(days=90 + index * 21)
            if index in [7, 18, 29]:
                joining_date = today.replace(day=max(1, min(today.day, 3 + index % 12)))
            status = "Resigned" if index in [39, 43] else "Active"
            employee = Employee.objects.create(
                employee_id=f"EMP-{index + 1:03d}",
                full_name=name,
                email=f"{name.lower().replace(' ', '.')}@peopleops.demo",
                phone=f"+971 50 {1000000 + index:07d}",
                department=department_name,
                department_ref=departments[department_name],
                designation=designations[department_name][level],
                date_of_joining=joining_date,
                employment_type="Contract" if index in [11, 27, 41] else "Full Time",
                status=status,
                salary=Decimal(32000 - level * 4000 + (index % 5) * 350),
                location=locations[index % len(locations)],
                skills=skills[department_name],
                avatar_color=colors[index % len(colors)],
            )
            employees.append(employee)

        for index, employee in enumerate(employees):
            if index >= 5:
                employee.manager = employees[index % 5]
                employee.save(update_fields=["manager"])

        for offset in range(59, -1, -1):
            day = today - timedelta(days=offset)
            if day.weekday() >= 5:
                continue
            for index, employee in enumerate(employees):
                if employee.status == "Resigned":
                    continue
                forced_absence = (
                    index in [6, 16, 26]
                    and day.month == today.month
                    and day.day <= 14
                )
                roll = random.random()
                status = "Absent" if forced_absence or roll < 0.045 else "Work From Home" if roll < 0.13 else "Present"
                Attendance.objects.create(
                    employee=employee,
                    date=day,
                    status=status,
                    check_in=None if status == "Absent" else time(8 + index % 2, 30 + index % 20),
                    check_out=None if status == "Absent" else time(17 + index % 2, index % 20),
                    remarks="Planned remote day" if status == "Work From Home" else "",
                )

        LeaveRequest.objects.create(
            employee=employees[8], leave_type="Annual", status="Approved",
            from_date=today - timedelta(days=1), to_date=today + timedelta(days=2),
            approver=employees[3], reason="Family holiday",
        )
        employees[8].status = "On Leave"
        employees[8].save(update_fields=["status"])
        LeaveRequest.objects.create(
            employee=employees[22], leave_type="Sick", status="Approved",
            from_date=today, to_date=today + timedelta(days=1),
            approver=employees[2], reason="Medical recovery",
        )
        employees[22].status = "On Leave"
        employees[22].save(update_fields=["status"])
        for index, leave_type in zip([12, 24, 31, 37], ["Annual", "Emergency", "Sick", "Unpaid"]):
            LeaveRequest.objects.create(
                employee=employees[index], leave_type=leave_type, status="Pending",
                from_date=today + timedelta(days=5 + index % 4),
                to_date=today + timedelta(days=7 + index % 4),
                approver=employees[index % 5], reason="Personal request pending manager review",
            )
        LeaveRequest.objects.create(
            employee=employees[15], leave_type="Annual", status="Rejected",
            from_date=today + timedelta(days=10), to_date=today + timedelta(days=15),
            approver=employees[0], reason="Annual leave request",
        )

        current_month = today.replace(day=1)
        previous_month = (current_month - timedelta(days=1)).replace(day=1)
        for employee in employees:
            if employee.status == "Resigned":
                continue
            for month, paid in [(previous_month, "Paid"), (current_month, "Processing")]:
                basic = employee.salary
                allowances = (basic * Decimal("0.18")).quantize(Decimal("0.01"))
                deductions = (basic * Decimal("0.035")).quantize(Decimal("0.01"))
                Payroll.objects.create(
                    employee=employee, month=month, basic_salary=basic,
                    allowances=allowances, deductions=deductions,
                    net_salary=basic + allowances - deductions, payment_status=paid,
                )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Employee.objects.count()} employees, {Attendance.objects.count()} attendance records, "
            f"{LeaveRequest.objects.count()} leave requests, and {Payroll.objects.count()} payroll records."
        ))
