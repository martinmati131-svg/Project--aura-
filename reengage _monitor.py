from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# CONFIGURATION
LEAD_SHEET_ID = "YOUR_SPREADSHEET_ID_HERE"
ADMIN_PHONE = "YOUR_PERSONAL_PHONE_NUMBER" # Where you want the alerts
SERVICE_ACCOUNT_FILE = 'drive_creds.json'

def check_stagnant_leads():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=creds)
    
    # Read the Lead Sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=LEAD_SHEET_ID, range="Sheet1!A2:E100"
    ).execute()
    rows = result.get('values', [])

    for row in rows:
        timestamp_str, phone, name, status, notes = row
        lead_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        
        # If lead is > 24 hours old and still marked as 'New Lead'
        if status == "New Lead" and datetime.now() > lead_time + timedelta(hours=24):
            trigger_admin_alert(name, phone)

def trigger_admin_alert(lead_name, lead_phone):
    """Sends a WhatsApp alert to the Admin via Meta API."""
    # (Use your existing send_whatsapp_message logic here)
    message = f"🚨 AURA ALERT: Lead '{lead_name}' ({lead_phone}) has been unaddressed for 24 hours. Follow up now!"
    print(message) 
