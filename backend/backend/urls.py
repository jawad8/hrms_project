from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hrms_api.views import (
    AttendanceViewSet,
    DepartmentViewSet,
    EmployeeViewSet,
    LeaveRequestViewSet,
    PayrollViewSet,
    chat,
    dashboard,
    home,
    reports,
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename="employee")
router.register(r'attendance', AttendanceViewSet, basename="attendance")
router.register(r'departments', DepartmentViewSet, basename="department")
router.register(r'leave-requests', LeaveRequestViewSet, basename="leave-request")
router.register(r'payroll', PayrollViewSet, basename="payroll")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),   # APIs
    path('api/dashboard/', dashboard, name="dashboard"),
    path('api/reports/', reports, name="reports"),
    path('api/chat/', chat, name="chat"),
    path('', home, name="home"),          # Frontend
]
