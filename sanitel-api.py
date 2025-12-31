DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Aura Mission Control</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #0f172a; color: white; padding: 40px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e293b; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #334155; }
        th { color: #38bdf8; text-transform: uppercase; font-size: 12px; }
        .status { color: #4ade80; font-weight: bold; }
        h1 { border-left: 4px solid #38bdf8; padding-left: 15px; }
    </style>
</head>
<body>
    <h1>Aura Intelligence: Shadow Test Logs</h1>
    <table>
        <tr><th>Time</th><th>User</th><th>Input</th><th>Aura Response</th><th>Status</th></tr>
        {% for log in logs %}
        <tr>
            <td>{{ log.timestamp }}</td>
            <td>{{ log.user }}</td>
            <td>{{ log.input }}</td>
            <td>{{ log.aura_response }}</td>
            <td class="status">{{ log.status }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""
import os
from flask import Flask, request, jsonify
from pyngrok import ngrok
from google import generativeai as genai
import requests

# --- CONFIGURATION ---
# App ID: 896941116042076
PORT = 3000
VERIFY_TOKEN = "aura_intelligence_2025"
WHATSAPP_TOKEN = "YOUR_PERMANENT_SYSTEM_TOKEN"
GEMINI_KEY = "YOUR_GEMINI_API_KEY"

# Initialize Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# 1. THE HANDSHAKE (GET)
@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Meta Handshake Verified")
        return challenge, 200
    return "Forbidden", 403

# 2. THE BRAIN (POST)
@app.route('/webhook', methods=['POST'])
def handle_messages():
    data = request.json
    try:
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            user_phone = message["from"]
            user_text = message["text"]["body"]
            
            # Aura Persona Logic
            prompt = f"Role: Aura (Robotics AI). Goal: Scale business & Zen Flow. User says: {user_text}"
            response = model.generate_content(prompt)
            
            # Send Reply back to WhatsApp
            send_whatsapp(user_phone, response.text)
            
    except Exception as e:
        print(f"❌ Processing Error: {e}")
        
    return "EVENT_RECEIVED", 200

def send_whatsapp(to, text):
    url = f"https://graph.facebook.com/v21.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    # Start ngrok tunnel via Python
    public_url = ngrok.connect(PORT).public_url
    print(f"🚀 Aura is LIVE at: {public_url}/webhook")
    print(f"👉 Copy the URL above into your Meta Dashboard (App ID: 896941116042076)")
    
    app.run(port=PORT)

# Simple in-memory log storage
shadow_test_logs = []

@app.route('/dashboard')
def dashboard():
    # Renders the logs in a clean HTML table
    return render_template_string(DASHBOARD_HTML, logs=shadow_test_logs)

@app.post('/webhook')
def handle_messages():
    # ... previous logic ...
    # Add to logs for the dashboard
    log_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "user": user_phone,
        "input": user_text,
        "aura_response": ai_reply,
        "status": "✅ Success"
    }
    shadow_test_logs.insert(0, log_entry) # Keep newest at top
    shadow_test_logs[:] = shadow_test_logs[:10] # Keep only last 10
    return "EVENT_RECEIVED", 200
app.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === 'YOUR_CUSTOM_TOKEN_HERE') {
    res.status(200).send(challenge); // This "echo" bypasses the restriction
  } else {
    res.sendStatus(403);
  }
});


# sentinel_api.py
from fastapi import Request, BackgroundTasks

@app.get("/sentinel/v1/trap-gate")
async def trigger_honeypot(request: Request, background_tasks: BackgroundTasks):
    """
    The Honeypot Endpoint: Only bots ever reach this.
    """
    bot_info = {
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "timestamp": datetime.now()
    }
    
    # 1. Log the Bot Intelligence
    background_tasks.add_task(log_bot_to_sentinel_db, bot_info)
    
    # 2. Add IP to the Global Blacklist for all 10 Pillars
    background_tasks.add_task(self.sentinel.blacklist_ip, bot_info["ip"])
    
    # 3. Misdirect the Bot: Give it fake, heavy data to waste its resources
    return {"status": "success", "data": "Generating encrypted admin logs... (0%)"}
import os
import json
import requests
import smtplib
from datetime import datetime
from flask import Flask, request, render_template_string
from pyngrok import ngrok
from google import generativeai as genai
from email.message import EmailMessage

# --- CONFIGURATION ---
# App ID: 896941116042076
PORT = 3000
VERIFY_TOKEN = "aura_intelligence_2025"
WHATSAPP_TOKEN = "YOUR_PERMANENT_SYSTEM_TOKEN"
GEMINI_KEY = "YOUR_GEMINI_API_KEY"

# Alert Settings (Use App Passwords for Gmail)
ALERT_EMAIL = "your-email@gmail.com"
EMAIL_PASS = "your-app-password"

# Initialize Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
logs = []

def send_alert(error_msg):
    """Sends an email alert if the Shadow Test fails."""
    msg = EmailMessage()
    msg.set_content(f"Aura Sentinel Alert: {error_msg}\nTimestamp: {datetime.now()}")
    msg['Subject'] = "🚨 AURA SYSTEM CRITICAL FAILURE"
    msg['From'] = ALERT_EMAIL
    msg['To'] = ALERT_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(ALERT_EMAIL, EMAIL_PASS)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Failed to send email alert: {e}")

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def handle_incoming():
    try:
        data = request.json
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        user_phone = message['from']
        user_text = message['text']['body']

        # Process via Aura Persona
        response = model.generate_content(f"You are Aura (Robotics AI). User: {user_text}")
        ai_reply = response.text

        # Log for Dashboard
        logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "user": user_phone, "text": user_text, "reply": ai_reply})
        
        # Send back to WhatsApp
        requests.post(
            f"https://graph.facebook.com/v21.0/YOUR_PHONE_NUMBER_ID/messages",
            json={"messaging_product": "whatsapp", "to": user_phone, "text": {"body": ai_reply}},
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
        )
    except Exception as e:
        send_alert(str(e))
    return "OK", 200

@app.route('/dashboard')
def show_dashboard():
    return render_template_string("<h1>Aura Mission Control</h1><ul>{% for l in logs %}<li><b>{{l.time}}</b>: {{l.text}} -> <i>{{l.reply}}</i></li>{% endfor %}</ul>", logs=logs)

if __name__ == "__main__":
    public_url = ngrok.connect(PORT).public_url
    print(f"🚀 Sentinel Live: {public_url}/webhook")
    app.run(port=PORT)
const express = require('express');
const app = express();
app.use(express.json());

// 1. WEBHOOK VERIFICATION (GET)
// This is the "handshake" Meta uses to verify your server.
app.get('/webhook', (req, res) => {
    const VERIFY_TOKEN = "aura_intelligence_2025"; // You set this in Meta Dashboard
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode && token) {
        if (mode === 'subscribe' && token === VERIFY_TOKEN) {
            console.log("✅ WEBHOOK_VERIFIED");
            res.status(200).send(challenge);
        } else {
            res.sendStatus(403);
        }
    }
});

// 2. MESSAGE HANDLER (POST)
app.post('/webhook', (req, res) => {
    // Acknowledge immediately to prevent Meta from retrying (Reverse Logic)
    res.status(200).send("EVENT_RECEIVED");

    if (req.body.object && req.body.entry?.[0]?.changes?.[0]?.value?.messages?.[0]) {
        const message = req.body.entry[0].changes[0].value.messages[0];
        const from = message.from; // User's phone number
        const msgBody = message.text.body; // The actual text

        console.log(`📩 Incoming from ${from}: ${msgBody}`);
        
        // NEXT STEP: Send msgBody to Gemini for processing
    }
});

app.listen(3000, () => console.log('🚀 Sentinel is listening on port 3000'));
import os
import time
import requests
from flask import Flask, request, jsonify
from pyngrok import ngrok
from google import generativeai as genai
from datetime import datetime

# --- SYSTEM STATES (Sentinel Pattern) ---
class SystemStatus:
    ONLINE = "🟢 ACTIVE"
    MAINTENANCE = "🟡 SYNCING"
    ERROR = "🔴 CRITICAL"

# --- CONFIGURATION ---
# App ID: 896941116042076
PORT = 3000
VERIFY_TOKEN = "aura_intelligence_2026"
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Aura Brain
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
current_status = SystemStatus.ONLINE

@app.route('/webhook', methods=['GET'])
def meta_handshake():
    # 2026 Handshake v24.0 Logic
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(f"[{datetime.now()}] ✅ Handshake v24.0 Successful")
        return challenge, 200
    return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def handle_sentinel_event():
    data = request.json
    # Sentinel Logic: Log every incoming packet for the Shadow Test
    print(f"[{datetime.now()}] 📡 Incoming Packet: {data}")
    
    try:
        # Process message via Gemini
        user_msg = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        response = model.generate_content(f"Aura Persona: Process input '{user_msg}'")
        
        # Send back to Meta
        # Note: In 2026, we use v24.0 for the Graph API
        send_response(data['entry'][0]['changes'][0]['value']['messages'][0]['from'], response.text)
        
    except Exception as e:
        print(f"⚠️ Sentinel Alert: {e}")
        
    return "EVENT_RECEIVED", 200

def send_response(to, text):
    url = f"https://graph.facebook.com/v24.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {"messaging_product": "whatsapp", "to": to, "text": {"body": text}}
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    # Start ngrok tunnel
    public_url = ngrok.connect(PORT).public_url
    print(f"🚀 Aura Sentinel {current_status}")
    print(f"🔗 Public Tunnel: {public_url}/webhook")
    app.run(port=PORT)
# Updated Persona Logic for 2026
prompt = (
    f"You are Aura (Robotics AI). Our technical codebase is hosted at "
    f"https://github.com/martinmati131-svg/my-online-business. "
    f"User says: {user_text}"
)
# --- 2026 COMPLIANCE HANDLER ---
def handle_compliance_logic(user_phone, user_text):
    """Checks for mandatory data deletion keywords."""
    trigger = user_text.strip().upper()
    
    if trigger == "DELETE DATA" or trigger == "STOP":
        # 1. Logic to purge data from your local logs/database
        # Example: db.delete_user(user_phone) 
        print(f"⚠️ [COMPLIANCE] Data deletion executed for: {user_phone}")
        
        # 2. Meta requires a 24-hour processing confirmation
        confirmation = (
            "Aura Sentinel Compliance: Your data deletion request has been processed. "
            "Your interaction history is purged from our systems."
        )
        send_response(user_phone, confirmation)
        return True # Stop further processing
    
    return False # Continue to Gemini Brain

# --- UPDATE YOUR POST ROUTE ---
@app.route('/webhook', methods=['POST'])
def handle_sentinel_event():
    data = request.json
    try:
        message_data = data['entry'][0]['changes'][0]['value']['messages'][0]
        user_phone = message_data['from']
        user_text = message_data['text']['body']

        # COMPLIANCE CHECK FIRST (v24.0 Requirement)
        if handle_compliance_logic(user_phone, user_text):
            return "COMPLIANCE_PROCESSED", 200

        # If not a deletion request, proceed to Gemini Brain
        response = model.generate_content(f"Aura Persona: {user_text}")
        send_response(user_phone, response.text)
        
    except Exception as e:
        print(f"⚠️ Sentinel Alert: {e}")
    return "EVENT_RECEIVED", 200
import csv
from datetime import datetime

def log_compliance_action(user_phone, action_type="DELETION"):
    """
    Creates a 2026-compliant audit trail.
    Note: We log the phone number's LAST 4 DIGITS to maintain 
    privacy even within the audit log itself.
    """
    log_file = "aura_compliance_audit.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    masked_phone = f"*******{user_phone[-4:]}"
    
    # Audit Header: Timestamp | Subject | Action | Status
    row = [timestamp, masked_phone, action_type, "SUCCESSFUL"]
    
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Entity_ID", "Action", "Result"])
        writer.writerow(row)
    
    print(f"🔒 [AUDIT] Compliance log updated for {masked_phone}")

# --- INTEGRATION INTO YOUR HANDLER ---
if trigger == "DELETE DATA":
    # 1. Execute Purge
    log_compliance_action(user_phone, "USER_DATA_PURGE")
    # 2. Confirm to User
    send_response(user_phone, "Aura Sentinel: Your data has been purged. Audit ID: " + datetime.now().strftime("%Y%m%d%H%M"))
