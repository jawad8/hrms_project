from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=60, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    EMPLOYMENT_TYPES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Contract", "Contract"),
        ("Intern", "Intern"),
    ]
    STATUSES = [
        ("Active", "Active"),
        ("On Leave", "On Leave"),
        ("Resigned", "Resigned"),
    ]

    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=50)
    department_ref = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.SET_NULL, related_name="employees"
    )
    designation = models.CharField(max_length=80, blank=True)
    manager = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="direct_reports"
    )
    date_of_joining = models.DateField(null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default="Full Time")
    status = models.CharField(max_length=20, choices=STATUSES, default="Active")
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    location = models.CharField(max_length=80, blank=True)
    skills = models.CharField(max_length=300, blank=True)
    avatar_color = models.CharField(max_length=20, default="#4f46e5")

    class Meta:
        ordering = ["employee_id"]

    def __str__(self):
        return self.full_name


class Attendance(models.Model):
    STATUSES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Leave", "Leave"),
        ("Half Day", "Half Day"),
        ("Work From Home", "Work From Home"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUSES)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "employee__full_name"]
        constraints = [
            models.UniqueConstraint(fields=["employee", "date"], name="unique_employee_attendance")
        ]


class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ("Annual", "Annual"),
        ("Sick", "Sick"),
        ("Emergency", "Emergency"),
        ("Unpaid", "Unpaid"),
    ]
    STATUSES = [("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    status = models.CharField(max_length=20, choices=STATUSES, default="Pending")
    from_date = models.DateField()
    to_date = models.DateField()
    approver = models.ForeignKey(
        Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name="leave_approvals"
    )
    reason = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Payroll(models.Model):
    PAYMENT_STATUSES = [("Paid", "Paid"), ("Pending", "Pending"), ("Processing", "Processing")]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payroll")
    month = models.DateField(help_text="Use the first day of the payroll month")
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default="Pending")

    class Meta:
        ordering = ["-month", "employee__full_name"]
        constraints = [
            models.UniqueConstraint(fields=["employee", "month"], name="unique_employee_payroll")
        ]
