export function PageHeader({ eyebrow, title, copy, actions }: { eyebrow?: string; title: string; copy: string; actions?: React.ReactNode }) {
  return <div className="page-header"><div>{eyebrow && <span className="eyebrow">{eyebrow}</span>}<h1>{title}</h1><p>{copy}</p></div>{actions && <div className="header-actions">{actions}</div>}</div>;
}

export function StatCard({ label, value, detail, tone = "indigo", icon }: { label: string; value: string | number; detail: string; tone?: string; icon: string }) {
  return <article className="stat-card"><div className={`stat-icon ${tone}`}>{icon}</div><div className="stat-label">{label}</div><strong>{value}</strong><small>{detail}</small></article>;
}

export function Badge({ children, tone = "green" }: { children: React.ReactNode; tone?: string }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}

export function Loading() {
  return <div className="loading-card"><span /><span /><span /><p>Loading workforce data…</p></div>;
}

export function Empty({ text = "No records found" }: { text?: string }) {
  return <div className="empty"><span>⌕</span><b>{text}</b><p>Try adjusting the selected filters.</p></div>;
}

export function BarChart({ data, valueKey = "value", labelKey = "department" }: { data: Record<string, any>[]; valueKey?: string; labelKey?: string }) {
  const max = Math.max(...data.map((x) => Number(x[valueKey])), 1);
  return <div className="bar-chart">{data.map((item, i) => <div className="bar-row" key={i}><span>{item[labelKey]}</span><div><i style={{ width: `${Number(item[valueKey]) / max * 100}%` }} /></div><b>{Number(item[valueKey]).toLocaleString()}</b></div>)}</div>;
}
