# focus_shield.py
# Project Aura: App v0.1 (Focus Shield)
# A client app that connects to the Aura Core API
# and prepares to take action based on the user's state.

import time
import requests

# The address of our Aura Core API
AURA_API_URL = "http://127.0.0.1:5000/api/v1/aura/status"
POLL_INTERVAL = 5 # seconds

class FocusShield:
    def __init__(self):
        self.shield_active = False
        print("🛡️ Aura Focus Shield is online.")
        print("Connecting to Aura Core...")

    def get_aura_state(self):
        """Gets the current state from the Aura Core API."""
        try:
            response = requests.get(AURA_API_URL)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.ConnectionError:
            return None

    def run(self):
        """The main loop for the Focus Shield."""
        while True:
            state_data = self.get_aura_state()

            if not state_data or state_data.get("status") != "running":
                print("...Waiting for Aura Core to come online...")
                time.sleep(POLL_INTERVAL)
                continue

            current_prediction = state_data.get("prediction")

            # --- This is the core logic ---
            if current_prediction == "focused" and not self.shield_active:
                self.engage_shield()
            elif current_prediction != "focused" and self.shield_active:
                self.disengage_shield()
            
            time.sleep(POLL_INTERVAL)

    def engage_shield(self):
        """Activates the Focus Shield."""
        print("\n[FOCUS SHIELD: ENGAGED]")
        print("   - (Action: Muting notifications...)")
        print("   - (Action: Blocking distracting websites...)")
        print("   - (Action: Starting 'Deep Work' playlist...)\n")
        self.shield_active = True

    def disengage_shield(self):
        """Deactivates the Focus Shield."""
        print("\n[FOCUS SHIELD: DISENGAGED]")
        print("   - (Action: Notifications unmuted.)")
        print("   - (Action: Websites unblocked.)\n")
        self.shield_active = False

if __name__ == "__main__":
    shield = FocusShield()
    shield.run()
