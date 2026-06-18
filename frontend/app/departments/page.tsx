"use client";

import { DataModule } from "@/components/DataModule";
import { money } from "@/lib/api";

export default function DepartmentsPage() {
  return <DataModule config={{
    eyebrow: "ORGANIZATION", title: "Departments", endpoint: "/departments/",
    copy: "Understand team composition, leadership, and salary distribution.",
    columns: [["name","Department"],["code","Code"],["employee_count","Headcount"],["average_salary","Average salary"],["highest_salary","Highest salary"],["description","Mandate"]],
    moneyKeys: ["average_salary","highest_salary"],
    stats: (r) => [
      {label:"Departments",value:r.length,detail:"Core business functions",icon:"▦"},
      {label:"Largest team",value:[...r].sort((a,b)=>b.employee_count-a.employee_count)[0]?.name || "—",detail:"By active headcount",icon:"♙",tone:"teal"},
      {label:"Highest average",value:money(Math.max(...r.map(x=>Number(x.average_salary || 0)),0)),detail:"Monthly department avg.",icon:"◇",tone:"violet"},
    ],
  }} />;
}
