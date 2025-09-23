# app_watcher.py
# Project Aura: Step 1.1
# This script identifies and prints the name of the active application on macOS.

import time
from AppKit import NSWorkspace

def get_active_app_name():
    """
    Uses the AppKit framework to get the name of the frontmost application.
    """
    try:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        app_name = active_app.localizedName()
        return app_name
    except Exception as e:
        # Handle cases where the name might not be retrievable
        return f"Unknown ({e})"

if __name__ == "__main__":
    print("Starting App Watcher... Press CTRL+C to stop.")
    try:
        while True:
            # Get the name of the active application
            current_app = get_active_app_name()
            
            # Print it to the console with a timestamp
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"[{timestamp}] Active App: {current_app}")
            
            # Wait for 2 seconds before checking again
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStopping App Watcher. Goodbye!")

