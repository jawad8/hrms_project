"use client";

import { DataModule } from "@/components/DataModule";

export default function LeavePage() {
  return <DataModule config={{
    eyebrow:"TIME OFF",title:"Leave management",endpoint:"/leave-requests/",
    copy:"Review balances, approvals, and upcoming team availability.",
    columns:[["employee_name","Employee"],["department","Department"],["leave_type","Leave type"],["from_date","From"],["to_date","To"],["approver_name","Approver"],["status","Status"],["reason","Reason"]],
    statusKey:"status",
    stats:(r)=>[
      {label:"Pending approvals",value:r.filter(x=>x.status==="Pending").length,detail:"Awaiting manager review",icon:"◷",tone:"amber"},
      {label:"Approved",value:r.filter(x=>x.status==="Approved").length,detail:"Scheduled leave",icon:"✓",tone:"teal"},
      {label:"Annual leave",value:r.filter(x=>x.leave_type==="Annual").length,detail:"Most used leave type",icon:"☼"},
    ],
  }} />;
}
