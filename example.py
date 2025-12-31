import ngrok
import os
from google import generativeai as genai
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Setup Gemini (Aura's Brain)
# Set your key as an environment variable first!
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Define the Webhook Logic
class AuraHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # This handles the Meta Webhook verification handshake
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Aura Sentinel is Online")

# 3. Launch Tunnel & Server
server = HTTPServer(("localhost", 8080), AuraHandler)
# authtoken is found in your ngrok dashboard
listener = ngrok.forward(8080, authtoken="YOUR_NGROK_AUTHTOKEN")

print(f"🚀 Aura is LIVE at: {listener.url()}")
server.serve_forever()
