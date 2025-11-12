# aura_platform_core.py - The Comprehensive Aura Digital Twin Core (Attention-Aware)

import time
import csv
import os
import joblib
import psutil
import pandas as pd
import uuid
import datetime
import numpy as np

# --- 1. EXTERNAL LIBRARIES AND SERVICES ---
# Core ML/AI Dependencies
import chromadb
from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.preprocessing import LabelEncoder

# Google Calendar API Dependencies
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- 2. CONFIGURATION AND PATHS ---
LOG_FILE = 'aura_log.csv'
FINAL_MODEL_FILE = 'attention_aware_classifier.joblib' # Loads the final SVM/RF
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'
PERSIST_PATH = "aura_memory_db"
COLLECTION_NAME = "activity_memories"
# Transformer Model used for Attention Vector generation
TRANSFORMER_MODEL_NAME = 'distilbert-base-uncased' 
POLL_INTERVAL = 60 # Poll every 60 seconds

# Google Calendar API Scopes
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Column Headers for the CSV (must match the training script)
HEADER = ['timestamp', 'user_state', 'active_app', 'key_count', 'mouse_distance', 'calendar_state']

# --- 3. MOUSE AND KEYBOARD TRACKING (MOCK) ---
class MockTracker:
    # Simulates activity data for demonstration purposes
    def __init__(self):
        pass
        
    def get_metrics(self):
        # Simulate activity based on time
        t = time.time()
        key_count = int(20 + 30 * (t % 10 < 5) + 5 * (t % 60) / 60)
        mouse_distance = int(500 + 1000 * (t % 10 >= 5))
        
        # Simulate app usage
        active_app = 'Chrome'
        if t % 15 < 5: active_app = 'PyCharm' 
        elif t % 15 < 10: active_app = 'Slack'
            
        return active_app, key_count, mouse_distance

tracker = MockTracker()

# --- 4. GOOGLE CALENDAR SERVICE ---
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
        
        start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
        now_dt = datetime.datetime.now(datetime.timezone.utc)

        return 'in_meeting' if start_dt <= now_dt < end_dt else 'free'
    except Exception as e:
        # print(f"Error fetching calendar: {e}")
        return 'unknown'

# --- 5. VECTOR MEMORY SERVICE ---
class MemoryService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=PERSIST_PATH)
        # Note: We configure Chroma to use the same Sentence Transformer as our main extractor
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=TRANSFORMER_MODEL_NAME
            )
        )

    def generate_document_text(self, row):
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
        except Exception as e:
            print(f"❌ Error saving to ChromaDB: {e}")

    def recall_context(self, current_state_text, n_results=3):
        """Queries the database for past memories most similar to the current activity."""
        try:
            results = self.collection.query(
                query_texts=[current_state_text],
                n_results=n_results,
                include=['documents']
            )
            return results.get('documents', [[]])[0]
        except Exception as e:
            print(f"❌ Error recalling context from ChromaDB: {e}")
            return []

# --- 6. TRANSFORMER FEATURE EXTRACTOR (ATTENTION) ---
class TransformerFeatureExtractor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(TRANSFORMER_MODEL_NAME)
        self.model = AutoModel.from_pretrained(TRANSFORMER_MODEL_NAME)
        self.device = torch.device("cpu") 

    def encode_text(self, text_input):
        """Feeds the context text through the Transformer and extracts the attention vector."""
        encoded_input = self.tokenizer(
            text_input, return_tensors='pt', padding=True, truncation=True, max_length=128
        ).to(self.device)

        with torch.no_grad():
            output = self.model(**encoded_input)

        # Extract the [CLS] token embedding (the summary of attention)
        cls_embedding = output.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
        return cls_embedding


# --- 7. CORE LOGIC ---
def get_user_state_input(active_app):
    """Prompts user for manual state labeling for training data."""
    prompt = f"Current App: {active_app}. What is your state? (focused/distracted/collaborating): "
    while True:
        state = input(prompt).strip().lower()
        if state in ['focused', 'distracted', 'collaborating']:
            return state
        print("Invalid state. Please use 'focused', 'distracted', or 'collaborating'.")

def initialize_services():
    """Initializes all external services and loads the ML model/encoder."""
    
    # 1. Check/Create CSV
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

    # 2. Load Model & Encoder
    model_data = None
    try:
        model_data = joblib.load(FINAL_MODEL_FILE)
        model = model_data['model']
        encoder = model_data['encoder']
        print(f"✅ Loaded Attention-Aware Classifier from {FINAL_MODEL_FILE}")
    except FileNotFoundError:
        print(f"❌ WARNING: Model file {FINAL_MODEL_FILE} not found. Running in data collection mode only.")
        model = None
        encoder = None
    
    # 3. Initialize Calendar
    calendar_service = None
    try:
        calendar_service = get_calendar_service()
        print("✅ Calendar service authenticated.")
    except Exception as e:
        print(f"❌ Could not initialize Calendar Service. Error: {e}")

    # 4. Initialize Memory & Transformer Extractor
    memory_db = MemoryService()
    transformer_extractor = TransformerFeatureExtractor()
    print("✅ Memory and Transformer services ready.")
    
    return model, encoder, calendar_service, memory_db, transformer_extractor

def run_aura_core():
    """The main loop for data collection and state prediction."""
    
    model, encoder, calendar_service, memory_db, transformer_extractor = initialize_services()

    print("\n--- Aura Digital Twin Core Running (Attention-Aware) ---\n")

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
            int(time.time()), user_state, active_app, key_count, mouse_distance, calendar_state
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

        # 6. Prediction (Only runs if the model is loaded)
        if model and encoder:
            # --- 6a. GATHER ALL CONTEXT ---
            current_activity_desc = (
                f"App is {active_app}, Key Count is {key_count}, Mouse Distance is {mouse_distance}. "
                f"Calendar State is '{calendar_state}'."
            )
            # Use the current activity to recall similar memories
            recalled_context = memory_db.recall_context(current_activity_desc, n_results=3)
            context_str = "\n".join(recalled_context)
            
            # Create the single input text for the Transformer
            full_input_text = f"Current State: {current_activity_desc}\nPast Memories: {context_str}"

            # --- 6b. TRANSFORM (ATTENTION) STEP ---
            # Generate the 768-dimensional Attention Vector
            attention_vector = transformer_extractor.encode_text(full_input_text)
            
            # Reshape the vector for the final model prediction (1 sample, 768 features)
            X_attention = attention_vector.reshape(1, -1) 
            
            # --- 6c. FINAL PREDICTION ---
            predicted_label = model.predict(X_attention)[0]
            predicted_state = encoder.inverse_transform([predicted_label])[0]
            
            print(f"\n--- Aura State Prediction (Attention-Aware) ---")
            print(f"**Predicted State: {predicted_state.upper()}**")
            print(f"Memory Context Used:")
            for i, memory in enumerate(recalled_context):
                print(f"| {i+1}. {memory[:80]}...")
            print(f"-------------------------------------------\n")

        # 7. Wait for the next cycle
        time_elapsed = time.time() - start_time
        time_to_wait = POLL_INTERVAL - time_elapsed
        if time_to_wait > 0:
            time.sleep(time_to_wait)

if __name__ == "__main__":
    run_aura_core()
