"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";

interface TelemetryPacket {
  timestamp?: string;
  motor_temp?: number;
  current_ma?: number;
  position_deg?: number;
  pos_steps?: number;
  estop?: boolean;
  rpm?: number;
  status?: string;
  [key: string]: unknown;
}

export default function DashboardPage() {
  const [bridgeUrl, setBridgeUrl] = useState("http://localhost:8000");
  const [connectionMode, setConnectionMode] = useState<"sse" | "polling" | "offline">("offline");
  const [telemetry, setTelemetry] = useState<TelemetryPacket | null>(null);
  const [rawLogs, setRawLogs] = useState<string[]>([]);
  const [commandStatus, setCommandStatus] = useState<string>("Ready");
  const [jogSteps, setJogSteps] = useState<number>(50);
  const [busy, setBusy] = useState<boolean>(false);
  const pollTimerRef = useRef<NodeJS.Timeout | null>(null);

  const appendLog = (entry: string) => {
    const stamp = new Date().toLocaleTimeString();
    setRawLogs((prev) => [`[${stamp}] ${entry}`, ...prev.slice(0, 29)]);
  };

  useEffect(() => {
    let eventSource: EventSource | null = null;
    let active = true;

    const startPolling = () => {
      if (!active) return;
      setConnectionMode("polling");
      appendLog("SSE unavailable; falling back to /telemetry polling...");

      const fetchSnapshot = async () => {
        try {
          const res = await fetch(`${bridgeUrl}/telemetry`, { cache: "no-store" });
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          const data: TelemetryPacket = await res.json();
          if (!active) return;
          setTelemetry(data);
          setConnectionMode("polling");
        } catch {
          if (!active) return;
          setConnectionMode("offline");
        }
      };

      fetchSnapshot();
      pollTimerRef.current = setInterval(fetchSnapshot, 1500);
    };

    try {
      eventSource = new EventSource(`${bridgeUrl}/stream`);

      eventSource.onopen = () => {
        if (!active) return;
        setConnectionMode("sse");
        appendLog(`Connected to live SSE stream at ${bridgeUrl}/stream`);
      };

      eventSource.onmessage = (event) => {
        if (!active) return;
        try {
          const parsed: TelemetryPacket = JSON.parse(event.data);
          setTelemetry(parsed);
          setConnectionMode("sse");
        } catch {
          appendLog(`Stream frame: ${event.data}`);
        }
      };

      eventSource.onerror = () => {
        if (!active) return;
        eventSource?.close();
        if (!pollTimerRef.current) {
          startPolling();
        }
      };
    } catch {
      startPolling();
    }

    return () => {
      active = false;
      eventSource?.close();
      if (pollTimerRef.current) {
        clearInterval(pollTimerRef.current);
        pollTimerRef.current = null;
      }
    };
  }, [bridgeUrl]);

  const sendCommand = async (payload: Record<string, unknown>, label: string) => {
    setBusy(true);
    setCommandStatus(`Sending ${label}...`);
    appendLog(`TX -> ${JSON.stringify(payload)}`);

    try {
      const res = await fetch(`${bridgeUrl}/command`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const text = await res.text();
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${text}`);
      }

      setCommandStatus(`${label} acknowledged`);
      appendLog(`RX <- ${text || "OK"}`);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Command failed";
      setCommandStatus(`Error: ${msg}`);
      appendLog(`ERR <- ${msg}`);
    } finally {
      setBusy(false);
    }
  };

  const safeSteps = Math.max(1, Math.abs(Number(jogSteps) || 0));

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-3">
              <Link href="/" className="text-sm text-cyan-400 hover:underline">
                ← Home
              </Link>
              <span className="text-slate-600">/</span>
              <span className="text-xs uppercase tracking-widest text-slate-400">
                Aura Edge Telemetry
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold mt-2">
              Telemetry &amp; Command Console
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <input
              type="text"
              value={bridgeUrl}
              onChange={(e) => setBridgeUrl(e.target.value)}
              aria-label="Bridge URL"
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
            />
            <span
              className={`px-3 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wide ${
                connectionMode === "sse"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                  : connectionMode === "polling"
                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                  : "bg-rose-500/20 text-rose-300 border border-rose-500/40"
              }`}
            >
              {connectionMode === "sse"
                ? "Live SSE"
                : connectionMode === "polling"
                ? "Polling"
                : "Offline"}
            </span>
          </div>
        </header>

        {/* Live Telemetry Readouts */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
            <p className="text-xs uppercase tracking-wider text-slate-400">E-STOP / State</p>
            <p className="text-2xl font-mono font-bold text-cyan-400 mt-2">
              {telemetry?.estop ? "ESTOP LOCKED" : String(telemetry?.status ?? "STANDBY")}
            </p>
          </div>
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
            <p className="text-xs uppercase tracking-wider text-slate-400">Position (Steps / Deg)</p>
            <p className="text-2xl font-mono font-bold text-slate-100 mt-2">
              {telemetry?.pos_steps !== undefined
                ? `${telemetry.pos_steps} steps`
                : telemetry?.position_deg !== undefined
                ? `${telemetry.position_deg}°`
                : "--"}
            </p>
          </div>
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
            <p className="text-xs uppercase tracking-wider text-slate-400">Current Draw</p>
            <p className="text-2xl font-mono font-bold text-slate-100 mt-2">
              {telemetry?.current_ma !== undefined ? `${telemetry.current_ma} mA` : "--"}
            </p>
          </div>
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
            <p className="text-xs uppercase tracking-wider text-slate-400">Actuator Temp</p>
            <p className="text-2xl font-mono font-bold text-slate-100 mt-2">
              {telemetry?.motor_temp !== undefined ? `${telemetry.motor_temp} °C` : "--"}
            </p>
          </div>
        </section>

        {/* Command Controls */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Actuator Controls</h2>
              <span className="text-xs font-mono text-slate-400">{commandStatus}</span>
            </div>

            {/* Emergency Stop & Calibration */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button
                type="button"
                disabled={busy}
                onClick={() => sendCommand({ cmd: "estop" }, "E-STOP")}
                className="bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white font-bold py-3 px-4 rounded-lg tracking-wider uppercase transition"
              >
                E-STOP
              </button>
              <button
                type="button"
                disabled={busy}
                onClick={() => sendCommand({ cmd: "calibrate" }, "Calibrate")}
                className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white font-semibold py-3 px-4 rounded-lg transition"
              >
                Zero-Point Calibrate
              </button>
            </div>

            {/* Motor Jog */}
            <div className="border-t border-slate-800 pt-4 space-y-3">
              <p className="text-sm font-medium text-slate-300">Manual Motor Jog</p>
              <div>
                <label className="block text-xs text-slate-400 mb-1">Steps</label>
                <input
                  type="number"
                  min={1}
                  value={jogSteps}
                  onChange={(e) => setJogSteps(Number(e.target.value))}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono"
                />
              </div>

              <div className="grid grid-cols-2 gap-3 pt-1">
                <button
                  type="button"
                  disabled={busy}
                  onClick={() =>
                    sendCommand({ cmd: "jog", dir: "rev", steps: safeSteps }, `Jog rev ${safeSteps}`)
                  }
                  className="bg-slate-800 hover:bg-slate-700 disabled:opacity-50 py-2.5 px-4 rounded-lg text-sm font-mono transition"
                >
                  ← Rev ({safeSteps})
                </button>
                <button
                  type="button"
                  disabled={busy}
                  onClick={() =>
                    sendCommand({ cmd: "jog", dir: "fwd", steps: safeSteps }, `Jog fwd ${safeSteps}`)
                  }
                  className="bg-slate-800 hover:bg-slate-700 disabled:opacity-50 py-2.5 px-4 rounded-lg text-sm font-mono transition"
                >
                  Fwd ({safeSteps}) →
                </button>
              </div>
            </div>
          </div>

          {/* Raw Telemetry & Command Log */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 flex flex-col justify-between space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Serial Bridge Stream Log</h2>
              <button
                type="button"
                onClick={() => setRawLogs([])}
                className="text-xs text-slate-400 hover:text-slate-200"
              >
                Clear
              </button>
            </div>

            <pre className="bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs font-mono text-emerald-300 h-56 overflow-y-auto whitespace-pre-wrap">
              {telemetry
                ? `Latest Packet:\n${JSON.stringify(telemetry, null, 2)}\n\n`
                : "Waiting for telemetry from read_telemetry.py...\n\n"}
              {rawLogs.join("\n")}
            </pre>
          </div>
        </section>
      </div>
    </main>
  );
}
