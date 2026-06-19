# PeopleOps HRMS

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/jawad8/hrms_project/tree/codex/peopleops-hrms)

**Live demo:** https://peopleops-hrms.vercel.app

PeopleOps is a recruiter-ready, full-stack human resource management platform. It turns workforce records into a polished operational dashboard with employee management, attendance, leave, payroll, reports, and a database-grounded AI assistant.

## Business problem

HR teams often work across fragmented spreadsheets and disconnected tools. PeopleOps gives managers one place to understand headcount, availability, attendance risk, leave approvals, salary distribution, and payroll cost—without losing the ability to inspect the underlying employee records.

## Highlights

- Enterprise Next.js dashboard with responsive sidebar, dark mode, cards, tables, filters, profile drawer, loading and empty states
- 45 synthetic UAE/India-style employee profiles across Engineering, HR, Finance, Sales, and Operations
- Two months of seeded attendance with office, absent, leave, half-day, and remote-work support
- Leave requests, approval states, approvers, and current availability
- Monthly payroll with basic salary, allowances, deductions, net salary, and payment status
- Department headcount and salary analytics
- Ready-made reports with CSV export
- PeopleOps AI assistant with deterministic HR queries, HR-only guardrails, and optional Gemini response polishing
- Django REST API, SQLite, admin interface, tests, Docker, and Render deployment blueprint

## Architecture

```text
Next.js 15 + TypeScript
        |
        | REST / JSON
        v
Django 6 + Django REST Framework
        |
        +-- SQLite workforce database
        +-- deterministic analytics / safe chat actions
        +-- Gemini API (server-side only, optional)
```

The AI assistant never sends a database query from the browser and cannot perform destructive actions. Known HR questions are answered with safe Django ORM queries first. When `GEMINI_API_KEY` is configured, Gemini only turns that verified result into concise natural language.

## Run locally

Double-click **`run project.bat`** on Windows. It creates the Python environment, installs backend and frontend packages, migrates and seeds the database, and opens:

- Frontend: http://localhost:3000
- API: http://127.0.0.1:8000/api/
- Django admin: http://127.0.0.1:8000/admin/

Manual startup:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python backend\manage.py migrate
.venv\Scripts\python backend\manage.py seed_hrms
.venv\Scripts\python backend\manage.py runserver

cd frontend
npm install
copy .env.example .env.local
npm run dev
```

## Gemini setup

Add the key only to the root `.env` file:

```env
GEMINI_API_KEY=your_key_here
```

Never place it in `frontend/.env.local` or use a `NEXT_PUBLIC_` key. The assistant remains fully usable without Gemini because its analytics are deterministic.

## Suggested AI questions

- Which employees were absent more than 5 times this month?
- Department-wise list the employees whose salary is second highest.
- Who joined this month?
- Which department has the highest payroll cost?
- Show employees currently on leave.
- What is the average salary in the Engineering department?
- Which employees have pending leave approvals?
- Give me a summary of HR performance this month.

## Testing

```bash
.venv\Scripts\python backend\manage.py test
.venv\Scripts\python backend\manage.py check
cd frontend
npm run build
```

## Live demo deployment

The included `render.yaml` creates the Django API service used by the Vercel frontend:

1. `jawad8-peopleops-api` — Django API

Deploy the `frontend/` directory to Vercel and set `NEXT_PUBLIC_API_URL` to the Render API URL. In Render, create a **Blueprint** from this repository and optionally provide `GEMINI_API_KEY`. If either platform assigns a different URL, update `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `NEXT_PUBLIC_API_URL`.

## Screenshots

Add final hosted screenshots to `docs/` after deployment:

- Dashboard overview
- Employee directory and profile
- Reports
- PeopleOps AI assistant

All included employee data is synthetic and intended for portfolio demonstration.
