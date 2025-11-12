# aura_platform_core.py - The Comprehensive Aura Digital Twin Core

import time
import csv
import os
import joblib
import psutil
import pandas as pd
import uuid

# --- 1. EXTERNAL LIBRARIES AND SERVICES ---
# These imports are now required directly in this file
import chromadb
from sentence_transformers import SentenceTransformer
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- 2. CONFIGURATION AND PATHS ---
LOG_FILE = 'aura_log.csv'
MODEL_FILE = 'random_forest_model.joblib' # Using the new Random Forest model
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'
PERSIST_PATH = "aura_memory_db"
COLLECTION_NAME = "activity_memories"
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2' 
POLL_INTERVAL = 60 # Poll every 60 seconds

# Google Calendar API Scopes
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Column Headers for the CSV (must match the training script)
HEADER = ['timestamp', 'user_state', 'active_app', 'key_count', 'mouse_distance', 'calendar_state']

# --- 3. MOUSE AND KEYBOARD TRACKING (Simplified Stubs) ---
# NOTE: In a real system, you would replace these with OS-level hooks (pynput, etc.)
# For simulation, we will use mock tracking logic
class MockTracker:
    def __init__(self):
        self.last_key_count = 0
        self.last_mouse_pos = (0, 0)
        
    def get_metrics(self):
        # Simulate keyboard activity (more keys when focused)
        key_count = int(20 + 30 * (time.time() % 10 < 5) + 5 * (time.time() % 60) / 60)
        
        # Simulate mouse movement (more movement when distracted/browsing)
        mouse_distance = int(500 + 1000 * (time.time() % 10 >= 5))
        
        # Get the active application (simplified)
        active_app = psutil.Process(os.getpid()).name() 
        if time.time() % 15 < 5:
            active_app = 'PyCharm' 
        elif time.time() % 15 < 10:
            active_app = 'Slack'
        else:
            active_app = 'Chrome'
            
        return active_app, key_count, mouse_distance

tracker = MockTracker()

# --- 4. GOOGLE CALENDAR SERVICE (Consolidated from calendar_client.py) ---
def get_calendar_service():
    """Authenticates the user and returns a Google Calendar service object."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, CALENDAR_SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, CALENDAR_SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

def get_current_calendar_state(service):
    """Checks the calendar for an event happening *right now*."""
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    try:
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=1, singleEvents=True, orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        if not events: return 'free' 

        event = events[0]
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        # NOTE: Using datetime objects requires an additional import:
        import datetime
        start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
        now_dt = datetime.datetime.now(datetime.timezone.utc)

        return 'in_meeting' if start_dt <= now_dt < end_dt else 'free'
    except Exception as e:
        # print(f"Error fetching calendar: {e}")
        return 'unknown'

# --- 5. VECTOR MEMORY SERVICE (Consolidated from memory_service.py) ---
class MemoryService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=PERSIST_PATH)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        # Chroma handles the embedding automatically with this line (simplification):
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            # We explicitly pass the sentence transformer model name
            embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=EMBEDDING_MODEL_NAME
            )
        )

    def generate_document_text(self, row):
        """Generates a rich, descriptive text string from a single log row."""
        return (
            f"User was '{row['user_state']}' for 60 seconds. "
            f"Active app was '{row['active_app']}'. "
            f"Typing: {row['key_count']} keys, Mouse: {int(row['mouse_distance'])}px. "
            f"Calendar state: '{row['calendar_state']}'. "
        )

    def save_memory(self, log_data_df):
        """Saves a batch of new log data as vectors (memories)."""
        ids = [str(uuid.uuid4()) for _ in log_data_df.index]
        documents = [self.generate_document_text(row) for index, row in log_data_df.iterrows()]
        metadatas = log_data_df.to_dict('records')

        try:
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
            # print(f"✅ Saved {len(ids)} new memories to ChromaDB.")
        except Exception as e:
            print(f"❌ Error saving to ChromaDB: {e}")

    def recall_context(self, current_state_text, n_results=5):
        """Queries the database for past memories most similar to the current activity."""
        try:
            # Chroma will embed the query text using the collection's defined embedding function
            results = self.collection.query(
                query_texts=[current_state_text],
                n_results=n_results,
                include=['documents']
            )
            
            return results.get('documents', [[]])[0]
        except Exception as e:
            # print(f"❌ Error recalling context from ChromaDB: {e}")
            return []

# --- 6. CORE LOGIC ---
def get_user_state_input(active_app):
    """Mocks the user input/labeling for training data creation."""
    prompt = f"Current App: {active_app}. What is your state? (focused/distracted/collaborating): "
    while True:
        state = input(prompt).strip().lower()
        if state in ['focused', 'distracted', 'collaborating']:
            return state
        print("Invalid state. Please use 'focused', 'distracted', or 'collaborating'.")

def initialize_services():
    """Initializes all external services and loads the ML model."""
    
    # 1. Check/Create CSV
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

    # 2. Load Model
    try:
        model = joblib.load(MODEL_FILE)
        print(f"✅ Loaded trained model from {MODEL_FILE}")
    except FileNotFoundError:
        print(f"❌ WARNING: Model file {MODEL_FILE} not found. Running in data collection mode only.")
        model = None
    
    # 3. Initialize Calendar
    calendar_service = None
    try:
        calendar_service = get_calendar_service()
        print("✅ Calendar service authenticated.")
    except Exception as e:
        print(f"❌ Could not initialize Calendar Service. Error: {e}")

    # 4. Initialize Memory
    memory_db = MemoryService()
    print("✅ Memory service ready.")
    
    return model, calendar_service, memory_db

def run_aura_core():
    """The main loop for data collection and state prediction."""
    
    model, calendar_service, memory_db = initialize_services()

    print("\n--- Aura Digital Twin Core Running ---\n")

    while True:
        start_time = time.time()

        # 1. Collect Raw Data
        active_app, key_count, mouse_distance = tracker.get_metrics()
        
        # 2. Get Calendar Context
        calendar_state = 'unknown'
        if calendar_service:
            calendar_state = get_current_calendar_state(calendar_service)
        
        # 3. Prompt for State (for training data)
        user_state = get_user_state_input(active_app)
        
        # 4. Prepare Data Row
        row_data = [
            int(time.time()),
            user_state,
            active_app,
            key_count,
            mouse_distance,
            calendar_state
        ]
        
        # 5. Save to CSV and Memory
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row_data)
        
        data_dict = dict(zip(HEADER, row_data))
        new_df = pd.DataFrame([data_dict])
        memory_db.save_memory(new_df)
        
        print(f"\n--- Data Logged ---")
        print(f"State: {user_state.upper()} | App: {active_app} | Cal: {calendar_state}")

        # 6. Prediction and Context Retrieval
        if model:
            # Prepare current data for prediction (must match training features)
            raw_input_data = pd.DataFrame([{'active_app': active_app, 
                                            'key_count': key_count, 
                                            'mouse_distance': mouse_distance, 
                                            'calendar_state': calendar_state}])
            
            # Predict the state using the Random Forest pipeline
            predicted_state = model.predict(raw_input_data)[0]
            
            # Create a simple text description for memory recall
            current_activity_desc = (
                f"I am currently in the app: {active_app} "
                f"with key counts: {key_count} and mouse distance: {mouse_distance}. "
                f"My calendar state is: {calendar_state}."
            )
            
            # Get the top 3 most similar past memories
            recalled_context = memory_db.recall_context(current_activity_desc, n_results=3)
            
            print(f"\n--- Aura State Prediction ---")
            print(f"**Predicted State: {predicted_state.upper()}**")
            print(f"| Memory Context Recalled |")
            print(f"|-------------------------|")
            for i, memory in enumerate(recalled_context):
                print(f"| {i+1}. {memory[:80]}...")
            print(f"---------------------------\n")

        # 7. Wait for the next cycle
        time_elapsed = time.time() - start_time
        time_to_wait = POLL_INTERVAL - time_elapsed
        if time_to_wait > 0:
            time.sleep(time_to_wait)

if __name__ == "__main__":
    run_aura_core()
