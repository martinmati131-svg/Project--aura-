import React from "react";
import Link from "next/link";

const telemetryFields = [
  {
    key: "temp",
    type: "float",
    unit: "°C",
    description: "SoC or microcontroller core temperature reading.",
  },
  {
    key: "v",
    type: "float",
    unit: "V",
    description: "Actuator or 5.0V nominal logic rail voltage.",
  },
  {
    key: "cpu",
    type: "int",
    unit: "%",
    description: "Host compute utilization percentage.",
  },
  {
    key: "inf_ms",
    type: "float",
    unit: "ms",
    description: "Per-frame edge inference latency.",
  },
  {
    key: "dist",
    type: "float",
    unit: "cm",
    description: "Forward proximity sensor (LiDAR / ultrasonic) distance.",
  },
];

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Top Navigation Bar */}
      <header className="border-b border-slate-800 bg-slate-950/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="font-mono text-xs uppercase tracking-widest text-slate-400 transition hover:text-emerald-400"
            >
              ← Aura Home
            </Link>
            <span className="text-slate-700">/</span>
            <h1 className="font-mono text-sm font-bold uppercase tracking-wider text-white">
              Documentation
            </h1>
          </div>

          <Link
            href="/dashboard"
            className="rounded-lg bg-emerald-600 px-3.5 py-2 font-mono text-xs font-semibold text-white transition hover:bg-emerald-500"
          >
            OPEN CONSOLE →
          </Link>
        </div>
      </header>

      {/* Main Content Layout */}
      <div className="mx-auto grid max-w-6xl grid-cols-1 gap-10 px-6 py-10 lg:grid-cols-4">
        {/* Sidebar Navigation */}
        <aside className="space-y-2 lg:col-span-1">
          <p className="font-mono text-xs font-semibold uppercase tracking-wider text-slate-500">
            Contents
          </p>
          <nav className="flex flex-col space-y-1.5 font-mono text-xs">
            <a
              href="#architecture"
              className="rounded-lg px-3 py-2 text-slate-300 transition hover:bg-slate-900 hover:text-emerald-400"
            >
              1. System Architecture
            </a>
            <a
              href="#quickstart"
              className="rounded-lg px-3 py-2 text-slate-300 transition hover:bg-slate-900 hover:text-emerald-400"
            >
              2. Bridge Quick Start
            </a>
            <a
              href="#schema"
              className="rounded-lg px-3 py-2 text-slate-300 transition hover:bg-slate-900 hover:text-emerald-400"
            >
              3. JSON Telemetry Schema
            </a>
            <a
              href="#firmware"
              className="rounded-lg px-3 py-2 text-slate-300 transition hover:bg-slate-900 hover:text-emerald-400"
            >
              4. Microcontroller Setup
            </a>
          </nav>
        </aside>

        {/* Documentation Body */}
        <main className="space-y-12 lg:col-span-3">
          {/* Section 1: Architecture */}
          <section id="architecture" className="space-y-4">
            <span className="inline-block rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 font-mono text-xs text-emerald-400">
              AURA INTELLIGENCE STACK
            </span>
            <h2 className="text-3xl font-bold tracking-tight text-white">
              Edge-to-Console Telemetry Pipeline
            </h2>
            <p className="text-sm leading-relaxed text-slate-300">
              Aura Intelligence bridges microcontroller hardware nodes and lightweight Linux hosts directly to a browser-based telemetry dashboard. Sensor packets can be streamed either directly via the{" "}
              <code className="rounded bg-slate-900 px-1.5 py-0.5 font-mono text-xs text-emerald-300">
                Web Serial API
              </code>{" "}
              on desktop Chromium browsers or through the{" "}
              <code className="rounded bg-slate-900 px-1.5 py-0.5 font-mono text-xs text-sky-300">
                read_telemetry.py
              </code>{" "}
              Server-Sent Events (SSE) bridge for mobile and containerized Linux environments.
            </p>
          </section>

          {/* Section 2: Bridge Quick Start */}
          <section id="quickstart" className="space-y-4">
            <h3 className="font-mono text-lg font-semibold text-white">
              2. Bridge Quick Start
            </h3>
            <p className="text-sm text-slate-300">
              Launch the Python SSE bridge in simulation mode to test the frontend without physical hardware attached, or bind directly to a USB serial device:
            </p>
            <pre className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/80 p-4 font-mono text-xs leading-relaxed text-emerald-400">
{`# Run with synthetic 2Hz sensor packets (no hardware required)
python3 read_telemetry.py --simulate

# Bind to a physical UART / USB serial device
python3 read_telemetry.py --port /dev/ttyUSB0 --baud 115200 --http-port 8000`}
            </pre>
            <p className="text-xs text-slate-400">
              Once running, open the{" "}
              <Link href="/dashboard" className="text-sky-400 underline hover:text-sky-300">
                Telemetry Console
              </Link>{" "}
              and click <strong className="text-slate-200">CONNECT BRIDGE</strong> to subscribe to{" "}
              <code className="font-mono text-slate-300">http://localhost:8000/stream</code>.
            </p>
          </section>

          {/* Section 3: JSON Telemetry Schema */}
          <section id="schema" className="space-y-4">
            <h3 className="font-mono text-lg font-semibold text-white">
              3. JSON Telemetry Schema
            </h3>
            <p className="text-sm text-slate-300">
              Each UART frame or SSE event expects a single-line JSON object containing any subset of the following keys:
            </p>

            <div className="overflow-hidden rounded-xl border border-slate-800">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-800 bg-slate-900 font-mono uppercase text-slate-400">
                  <tr>
                    <th className="px-4 py-3">Key</th>
                    <th className="px-4 py-3">Type</th>
                    <th className="px-4 py-3">Unit</th>
                    <th className="px-4 py-3">Description</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80 bg-slate-950/60">
                  {telemetryFields.map((field) => (
                    <tr key={field.key}>
                      <td className="px-4 py-3 font-mono font-semibold text-emerald-400">
                        {field.key}
                      </td>
                      <td className="px-4 py-3 font-mono text-slate-300">{field.type}</td>
                      <td className="px-4 py-3 font-mono text-amber-300">{field.unit}</td>
                      <td className="px-4 py-3 text-slate-300">{field.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {/* Section 4: Firmware Output */}
          <section id="firmware" className="space-y-4">
            <h3 className="font-mono text-lg font-semibold text-white">
              4. Microcontroller Firmware Snippet
            </h3>
            <p className="text-sm text-slate-300">
              Configure your ESP32 or Arduino node at <code className="font-mono text-slate-200">115200</code> baud to emit newline-delimited JSON frames:
            </p>
            <pre className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/80 p-4 font-mono text-xs leading-relaxed text-sky-300">
{`void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.printf(
    "{\\"temp\\":%.1f,\\"v\\":%.2f,\\"cpu\\":%d,\\"inf_ms\\":%.1f,\\"dist\\":%.1f}\\n",
    44.5, 5.06, 39, 13.4, 98.2
  );
  delay(500);
}`}
            </pre>
          </section>
        </main>
      </div>
    </div>
  );
}
