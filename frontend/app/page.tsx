"use client";

import { useEffect, useState } from "react";
import { api, downloadCsv, money } from "@/lib/api";
import { BarChart, Loading, PageHeader, StatCard } from "@/components/UI";

type Dashboard = {
  metrics: Record<string, number>;
  department_headcount: Record<string, any>[];
  attendance_trend: Record<string, any>[];
  salary_by_department: Record<string, any>[];
  recent_employees: Record<string, any>[];
};

export default function DashboardPage() {
  const [data, setData] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");
  useEffect(() => { api<Dashboard>("/dashboard/").then(setData).catch(() => setError("Unable to connect to the HRMS API. Start the Django service and refresh.")); }, []);
  if (error) return <div className="error-banner">{error}</div>;
  if (!data) return <Loading />;
  const m = data.metrics;
  const downloadDashboardReport = () => {
    const report = [
      { metric: "Generated at", value: new Date().toLocaleString("en-AE") },
      { metric: "Total employees", value: m.total_employees },
      { metric: "Active employees", value: m.active_employees },
      { metric: "Employees on leave today", value: m.on_leave_today },
      { metric: "Monthly absences", value: m.monthly_absences },
      { metric: "Monthly payroll", value: money(m.payroll_total) },
      { metric: "Average salary", value: money(m.average_salary) },
      { metric: "Department count", value: m.department_count },
      { metric: "New joiners this month", value: m.new_joiners },
      { metric: "Attrition count", value: m.attrition_count },
    ];
    downloadCsv(`peopleops-dashboard-${new Date().toISOString().slice(0, 10)}`, report);
  };

  return <>
    <PageHeader eyebrow="THURSDAY · WORKFORCE PULSE" title="Good evening, Jawad" copy="Here’s what’s happening across your organization today." actions={<><button className="btn secondary" onClick={downloadDashboardReport}>Download report</button><button className="btn primary">＋ Add employee</button></>} />
    <section className="stats-grid">
      <StatCard label="Total employees" value={m.total_employees} detail={`${m.new_joiners} joined this month`} icon="♙" />
      <StatCard label="Active workforce" value={m.active_employees} detail={`${Math.round(m.active_employees / m.total_employees * 100)}% of total headcount`} tone="teal" icon="✓" />
      <StatCard label="On leave today" value={m.on_leave_today} detail="Approved leave requests" tone="amber" icon="◷" />
      <StatCard label="Monthly payroll" value={money(m.payroll_total)} detail={`${money(m.average_salary)} avg. salary`} tone="violet" icon="◇" />
    </section>
    <section className="dashboard-grid">
      <article className="panel wide"><div className="panel-head"><div><h2>Attendance pulse</h2><p>Present vs absent · last 7 days</p></div><span className="live">● Live data</span></div>
        <div className="attendance-chart">{data.attendance_trend.map((d, i) => <div className="day" key={i}><div className="columns"><i style={{height: `${d.present * 3.2}px`}} /><i style={{height: `${Math.max(d.absent * 8, 5)}px`}} /></div><span>{d.date}</span></div>)}</div>
        <div className="legend"><span><i className="dot indigo" /> Present / remote</span><span><i className="dot coral" /> Absent</span></div>
      </article>
      <article className="panel"><div className="panel-head"><div><h2>Headcount by team</h2><p>Active distribution</p></div></div><BarChart data={data.department_headcount} /></article>
      <article className="panel"><div className="panel-head"><div><h2>Organization health</h2><p>Signals requiring attention</p></div></div>
        <div className="health-score"><div><strong>{Math.max(0, 94 - m.monthly_absences)}</strong><span>/100</span></div><p>Healthy</p></div>
        <div className="health-items"><p><span>Monthly absences</span><b>{m.monthly_absences}</b></p><p><span>New joiners</span><b>{m.new_joiners}</b></p><p><span>Attrition</span><b>{m.attrition_count}</b></p></div>
      </article>
      <article className="panel wide"><div className="panel-head"><div><h2>Salary benchmark</h2><p>Average monthly salary by department</p></div></div><BarChart data={data.salary_by_department} /></article>
    </section>
  </>;
}
