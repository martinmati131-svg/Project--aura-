# app_watcher.py
# Project Aura: v1.0 (Live Predictions)
# This agent collects data, logs user feedback, and makes live predictions.

import time
import threading
import csv
import os
import pandas as pd
import joblib
from AppKit import NSWorkspace
from pynput import keyboard, mouse
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw

# --- Configuration ---
LOG_FILE = 'aura_log.csv'
MODEL_FILE = 'aura_model.joblib'
COLUMNS_FILE = 'model_columns.joblib'
PREDICTION_INTERVAL = 30  # seconds

# --- Global State & Thread-Safety ---
class ActivityMonitor:
    def __init__(self):
        self.key_presses = 0
        self.mouse_clicks = 0
        self.lock = threading.Lock()

    def on_press(self, key):
        with self.lock:
            self.key_presses += 1

    def on_click(self, x, y, button, pressed):
        if pressed:
            with self.lock:
                self.mouse_clicks += 1
    
    def get_and_reset_counts(self):
        with self.lock:
            keys = self.key_presses
            clicks = self.mouse_clicks
            self.key_presses = 0
            self.mouse_clicks = 0
            return keys, clicks

def get_active_app_name():
    try:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        return active_app.localizedName()
    except Exception:
        return "Unknown"

# --- Data Logging ---
def write_log(label, app, keys, clicks):
    timestamp = int(time.time())
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, label, app, keys, clicks])

# --- Prediction Logic ---
def predict_current_state(model, columns):
    app = get_active_app_name()
    keys, clicks = monitor.get_and_reset_counts()
    
    # Create a DataFrame for the current state with the same structure as the training data
    live_data = pd.DataFrame([[app, keys, clicks]], columns=['app_name', 'key_presses', 'mouse_clicks'])
    live_features = pd.get_dummies(live_data, columns=['app_name'])
    
    # Align columns to match the model's training data exactly
    live_features_aligned = live_features.reindex(columns=columns, fill_value=0)
    
    # Make prediction
    prediction = model.predict(live_features_aligned)
    probability = model.predict_proba(live_features_aligned)
    
    confidence = max(probability[0]) * 100
    print(f"[{time.strftime('%H:%M:%S')}] LIVE PREDICTION: {prediction[0].upper()} (Confidence: {confidence:.1f}%) | App: {app} | Activity: {keys} keys, {clicks} clicks")

# --- Menu Bar Icon Logic ---
def on_focused_clicked(icon, item):
    keys, clicks = monitor.get_and_reset_counts()
    app = get_active_app_name()
    write_log('focused', app, keys, clicks)
    print(f"MANUAL LOG: focused | App: {app}")

def on_distracted_clicked(icon, item):
    keys, clicks = monitor.get_and_reset_counts()
    app = get_active_app_name()
    write_log('distracted', app, keys, clicks)
    print(f"MANUAL LOG: distracted | App: {app}")

def create_image():
    image = Image.new('RGB', (16, 16), color = 'black')
    dc = ImageDraw.Draw(image)
    dc.rectangle([(4, 4), (12, 12)], fill='white')
    return image

if __name__ == "__main__":
    print("Starting Aura Agent v1.0 (Live Predictions)...")

    # Initialize CSV file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'label', 'app_name', 'key_presses', 'mouse_clicks'])

    # --- Load the trained model ---
    try:
        model = joblib.load(MODEL_FILE)
        model_columns = joblib.load(COLUMNS_FILE)
        print("✅ Model loaded successfully.")
    except FileNotFoundError:
        print("⚠️ Model not found. Running in data collection mode only.")
        print("   Run train_model.py to build the model.")
        model = None
        model_columns = None

    # --- Start background activity monitoring ---
    monitor = ActivityMonitor()
    keyboard_listener = keyboard.Listener(on_press=monitor.on_press)
    mouse_listener = mouse.Listener(on_click=monitor.on_click)
    keyboard_listener.start()
    mouse_listener.start()

    # --- Start the prediction loop in a separate thread if model is loaded ---
    if model:
        def prediction_loop():
            predict_current_state(model, model_columns)
            # Schedule the next prediction
            threading.Timer(PREDICTION_INTERVAL, prediction_loop).start()
        
        # Start the first prediction after a short delay
        threading.Timer(PREDICTION_INTERVAL, prediction_loop).start()
        print(f"Live predictions will start in {PREDICTION_INTERVAL} seconds.")

    # --- Setup and run the Menu Bar Icon ---
    icon = pystray.Icon(
        "Aura",
        icon=create_image(),
        title="Aura Agent",
        menu=pystray.Menu(
            item('I\'m Focused', on_focused_clicked),
            item('I\'m Distracted', on_distracted_clicked)
        )
    )
    
    icon.run()


 
   