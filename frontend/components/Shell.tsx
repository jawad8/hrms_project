"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const nav = [
  ["/", "⌂", "Overview"],
  ["/employees", "♙", "Employees"],
  ["/departments", "▦", "Departments"],
  ["/attendance", "✓", "Attendance"],
  ["/leave", "◷", "Leave"],
  ["/payroll", "◇", "Payroll"],
  ["/reports", "↗", "Reports"],
  ["/assistant", "✦", "PeopleOps AI"],
];

export function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const [dark, setDark] = useState(false);
  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
  }, [dark]);
  return (
    <div className="app-shell">
      <aside className={`sidebar ${open ? "open" : ""}`}>
        <div className="brand"><span className="brand-mark">P</span><div><b>PeopleOps</b><small>HR intelligence</small></div></div>
        <nav>
          <p className="nav-label">WORKSPACE</p>
          {nav.map(([href, icon, label]) => (
            <Link key={href} href={href} onClick={() => setOpen(false)}
              className={path === href ? "active" : ""}><span>{icon}</span>{label}</Link>
          ))}
        </nav>
        <div className="sidebar-card"><span>✦</span><b>AI-powered insights</b><p>Ask questions across your workforce data.</p><Link href="/assistant">Open assistant →</Link></div>
        <div className="sidebar-user"><span className="avatar">JM</span><div><b>Jawad Malik</b><small>HR Administrator</small></div><span>⋮</span></div>
      </aside>
      <div className="workspace">
        <header className="topbar">
          <button className="menu-btn" onClick={() => setOpen(!open)}>☰</button>
          <div className="global-search"><span>⌕</span><input aria-label="Global search" placeholder="Search people, reports, or actions..." /><kbd>⌘ K</kbd></div>
          <div className="top-actions"><button onClick={() => setDark(!dark)}>{dark ? "☀" : "☾"}</button><button className="notification">♢<i /></button><span className="avatar">JM</span></div>
        </header>
        <main>{children}</main>
      </div>
    </div>
  );
}
