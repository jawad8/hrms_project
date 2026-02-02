from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer

# -------- FRONTEND PAGE --------
def home(request):
    return render(request, "index.html")

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
