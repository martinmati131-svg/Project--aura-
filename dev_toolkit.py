# dev_toolkit.py
# Project Aura: Developer Toolkit v0.1

import time
import requests

# The address of our Aura Core API
AURA_API_URL = "http://127.0.0.1:5000/api/v1/aura/status"
POLL_INTERVAL = 5 # seconds

# --- STATE TRACKING ---
# We need to see how long a user has been in a "distracted" state
distracted_start_time = None
HELP_OFFERED = False

def get_aura_state():
    """Gets the current state from the Aura Core API."""
    try:
        response = requests.get(AURA_API_URL)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def run_dev_toolkit():
    """The main loop for the Developer Toolkit."""
    global distracted_start_time, HELP_OFFERED
    
    print("🧑‍💻 Aura Developer Toolkit is online.")
    print("   Watching for 'debugging' patterns...")

    while True:
        state_data = get_aura_state()

        if not state_data or state_data.get("status") != "running":
            # Reset states if brain is offline
            distracted_start_time = None
            HELP_OFFERED = False
            time.sleep(POLL_INTERVAL)
            continue

        current_prediction = state_data.get("prediction")

        # --- This is the core logic ---
        if current_prediction == "distracted":
            if distracted_start_time is None:
                # User just became distracted, start the timer
                distracted_start_time = time.time()
            else:
                # User is still distracted, check how long
                duration_distracted = time.time() - distracted_start_time
                
                # If they've been distracted for 30 seconds...
                if duration_distracted > 30 and not HELP_OFFERED:
                    offer_debugging_help()
                    HELP_OFFERED = True # Only offer help once
        
        elif current_prediction == "focused":
            # User is focused, reset everything
            distracted_start_time = None
            HELP_OFFERED = False
        
        time.sleep(POLL_INTERVAL)

def offer_debugging_help():
    """
    This is the "proactive" part.
    In a real app, this would be a pop-up.
    """
    print("\n[AURA DEV TOOLKIT]")
    print("   ...Detecting a 'debugging' pattern (high context-switching)...")
    print("   💡 Would you like me to scan your recent code for common errors?\n")
    # In a real app, we would now trigger a linter or AI code-scan
    
if __name__ == "__main__":
    run_dev_toolkit()
