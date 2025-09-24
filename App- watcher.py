
# app_watcher.py
# Project Aura: v0.3
# Now tracks input rhythm (keyboard/mouse activity) in addition to context switches.

import time
from AppKit import NSWorkspace
from pynput import keyboard, mouse
import threading

# --- Global State & Thread-Safety ---
# A simple thread-safe object to hold our activity counts.
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
    """Gets the name of the frontmost application."""
    try:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        app_name = active_app.localizedName()
        return app_name
    except Exception:
        return "Unknown"

if __name__ == "__main__":
    print("Starting Aura Agent v0.3 (Context & Rhythm)... Press CTRL+C to stop.")
    
    # --- Setup Activity Monitoring ---
    monitor = ActivityMonitor()
    keyboard_listener = keyboard.Listener(on_press=monitor.on_press)
    mouse_listener = mouse.Listener(on_click=monitor.on_click)
    
    keyboard_listener.start()
    mouse_listener.start()
    
    # --- Main Loop ---
    previous_app = get_active_app_name()
    print(f"Initial application: {previous_app}")
    
    try:
        while True:
            time.sleep(10) # Check every 10 seconds
            
            # 1. Get activity counts for the last interval
            keys, clicks = monitor.get_and_reset_counts()
            
            # 2. Check for context switch
            current_app = get_active_app_name()
            if current_app != previous_app:
                timestamp = time.strftime('%H:%M:%S')
                print(f"[{timestamp}] CONTEXT SWITCH: To '{current_app}'")
                print(f"    └─ Activity in '{previous_app}': {keys} keys, {clicks} clicks.")
                previous_app = current_app
            else:
                timestamp = time.strftime('%H:%M:%S')
                print(f"[{timestamp}] HEARTBEAT: Still in '{current_app}'. Activity: {keys} keys, {clicks} clicks.")

    except KeyboardInterrupt:
        print("\nStopping agent...")
        keyboard_listener.stop()
        mouse_listener.stop()
        print("Goodbye!")
