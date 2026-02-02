const API = "/api";

// Add Employee
$("#addEmp").click(function(){
    let data = {
        employee_id: $("#emp_id").val(),
        full_name: $("#name").val(),
        email: $("#email").val(),
        department: $("#dept").val()
    };

    $.ajax({
        url: API + "/employees/",
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(){
            alert("Employee Added!");
            loadEmployees();
            updateDashboard();
            $("#emp_id, #name, #email, #dept").val("");
        },
        error: function(err){
            alert("Error: " + err.responseText);
        }
    });
});

// Load Employees
function loadEmployees(){
    $("#employeeList").html('<div class="text-muted">Loading...</div>');

    $.get(API + "/employees/", function(data){
        $("#totalEmployees").text(data.length);

        if(data.length === 0){
            $("#employeeList").html('<div class="text-muted">No employees found.</div>');
            return;
        }

        let html = "";
        data.forEach(emp => {
            html += `
            <div>
                <strong>${emp.employee_id}</strong> - ${emp.full_name} (${emp.department})
                <button class="btn btn-sm btn-danger delete-btn" onclick="deleteEmp(${emp.id})">Delete</button>
            </div>
            `;
        });
        $("#employeeList").html(html);
    });
}

// Delete Employee
function deleteEmp(id){
    if(!confirm("Are you sure you want to delete this employee?")) return;

    $.ajax({
        url: API + "/employees/" + id + "/",
        type: "DELETE",
        success: function(){
            loadEmployees();
            loadAttendance();
            updateDashboard();
        }
    });
}

// Mark Attendance
$("#markAtt").click(function(){
    let data = {
        employee: $("#att_emp_id").val(),
        date: $("#date").val(),
        status: $("#status").val()
    };

    $.ajax({
        url: API + "/attendance/",
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(){
            alert("Attendance Marked!");
            loadAttendance();
            updateDashboard();
            $("#att_emp_id, #date").val("");
        },
        error: function(err){
            alert("Error: " + err.responseText);
        }
    });
});

// Load Attendance with Filter
function loadAttendance(){
    $("#attendanceList").html('<div class="text-muted">Loading...</div>');

    let selectedDate = $("#filterDate").val();

    $.get(API + "/attendance/", function(data){
        if(selectedDate){
            data = data.filter(a => a.date === selectedDate);
        }

        if(data.length === 0){
            $("#attendanceList").html('<div class="text-muted">No records found.</div>');
            return;
        }

        let html = "";
        data.forEach(a => {
            html += `
            <div>
                <strong>Emp ID:</strong> ${a.employee} |
                <strong>Date:</strong> ${a.date} |
                <span class="${a.status === 'Present' ? 'text-success' : 'text-danger'}">
                  ${a.status}
                </span>
            </div>
            `;
        });
        $("#attendanceList").html(html);
    });
}

// Update Dashboard (Present / Absent Today)
function updateDashboard(){
    let today = new Date().toISOString().split("T")[0];

    $.get(API + "/attendance/", function(data){
        let todayRecords = data.filter(a => a.date === today);

        let presentCount = todayRecords.filter(a => a.status === "Present").length;
        let absentCount = todayRecords.filter(a => a.status === "Absent").length;

        $("#presentToday").text(presentCount);
        $("#absentToday").text(absentCount);
    });
}

// Initial load
loadEmployees();
loadAttendance();
updateDashboard();
