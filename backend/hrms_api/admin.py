from django.contrib import admin

from .models import Attendance, Department, Employee, LeaveRequest, Payroll


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "department", "designation", "status")
    search_fields = ("employee_id", "full_name", "email")
    list_filter = ("department", "status", "employment_type")


admin.site.register(Department)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
admin.site.register(Payroll)
