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
bool eStopEngaged = false;
long currentSteps = 0;
String rxBuffer = "";

void handleCommandLine(const String& raw) {
  String line = raw;
  line.trim();
  if (line.length() == 0) return;

  if (line.indexOf("\"estop\"") >= 0) {
    eStopEngaged = true;
    // TODO: Disable stepper/motor driver enable pin here
    Serial.println("ACK: ESTOP");
    return;
  }

  if (line.indexOf("\"calibrate\"") >= 0) {
    eStopEngaged = false;
    currentSteps = 0;
    // TODO: Re-enable driver and zero step counter
    Serial.println("ACK: CAL_OK");
    return;
  }

  if (line.indexOf("\"jog\"") >= 0) {
    if (eStopEngaged) {
      Serial.println("ERR: ESTOP_ACTIVE");
      return;
    }

    bool isRev = line.indexOf("\"rev\"") >= 0;
    int steps = 200;
    int stepsIdx = line.indexOf("\"steps\":");
    if (stepsIdx >= 0) {
      steps = line.substring(stepsIdx + 8).toInt();
    }

    currentSteps += isRev ? -steps : steps;
    // TODO: Pulse STEP/DIR pins for `steps` in chosen direction
    Serial.printf("ACK: JOG_%s_%d POS=%ld\n", isRev ? "REV" : "FWD", steps, currentSteps);
    return;
  }

  Serial.printf("ACK: RAW %s\n", line.c_str());
}

void pollSerialCommands() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\n') {
      handleCommandLine(rxBuffer);
      rxBuffer = "";
    } else if (c != '\r') {
      rxBuffer += c;
    }
  }
}
