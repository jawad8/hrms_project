# HRMS Lite

### HOW TO RUN THE PROJECT ###
## check this link for reference -> https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ ##
(Please use the requirements.txt file to setup the venv)
step1 -> download the zip from the git repo.
step2 -> extract the contents from the zip
step3 -> open terminal and go to the directory hrms_main/backend
step4 -> run django server.
step5 -> open http://127.0.0.1:8000/ on any web browser to access the web application.

## Overview

HRMS Lite is a lightweight, web-based Human Resource Management System designed to handle core HR operations such as employee management and daily attendance tracking.  

The system follows a clear separation of concerns between frontend and backend, with a RESTful API layer built using Django REST Framework and a Bootstrap-based user interface served through Django templates. The application is designed to be simple, maintainable, and realistically usable rather than a feature-heavy demo.

This project was built keeping in mind:
- Clean architecture  
- Readable and modular code  
- Proper API design  
- Basic validation and error handling  
- A professional, user-friendly UI  
- Deployment readiness  

---


## Tech Stack

### Backend
- Python
- Django
- Django REST Framework (DRF)
- SQLite (Development)
- PostgreSQL (Production-ready)

### Frontend
- HTML
- CSS
- Bootstrap (via CDN)
- jQuery
- AJAX

### Deployment
- Backend: Render  
- Frontend: Served via Django (same domain as backend)

---

## Features Implemented

### Employee Management
- Add new employees with:
  - Employee ID (unique)
  - Full Name
  - Email (validated, unique)
  - Department  
- View all employees in a structured list  
- Delete employees with confirmation  

### Attendance Management
- Mark attendance for an employee with:
  - Date  
  - Status (Present / Absent)  
- View attendance records  
- Filter attendance by date  

### Dashboard (Bonus Feature)
- Total number of employees  
- Number of employees Present today  
- Number of employees Absent today  

### Backend & API
- Fully RESTful APIs using Django REST Framework  
- Proper HTTP status codes  
- Server-side validation  
- Duplicate employee prevention  
- Graceful error handling  
- Relational database modeling with foreign key constraints  
