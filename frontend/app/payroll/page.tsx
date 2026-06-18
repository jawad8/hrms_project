"use client";

import { DataModule } from "@/components/DataModule";
import { money } from "@/lib/api";

export default function PayrollPage() {
  return <DataModule config={{
    eyebrow:"COMPENSATION",title:"Payroll",endpoint:"/payroll/",
    copy:"Track monthly compensation, deductions, and payment readiness.",
    columns:[["month","Period"],["employee_name","Employee"],["department","Department"],["basic_salary","Basic salary"],["allowances","Allowances"],["deductions","Deductions"],["net_salary","Net salary"],["payment_status","Status"]],
    statusKey:"payment_status",moneyKeys:["basic_salary","allowances","deductions","net_salary"],
    stats:(r)=>[
      {label:"Total payroll",value:money(r.reduce((s,x)=>s+Number(x.net_salary),0)),detail:"All visible periods",icon:"◇",tone:"violet"},
      {label:"Average net pay",value:money(r.length?r.reduce((s,x)=>s+Number(x.net_salary),0)/r.length:0),detail:"Per payroll record",icon:"≈"},
      {label:"Processing",value:r.filter(x=>x.payment_status==="Processing").length,detail:"Current cycle records",icon:"◷",tone:"amber"},
    ],
  }} />;
}
