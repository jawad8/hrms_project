from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Attendance, Employee


class HRMSApiTests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id="EMP-001",
            full_name="Aisha Khan",
            email="aisha@example.com",
            department="Engineering",
        )

    def test_create_employee(self):
        response = self.client.post(
            reverse("employee-list"),
            {
                "employee_id": "EMP-002",
                "full_name": "Omar Ali",
                "email": "omar@example.com",
                "department": "Design",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(employee_id="EMP-002").exists())

    def test_reject_duplicate_employee_email(self):
        response = self.client.post(
            reverse("employee-list"),
            {
                "employee_id": "EMP-003",
                "full_name": "Another Employee",
                "email": self.employee.email,
                "department": "Finance",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_attendance(self):
        response = self.client.post(
            reverse("attendance-list"),
            {
                "employee": self.employee.id,
                "date": "2026-06-18",
                "status": "Present",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)
