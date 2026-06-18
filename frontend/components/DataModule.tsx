"use client";

import { useEffect, useMemo, useState } from "react";
import { api, downloadCsv, money } from "@/lib/api";
import { Badge, Empty, Loading, PageHeader, StatCard } from "./UI";

type Config = {
  title: string; eyebrow: string; copy: string; endpoint: string;
  columns: [string, string][]; statusKey?: string; moneyKeys?: string[];
  stats?: (rows: Record<string, any>[]) => { label: string; value: string | number; detail: string; icon: string; tone?: string }[];
};

export function DataModule({ config }: { config: Config }) {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  useEffect(() => { api<Record<string, any>[]>(config.endpoint).then(setRows).finally(() => setLoading(false)); }, [config.endpoint]);
  const filtered = useMemo(() => rows.filter((row) => JSON.stringify(row).toLowerCase().includes(search.toLowerCase())), [rows, search]);
  const stats = config.stats?.(rows) || [];
  return <>
    <PageHeader eyebrow={config.eyebrow} title={config.title} copy={config.copy} actions={<><button className="btn secondary" onClick={() => downloadCsv(config.title.toLowerCase(), filtered)}>↓ Export CSV</button><button className="btn primary">＋ Add record</button></>} />
    {!!stats.length && <section className="stats-grid compact">{stats.map((s) => <StatCard key={s.label} {...s} tone={s.tone} />)}</section>}
    <div className="toolbar"><div className="field search"><span>⌕</span><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder={`Search ${config.title.toLowerCase()}...`} /></div><button className="btn secondary">☷ Filters</button><span className="result-count">{filtered.length} records</span></div>
    <article className="table-card">{loading ? <Loading /> : !filtered.length ? <Empty /> : <div className="table-wrap"><table><thead><tr>{config.columns.map(([key, label]) => <th key={key}>{label}</th>)}</tr></thead><tbody>{filtered.map((row, i) => <tr key={row.id || i}>{config.columns.map(([key]) => <td key={key}>{key === config.statusKey ? <Badge tone={row[key] === "Approved" || row[key] === "Paid" || row[key] === "Present" ? "green" : row[key] === "Pending" || row[key] === "Processing" ? "amber" : row[key] === "Absent" || row[key] === "Rejected" ? "red" : "blue"}>{row[key]}</Badge> : config.moneyKeys?.includes(key) ? <b>{money(row[key])}</b> : row[key] || "—"}</td>)}</tr>)}</tbody></table></div>}</article>
  </>;
}
