"use client";

import { useEffect, useState } from "react";
import { api, downloadCsv, money } from "@/lib/api";
import { Badge, Loading, PageHeader } from "@/components/UI";

const reportMeta: Record<string, [string,string]> = {
  absent_more_than_five:["Attendance exceptions","Employees absent more than five times this month"],
  second_highest_salary:["Salary benchmark","Second-highest salary earners by department"],
  new_joiners:["Talent movement","New joiners this month"],
  on_leave_today:["Live availability","Employees currently on approved leave"],
  department_headcount:["Workforce distribution","Department-wise active headcount"],
  payroll_summary:["Compensation","Department payroll summary"],
  attendance_summary:["Attendance mix","Monthly attendance by status"],
};

export default function ReportsPage() {
  const [data,setData]=useState<Record<string,Record<string,any>[]> | null>(null);
  const [active,setActive]=useState("absent_more_than_five");
  useEffect(()=>{api<Record<string,Record<string,any>[]> >("/reports/").then(setData)},[]);
  if(!data) return <Loading />;
  const rows=data[active] || []; const keys=rows.length?Object.keys(rows[0]):[];
  return <><PageHeader eyebrow="ANALYTICS LIBRARY" title="Reports" copy="Decision-ready workforce reports with one-click CSV exports." actions={<button className="btn primary" onClick={()=>downloadCsv(active,rows)}>↓ Export current report</button>} />
    <div className="reports-layout"><aside className="report-menu">{Object.entries(reportMeta).map(([key,[title,copy]])=><button className={active===key?"active":""} onClick={()=>setActive(key)} key={key}><span>↗</span><div><b>{title}</b><small>{copy}</small></div></button>)}</aside>
      <article className="panel report-view"><div className="panel-head"><div><span className="eyebrow">READY-MADE REPORT</span><h2>{reportMeta[active][0]}</h2><p>{reportMeta[active][1]}</p></div><Badge tone="blue">{rows.length} results</Badge></div>
      {!rows.length?<div className="empty"><span>✓</span><b>No exceptions found</b><p>Your workforce looks clear for this report.</p></div>:<div className="table-wrap"><table><thead><tr>{keys.map(k=><th key={k}>{k.replaceAll("_"," ")}</th>)}</tr></thead><tbody>{rows.map((r,i)=><tr key={i}>{keys.map(k=><td key={k}>{k.includes("salary")||k==="total"||k==="average"?money(r[k]):String(r[k]??"—")}</td>)}</tr>)}</tbody></table></div>}</article>
    </div></>;
}
