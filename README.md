# AURA — Edge-AI & Robotics Telemetry Control Plane

AURA is an Edge-AI and robotics telemetry interface and hardware bridge built for low-latency sensor observability, real-time actuator control, and field deployment workflows. It pairs a **Next.js 16 (App Router) + Tailwind CSS** operator console with a lightweight **Python Serial-to-HTTP/SSE Bridge** (`read_telemetry.py`).

---

## Architecture Overview

```text
+----------------------+      USB / UART       +-------------------------+
|  Edge Controller /   | <-------------------> |   read_telemetry.py     |
|  Actuator Firmware   |   115200 baud JSON    |   (Python HTTP + SSE)   |
+----------------------+                       +------------+------------+
                                                            |
                                  GET  /stream    (SSE)     |
                                  GET  /telemetry (JSON)    |  Port 8000
                                  POST /command   (JSON)    |
                                                            v
                                               +-------------------------+
                                               |     aura-frontend       |
                                               |   Next.js 16 + Tailwind |
                                               |  /  | /dashboard | /docs|
                                               +-------------------------+
Core Features & Routes
Purpose Key Capabilities
/ Engineering & Release Feed Tag-filtered activity stream (ALL, ROBOTICS, EDGE-AI, PYTHON, RELEASE) with client-side post creation persisted in localStorage (aura_custom_posts_v1).
/dashboard Live Telemetry & Command Console Real-time Server-Sent Events (/stream) with automatic /telemetry polling fallback, live sensor readouts, and bi-directional motor/safety controls (Calibrate, Jog, E-Stop).
/docs System & Wire Protocol Reference Embedded architectural overview, endpoint specifications, and hardware bridge quickstart.

Prerequisites
​Node.js 20+ and npm (or pnpm)
​Python 3.10+ with pyserial (pip install pyserial)
​(Optional) Microcontroller or actuator driver attached via /dev/ttyUSB0 or /dev/ttyACM0
Quick Start
​1. Start the Telemetry Bridge (read_telemetry.py)
​With physical hardware:
python3 read_telemetry.py --port /dev/ttyUSB0 --baud 115200 --http-port 8000
Without hardware (Synthetic Simulation Mode):
python3 read_telemetry.py --simulate --http-port 8000
2. Start the Frontend (aura-frontend)
npm install
npm run dev
Open http://localhost:3000/dashboard to view live telemetry packets and dispatch actuator commands.
​Bridge HTTP & SSE Wire Protocol
​GET /telemetry
​Returns the latest telemetry snapshot as JSON:
{
  "temp": 44.2,
  "v": 5.08,
  "cpu": 38,
  "inf_ms": 14.2,
  "dist": 112.5,
  "estop": false,
  "pos_steps": 0
}
GET /stream
​Streams continuous text/event-stream (SSE) frames in the format:
data: {"temp": 44.8, "v": 5.10, "cpu": 39, "inf_ms": 16.2, "dist": 106.0, "estop": false, "pos_steps": 0}
POST /command
​Dispatches JSON commands to the serial controller and returns an acknowledgement ({"ok": true, "ack": "..."}):
Action JSON Payload Expected Ack
Zero / Calibrate {"cmd": "calibrate"} ACK: CAL_ZEROED
Jog Actuator {"cmd": "jog", "dir": "fwd", "steps": 25} ACK: JOG fwd 25 -> pos=25
Emergency Stop {"cmd": "estop"} ACK: ESTOP_LOCKED
Smoke-Testing the Bridge
curl -s http://localhost:8000/telemetry
curl -N -s http://localhost:8000/stream | head -n 5
curl -s -X POST http://localhost:8000/command -H "Content-Type: application/json" -d '{"cmd":"calibrate"}'
curl -s -X POST http://localhost:8000/command -H "Content-Type: application/json" -d '{"cmd":"jog","dir":"fwd","steps":25}'
curl -s -X POST http://localhost:8000/command -H "Content-Type: application/json" -d '{"cmd":"estop"}'
Production Build

npm run build
npm run start

