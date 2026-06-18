from rest_framework import serializers

from .models import Attendance, Department, Employee, LeaveRequest, Payroll


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True, default=0)
    average_salary = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, default=0)
    highest_salary = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, default=0)

    class Meta:
        model = Department
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source="manager.full_name", read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"

    def validate_email(self, value):
        queryset = Employee.objects.filter(email__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("This email already exists.")
        return value


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    department = serializers.CharField(source="employee.department", read_only=True)

    class Meta:
        model = Attendance
        fields = "__all__"


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    approver_name = serializers.CharField(source="approver.full_name", read_only=True)
    department = serializers.CharField(source="employee.department", read_only=True)

    class Meta:
        model = LeaveRequest
        fields = "__all__"


class PayrollSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    department = serializers.CharField(source="employee.department", read_only=True)

    class Meta:
        model = Payroll
        fields = "__all__"
