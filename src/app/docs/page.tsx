import Link from "next/link";

const endpoints = [
  {
    method: "GET",
    path: "/stream",
    description: "Server-Sent Events (SSE) stream pushing live JSON telemetry packets to /dashboard.",
  },
  {
    method: "GET",
    path: "/telemetry",
    description: "Latest snapshot JSON payload (latest_packet) used for polling or health checks.",
  },
  {
    method: "POST",
    path: "/command",
    description: "Dispatches JSON actuator commands via dispatch_command (estop, calibrate, jog).",
  },
];

const commandPayloads = [
  {
    action: "Emergency Stop",
    payload: '{ "cmd": "estop" }',
    behavior: "Sets estop_engaged = True and locks motor motion until calibrated.",
  },
  {
    action: "Zero-Point Calibration",
    payload: '{ "cmd": "calibrate" }',
    behavior: "Clears estop_engaged, zeroes position_steps to 0, and updates latest_packet.",
  },
  {
    action: "Manual Motor Jog",
    payload: '{ "cmd": "jog", "dir": "fwd", "steps": 50 }',
    behavior: "Moves step count in dir (fwd or rev) when E-STOP is not active.",
  },
];

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-10">
        {/* Top Navigation */}
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <nav className="flex items-center gap-4 font-mono text-xs text-slate-400">
              <Link href="/" className="hover:text-white transition">
                HOME
              </Link>
              <Link href="/dashboard" className="text-cyan-400 hover:text-cyan-300 transition">
                TELEMETRY
              </Link>
              <span className="text-white font-semibold">DOCS</span>
            </nav>
            <h1 className="text-2xl md:text-3xl font-bold mt-3">
              Aura Intelligence Architecture &amp; Bridge Docs
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Frontend console, Python serial/SSE telemetry bridge, and ML pipeline overview.
            </p>
          </div>

          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400 transition shrink-0"
          >
            Open Console →
          </Link>
        </header>

        {/* System Overview */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-2">
            <p className="text-xs font-mono uppercase tracking-wider text-cyan-400">
              Frontend App
            </p>
            <h2 className="text-lg font-semibold">Next.js App Router</h2>
            <p className="text-sm text-slate-300">
              Styled with Tailwind CSS, exposing the main feed (`/`), telemetry console (`/dashboard`),
              and system documentation (`/docs`).
            </p>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-2">
            <p className="text-xs font-mono uppercase tracking-wider text-cyan-400">
              Serial / HTTP Bridge
            </p>
            <h2 className="text-lg font-semibold font-mono">read_telemetry.py</h2>
            <p className="text-sm text-slate-300">
              Bridges serial hardware frames and HTTP/SSE endpoints (`http://localhost:8000`) with
              thread-safe state locking and CORS headers.
            </p>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-2">
            <p className="text-xs font-mono uppercase tracking-wider text-cyan-400">
              Model Pipeline
            </p>
            <h2 className="text-lg font-semibold font-mono">train_and_save.py</h2>
            <p className="text-sm text-slate-300">
              Trains and persists model artifacts for Aura Intelligence telemetry and predictive
              workflows alongside the frontend repo.
            </p>
          </div>
        </section>

        {/* HTTP / SSE Endpoints */}
        <section className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-xl font-semibold">Bridge Endpoints (`read_telemetry.py`)</h2>
          <div className="divide-y divide-slate-800">
            {endpoints.map((ep) => (
              <div key={ep.path} className="py-3 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
                <span className="font-mono text-xs px-2.5 py-1 rounded bg-slate-800 text-cyan-300 w-fit">
                  {ep.method} {ep.path}
                </span>
                <p className="text-sm text-slate-300">{ep.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Command Wire Format */}
        <section className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-xl font-semibold">Command Wire Payloads (`/command`)</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {commandPayloads.map((item) => (
              <div
                key={item.action}
                className="bg-slate-950 border border-slate-800 rounded-lg p-4 space-y-2"
              >
                <p className="text-sm font-semibold text-slate-100">{item.action}</p>
                <pre className="text-xs font-mono text-emerald-300 bg-slate-900/90 p-2.5 rounded overflow-x-auto">
                  {item.payload}
                </pre>
                <p className="text-xs text-slate-400">{item.behavior}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Local Run Workflow */}
        <section className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-3">
          <h2 className="text-xl font-semibold">Local Development Workflow</h2>
          <pre className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-xs font-mono text-slate-200 overflow-x-auto">
{`# 1. Start the Python serial/telemetry bridge
python3 read_telemetry.py

# 2. Run the Next.js frontend
npm run dev

# 3. Verify production build before pushing
npm run build`}
          </pre>
        </section>
      </div>
    </main>
  );
}
