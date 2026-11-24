import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Aura Intelligence — Edge-AI & Telemetry",
  description: "Real-time hardware telemetry and bi-directional serial command console.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 antialiased">{children}</body>
    </html>
  );
}
