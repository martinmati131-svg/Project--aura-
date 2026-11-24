import argparse
import json
import random
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    import serial
except ImportError:
    serial = None

state_lock = threading.Lock()
estop_engaged = False
position_steps = 0
serial_handle = None

latest_packet = {
    "temp": 44.2,
    "v": 5.08,
    "cpu": 38,
    "inf_ms": 14.2,
    "dist": 112.5,
    "estop": False,
    "pos_steps": 0,
}


def dispatch_command(raw_line: str) -> dict:
    global estop_engaged, position_steps

    line = raw_line.strip()
    if not line:
        return {"ok": False, "error": "Empty command"}

    with state_lock:
        ser = serial_handle
        if ser is not None and ser.is_open:
            ser.write((line + "\n").encode("utf-8"))
            ser.flush()

        try:
            msg = json.loads(line)
            cmd = msg.get("cmd")
        except json.JSONDecodeError:
            return {"ok": True, "ack": f"RAW_SENT: {line}"}

        if cmd == "estop":
            estop_engaged = True
            latest_packet["estop"] = True
            return {"ok": True, "ack": "ACK: ESTOP_LOCKED"}

        if cmd == "calibrate":
            estop_engaged = False
            position_steps = 0
            latest_packet["estop"] = False
            latest_packet["pos_steps"] = 0
            return {"ok": True, "ack": "ACK: CAL_ZEROED"}

        if cmd == "jog":
            if estop_engaged:
                return {"ok": False, "ack": "ERR: ESTOP_ACTIVE"}
            direction = msg.get("dir", "fwd")
            steps = abs(int(msg.get("steps", 0)))
            delta = steps if direction == "fwd" else -steps
            position_steps += delta
            latest_packet["pos_steps"] = position_steps
            return {"ok": True, "ack": f"ACK: JOG {direction} {steps} -> pos={position_steps}"}

        return {"ok": True, "ack": f"ACK: CMD_{cmd or 'UNKNOWN'}"}


def sensor_worker(port: str, baud: int, simulate: bool):
    global serial_handle

    if not simulate:
        if serial is None:
            raise RuntimeError("pyserial not installed. Run with --simulate or install pyserial.")
        ser = serial.Serial(port, baud, timeout=1)
        with state_lock:
            serial_handle = ser
        print(f"[SERIAL] Listening on {port} @ {baud} baud", flush=True)
    else:
        ser = None
        print("[SIM] Emitting synthetic telemetry packets...", flush=True)

    while True:
        if simulate:
            packet = {
                "temp": round(43.0 + random.uniform(0, 4.5), 1),
                "v": round(5.02 + random.uniform(0, 0.14), 2),
                "cpu": random.randint(32, 60),
                "inf_ms": round(12.5 + random.uniform(0, 5.2), 1),
                "dist": round(80.0 + random.uniform(-25.0, 45.0), 1),
            }
            with state_lock:
                latest_packet.update(packet)
                snapshot = dict(latest_packet)
            print(json.dumps(snapshot), flush=True)
            time.sleep(0.5)
        else:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue
            try:
                data = json.loads(raw)
                with state_lock:
                    latest_packet.update({
                        "temp": float(data.get("temp", latest_packet["temp"])),
                        "v": float(data.get("v", latest_packet["v"])),
                        "cpu": int(data.get("cpu", latest_packet["cpu"])),
                        "inf_ms": float(data.get("inf_ms", latest_packet["inf_ms"])),
                        "dist": float(data.get("dist", latest_packet["dist"])),
                    })
                    snapshot = dict(latest_packet)
                print(json.dumps(snapshot), flush=True)
            except json.JSONDecodeError:
                print(f"[RAW] {raw}", flush=True)


class TelemetryHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/stream":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                while True:
                    with state_lock:
                        payload = json.dumps(latest_packet)
                    self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(0.5)
            except (BrokenPipeError, ConnectionResetError):
                pass
        elif self.path == "/telemetry":
            with state_lock:
                payload = json.dumps(latest_packet).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/command":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8", errors="ignore")
            result = dispatch_command(body)
            payload = json.dumps(result).encode("utf-8")
            self.send_response(200 if result.get("ok") else 409)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aura Telemetry Bridge")
    parser.add_argument("--port", default="/dev/ttyUSB0", help="Serial device path")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--http-port", type=int, default=8000, help="HTTP stream port")
    parser.add_argument("--simulate", action="store_true", help="Emit synthetic JSON telemetry")
    args = parser.parse_args()

    t = threading.Thread(
        target=sensor_worker,
        args=(args.port, args.baud, args.simulate),
        daemon=True,
    )
    t.start()

    server = ThreadingHTTPServer(("0.0.0.0", args.http_port), TelemetryHandler)
    print(f"[HTTP] SSE stream ready at http://localhost:{args.http_port}/stream", flush=True)
    server.serve_forever()
