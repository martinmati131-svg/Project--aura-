# client/calendar_client.py
# This module handles all Google Calendar authentication and fetching

import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file 'token.json'.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'client/credentials.json'
TOKEN_FILE = 'client/token.json'

def get_calendar_service():
    """Authenticates the user and returns a Google Calendar service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

def get_current_calendar_state(service):
    """
    Checks the calendar for an event happening *right now*.
    Returns 'in_meeting' or 'free'.
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    try:
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=1,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])

        if not events:
            return 'free' # No upcoming events

        # Check if the first event is happening right now
        event = events[0]
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        # Convert to datetime objects for comparison
        start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
        now_dt = datetime.datetime.now(datetime.timezone.utc)

        if start_dt <= now_dt < end_dt:
            return 'in_meeting' # An event is currently in progress
        else:
            return 'free' # The next event hasn't started yet

    except Exception as e:
        print(f"Error fetching calendar: {e}")
        return 'unknown'

if __name__ == '__main__':
    # This part is just for testing
    print("Attempting to connect to Google Calendar...")
    service = get_calendar_service()
    print("✅ Service connected.")
    state = get_current_calendar_state(service)
    print(f"Your current calendar state is: {state.upper()}")
