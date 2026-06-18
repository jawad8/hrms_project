import type { Metadata } from "next";
import "./globals.css";
import { Shell } from "@/components/Shell";

export const metadata: Metadata = {
  title: "PeopleOps — Intelligent HRMS",
  description: "Enterprise HR analytics, workforce operations, and AI assistance.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body><Shell>{children}</Shell></body>
    </html>
  );
}
