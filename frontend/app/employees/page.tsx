"use client";

import { useEffect, useMemo, useState } from "react";
import { api, money } from "@/lib/api";
import { Badge, Empty, Loading, PageHeader } from "@/components/UI";

type Employee = Record<string, any>;

export default function EmployeesPage() {
  const [rows, setRows] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const [selected, setSelected] = useState<Employee | null>(null);
  useEffect(() => { api<Employee[]>("/employees/").then(setRows).finally(() => setLoading(false)); }, []);
  const departments = [...new Set(rows.map((x) => x.department))];
  const filtered = useMemo(() => rows.filter((x) =>
    (!department || x.department === department) &&
    (`${x.full_name} ${x.employee_id} ${x.email} ${x.designation}`.toLowerCase().includes(search.toLowerCase()))
  ), [rows, search, department]);
  return <>
    <PageHeader eyebrow="PEOPLE DIRECTORY" title="Employees" copy="A complete view of your people, roles, and reporting structure." actions={<button className="btn primary">＋ Add employee</button>} />
    <div className="toolbar"><div className="field search"><span>⌕</span><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by name, ID, email, or role" /></div><select value={department} onChange={(e) => setDepartment(e.target.value)}><option value="">All departments</option>{departments.map((x) => <option key={x}>{x}</option>)}</select><button className="btn secondary">⇅ Sort</button><span className="result-count">{filtered.length} people</span></div>
    <article className="table-card">
      {loading ? <Loading /> : !filtered.length ? <Empty /> : <div className="table-wrap"><table><thead><tr><th>Employee</th><th>Department</th><th>Role</th><th>Manager</th><th>Location</th><th>Status</th><th>Salary</th><th /></tr></thead><tbody>{filtered.map((e) => <tr key={e.id}><td><div className="person"><span className="avatar" style={{background:e.avatar_color}}>{e.full_name.split(" ").map((n:string) => n[0]).join("")}</span><div><b>{e.full_name}</b><small>{e.employee_id} · {e.email}</small></div></div></td><td><Badge tone="blue">{e.department}</Badge></td><td>{e.designation}</td><td>{e.manager_name || "Executive team"}</td><td>{e.location}</td><td><Badge tone={e.status === "Active" ? "green" : e.status === "On Leave" ? "amber" : "gray"}>{e.status}</Badge></td><td><b>{money(e.salary)}</b></td><td><button className="icon-btn" onClick={() => setSelected(e)}>→</button></td></tr>)}</tbody></table></div>}
    </article>
    {selected && <div className="modal-backdrop" onClick={() => setSelected(null)}><aside className="profile-drawer" onClick={(e) => e.stopPropagation()}><button className="close" onClick={() => setSelected(null)}>×</button><span className="avatar huge" style={{background:selected.avatar_color}}>{selected.full_name.split(" ").map((n:string) => n[0]).join("")}</span><h2>{selected.full_name}</h2><p>{selected.designation} · {selected.department}</p><Badge>{selected.status}</Badge><div className="profile-grid"><div><small>Employee ID</small><b>{selected.employee_id}</b></div><div><small>Joined</small><b>{selected.date_of_joining}</b></div><div><small>Manager</small><b>{selected.manager_name || "Executive team"}</b></div><div><small>Location</small><b>{selected.location}</b></div><div><small>Employment</small><b>{selected.employment_type}</b></div><div><small>Salary</small><b>{money(selected.salary)}</b></div></div><h3>Skills</h3><p>{selected.skills}</p><h3>Employee workspace</h3><div className="placeholder-tabs"><span>Attendance</span><span>Leave</span><span>Payroll</span><span>Documents</span></div></aside></div>}
  </>;
}
