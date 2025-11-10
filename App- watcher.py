
# aura_platform_core.py
# Project Aura: Platform v0.1
# The core engine that senses, predicts, and serves the Aura state via a local API.

import time
import threading
import pandas as pd
import joblib
from flask import Flask, jsonify
# client/app_watcher.py

# ... (Existing imports like time, csv, etc.)
from . import calendar_client 
from . import memory_service # <--- NEW IMPORT
# ...
if __name__ == "__main__":
    # ... (Calendar Service initialization)
    
    # --- NEW: Initialize Memory Service ---
    try:
        print("Connecting to ChromaDB Memory Service...")
        memory_db = memory_service.MemoryService()
        print("✅ Memory service ready.")
    except Exception as e:
        print(f"❌ Could not initialize Memory Service. Running without long-term memory. Error: {e}")
        memory_db = None
        
    # ... (The rest of your existing setup code continues here...)

# client/app_watcher.py

# ... (Existing imports like time, csv, etc.)
from . import calendar_client # Import our new calendar module
# ...

# client/app_watcher.py

# ... (inside the main block)
if __name__ == "__main__":
    # --- NEW: Initialize Calendar Service ---
    try:
        print("Connecting to Google Calendar for the first time...")
        calendar_service = calendar_client.get_calendar_service()
        print("✅ Calendar service authenticated.")
    except Exception as e:
        print(f"❌ Could not initialize Calendar Service. Running without calendar data. Error: {e}")
        calendar_service = None
        
    # --- The rest of your existing setup code continues here...
    
    # ... (Then the main while loop starts)
    while True:
        # ...
# client/app_watcher.py

# ... (inside the main while True loop)

    # 1. Get raw system metrics (app, mouse, keyboard)
    # ... (Your existing code to get active_app, key_count, mouse_distance)
    
    # 2. Get the new Calendar State
    calendar_state = 'unknown' # Default value
    if calendar_service:
        calendar_state = calendar_client.get_current_calendar_state(calendar_service)
        
    # 3. Prompt for State (User Feedback)
    user_state = get_user_state_input(active_app)
    
    # 4. Prepare the row for the CSV
    row_data = [
        int(time.time()),
        user_state,
        active_app,
        key_count,
        mouse_distance,
        calendar_state # <-- NEW FEATURE COLUMN
    ]

    # ... (The rest of your existing code to save to CSV)
    # ... (print(f"Logged: {row_data}"))


# --- (You can copy these from your previous file) ---
from AppKit import NSWorkspace
from pynput import keyboard, mouse
# --- (Keep the ActivityMonitor class and get_active_app_name function as they are) ---

# --- Placeholder for the full ActivityMonitor class ---
# Make sure to copy your full ActivityMonitor class here
class ActivityMonitor:
    def __init__(self):
        self.key_presses = 0
        self.mouse_clicks = 0
        self.lock = threading.Lock()
    def on_press(self, key):
        with self.lock: self.key_presses += 1
    def on_click(self, x, y, button, pressed):
        if pressed:
            with self.lock: self.mouse_clicks += 1
    def get_and_reset_counts(self):
        with self.lock:
            keys, clicks = self.key_presses, self.mouse_clicks
            self.key_presses, self.mouse_clicks = 0, 0
            return keys, clicks

def get_active_app_name():
    try:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        return active_app.localizedName()
    except Exception: return "Unknown"
# --- End of placeholder ---


# --- Global State for API ---
# A thread-safe dictionary to hold the latest Aura state.
aura_state = {"status": "initializing", "prediction": None, "confidence": 0.0}
state_lock = threading.Lock()

# --- Prediction Logic ---
def predict_current_state(model, columns, monitor):
    app = get_active_app_name()
    keys, clicks = monitor.get_and_reset_counts()
    
    live_data = pd.DataFrame([[app, keys, clicks]], columns=['app_name', 'key_presses', 'mouse_clicks'])
    live_features = pd.get_dummies(live_data, columns=['app_name'])
    live_features_aligned = live_features.reindex(columns=columns, fill_value=0)
    
    prediction = model.predict(live_features_aligned)[0]
    probability = model.predict_proba(live_features_aligned)
    confidence = max(probability[0])
    
    # --- Update the global state for the API ---
    with state_lock:
        aura_state["status"] = "running"
        aura_state["prediction"] = prediction
        aura_state["confidence"] = float(confidence)
    
    print(f"[{time.strftime('%H:%M:%S')}] Prediction updated: {prediction.upper()} ({confidence:.1%})")

# --- API Server ---
app = Flask(__name__)

@app.route("/api/v1/aura/status", methods=['GET'])
def get_aura_status():
    """The main API endpoint to get the current Aura state."""
    with state_lock:
        return jsonify(aura_state)

# --- Main Application Logic ---
if __name__ == "__main__":
    print("Starting Aura Platform Core...")
    
    MODEL_FILE = 'aura_model.joblib'
    COLUMNS_FILE = 'model_columns.joblib'
    PREDICTION_INTERVAL = 30 # seconds

    try:
        model = joblib.load(MODEL_FILE)
        model_columns = joblib.load(COLUMNS_FILE)
        print("✅ Model loaded successfully.")
    except FileNotFoundError:
        print("FATAL: Model not found. The platform cannot start without a trained model.")
        exit()

    monitor = ActivityMonitor()
    keyboard_listener = keyboard.Listener(on_press=monitor.on_press)
    mouse_listener = mouse.Listener(on_click=monitor.on_click)
    keyboard_listener.start()
    mouse_listener.start()

    # --- Start the prediction loop in a separate thread ---
    def prediction_loop():
        while True:
            predict_current_state(model, model_columns, monitor)
            time.sleep(PREDICTION_INTERVAL)

    prediction_thread = threading.Thread(target=prediction_loop, daemon=True)
    prediction_thread.start()
    print(f"Prediction engine is running. Updates every {PREDICTION_INTERVAL} seconds.")

    # --- Start the API server ---
    print("\n🚀 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5 Aura API is live and listening on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)



  # ... (keep all your other code: Flask setup, ActivityMonitor, etc.) ...
# ... (keep your existing @app.route("/api/v1/aura/status") ...

#
# --- ADD THIS NEW FUNCTION ---
#
@app.route("/api/v1/aura/command", methods=['POST'])
def handle_command():
    """Receives a command from the robot dashboard."""
    try:
        data = request.get_json()
        command = data.get('command')

        if command == "TOGGLE_SHIELD":
            # In a real app, this would message focus_shield.py
            # For now, we just print to the console to prove it works.
            print(f"\n--- 🤖 DASHBOARD COMMAND RECEIVED: {command} ---\n")
            return jsonify({"status": "success", "command_received": command}), 200
        else:
            return jsonify({"status": "error", "message": "Unknown command"}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
#
# --- END OF NEW FUNCTION ---
#

if __name__ == "__main__":
    # ... (all your startup code) ...
    # ... (app.run(host='127.0.0.1', port=5000))
   
   
     
      
           
        

 
   