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
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Aura's content generation for Google Portfolio
def generate_aura_post():
    prompt = "Create a professional business post for Aura Intelligence about launching our new AI Sentinel on WhatsApp. Keep it under 300 characters for Google Maps."
    response = model.generate_content(prompt)
    return response.text

# Note: This requires enabling the Google My Business API in your Google Cloud Console
def post_to_google_portfolio(content):
    # Your 20-digit ID is used in the account path
    account_id = "11942169205531151033" 
    # Use your Google Cloud credentials here
    print(f"📡 Posting to Aura Portfolio: {content}")
    # Logic to send to mybusiness.googleapis.com

