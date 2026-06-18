"use client";

import { DataModule } from "@/components/DataModule";

export default function AttendancePage() {
  return <DataModule config={{
    eyebrow:"TIME & ATTENDANCE",title:"Attendance",endpoint:"/attendance/",
    copy:"Monitor presence, remote work, and attendance exceptions.",
    columns:[["date","Date"],["employee_name","Employee"],["department","Department"],["status","Status"],["check_in","Check in"],["check_out","Check out"],["remarks","Remarks"]],
    statusKey:"status",
    stats:(r)=>[
      {label:"Records",value:r.length,detail:"Across the last 60 days",icon:"✓"},
      {label:"Present",value:r.filter(x=>x.status==="Present").length,detail:"Office attendance",icon:"●",tone:"teal"},
      {label:"Remote days",value:r.filter(x=>x.status==="Work From Home").length,detail:"Flexible work",icon:"⌂",tone:"violet"},
      {label:"Absences",value:r.filter(x=>x.status==="Absent").length,detail:"Requires monitoring",icon:"!",tone:"amber"},
    ],
  }} />;
}
