from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# CONFIGURATION
LEAD_SHEET_ID = "YOUR_SPREADSHEET_ID_HERE"  # Found in your Sheet's URL
SERVICE_ACCOUNT_FILE = 'drive_creds.json'  # Same key we used for Drive

def log_new_lead(phone_number, name="Prospective Client", status="New Lead"):
    """Appends a new lead row to the Google Sheet."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=creds)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = [[timestamp, phone_number, name, status, "Brochure Dispatched"]]
    body = {'values': values}
    
    result = service.spreadsheets().values().append(
        spreadsheetId=LEAD_SHEET_ID,
        range="Sheet1!A1",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    
    print(f"📈 [LEAD] Successfully logged: {phone_number}")
