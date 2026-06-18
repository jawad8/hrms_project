@echo off
setlocal
pushd "%~dp0"

set "VENV_DIR=%CD%\.venv"
set "PYTHON=%VENV_DIR%\Scripts\python.exe"

echo.
echo ==================================================
echo   PeopleOps HRMS - Local Development Launcher
echo ==================================================
echo.

where node >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js 20 or newer is required.
    goto :failed
)

if not exist "%PYTHON%" (
    echo [1/6] Creating Python environment...
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3 -m venv "%VENV_DIR%"
    ) else (
        python -m venv "%VENV_DIR%"
    )
    if errorlevel 1 goto :failed
) else (
    echo [1/6] Python environment ready.
)

echo [2/6] Installing backend dependencies...
"%PYTHON%" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto :failed

if not exist ".env" copy /Y ".env.example" ".env" >nul
for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do set "%%A=%%B"

echo [3/6] Applying database migrations...
"%PYTHON%" backend\manage.py migrate --noinput
if errorlevel 1 goto :failed

echo [4/6] Preparing demo workforce data...
"%PYTHON%" backend\manage.py shell -c "from hrms_api.models import Employee; import subprocess,sys; subprocess.run([sys.executable,'backend/manage.py','seed_hrms']) if Employee.objects.count() < 40 else None"
if errorlevel 1 goto :failed

echo [5/6] Installing frontend dependencies...
call npm.cmd install --prefix frontend --no-audit --no-fund
if errorlevel 1 goto :failed

if not exist "frontend\.env.local" copy /Y "frontend\.env.example" "frontend\.env.local" >nul

echo [6/6] Starting Django API and Next.js...
start "PeopleOps API" /D "%CD%\backend" cmd.exe /k ""%PYTHON%" manage.py runserver 127.0.0.1:8000"
start "PeopleOps Frontend" /D "%CD%\frontend" cmd.exe /k "npm.cmd run dev"

echo.
echo API:       http://127.0.0.1:8000/api/
echo Frontend:  http://localhost:3000
echo.
echo Two service windows have been opened. Close them to stop the project.
timeout /t 4 >nul
start "" http://localhost:3000
popd
exit /b 0

:failed
echo.
echo ERROR: Project startup failed. Review the message above.
popd
pause
exit /b 1
