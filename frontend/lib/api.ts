export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`Request failed (${response.status})`);
  return response.json();
}

export const money = (value: number | string) =>
  new Intl.NumberFormat("en-AE", {
    style: "currency",
    currency: "AED",
    maximumFractionDigits: 0,
  }).format(Number(value));

export const downloadCsv = (name: string, rows: Record<string, unknown>[]) => {
  if (!rows.length) return;
  const headers = Object.keys(rows[0]);
  const csv = [headers.join(","), ...rows.map((row) => headers.map((h) =>
    `"${String(row[h] ?? "").replaceAll('"', '""')}"`).join(","))].join("\n");
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  link.download = `${name}.csv`;
  link.click();
  URL.revokeObjectURL(link.href);
};
