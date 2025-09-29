# app_watcher.py
# Project Aura: v0.4
# Adds a menu bar icon for user feedback and logs labeled data to a CSV file.

import time
import threading
import csv
from AppKit import NSWorkspace
from pynput import keyboard, mouse
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw

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
    """Gets the name of the frontmost application."""
    try:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        app_name = active_app.localizedName()
        return app_name
    except Exception:
        return "Unknown"

# --- Data Logging ---
LOG_FILE = 'aura_log.csv'

def write_log(label, app, keys, clicks):
    """Appends a new row to our CSV log file."""
    timestamp = int(time.time())
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, label, app, keys, clicks])

# --- Menu Bar Icon Logic ---
def on_focused_clicked(icon, item):
    """Callback for the 'Focused' menu item."""
    keys, clicks = monitor.get_and_reset_counts()
    app = get_active_app_name()
    write_log('focused', app, keys, clicks)
    print(f"LOGGED: focused | App: {app} | Activity: {keys} keys, {clicks} clicks")

def on_distracted_clicked(icon, item):
    """Callback for the 'Distracted' menu item."""
    keys, clicks = monitor.get_and_reset_counts()
    app = get_active_app_name()
    write_log('distracted', app, keys, clicks)
    print(f"LOGGED: distracted | App: {app} | Activity: {keys} keys, {clicks} clicks")

def create_image():
    """Create a simple 16x16 icon for the menu bar."""
    image = Image.new('RGB', (16, 16), color = 'black')
    dc = ImageDraw.Draw(image)
    dc.rectangle([(4, 4), (12, 12)], fill='white')
    return image

if __name__ == "__main__":
    print("Starting Aura Agent v0.4 (Data Logger)...")

    # Initialize CSV file with headers if it doesn't exist
    try:
        with open(LOG_FILE, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'label', 'app_name', 'key_presses', 'mouse_clicks'])
    except FileExistsError:
        pass # File already exists

    # --- Setup Activity Monitoring in a background thread ---
    monitor = ActivityMonitor()
    keyboard_listener = keyboard.Listener(on_press=monitor.on_press)
    mouse_listener = mouse.Listener(on_click=monitor.on_click)
    keyboard_listener.start()
    mouse_listener.start()

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
    
    print("Agent is running in the menu bar. Right-click the icon to log your status.")
    icon.run()


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
