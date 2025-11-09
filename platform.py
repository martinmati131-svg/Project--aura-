

app.py
from flask import Flask, request, jsonify
from sklearn.externals import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained AI model
model = aura_model.joblib('aura model
h5')

@app.route('/track', methods=['POST'])
def track():
    # Get user activity data from the request
    data = request.get_json()
    mouse_data = data['mouse']
    keyboard_data = data['keyboard']

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
 
    # Extract features from the data
    features = extract_features(mouse_data, keyboard_data)
    
    # Classify the user state using the AI model
    classification = model.predict(features)
    
    # Return the classification result
    return jsonify({'classification': classification})

def extract_features(mouse_data, keyboard_data):
    # Calculate features from mouse data (e.g., movement speed, click frequency)
    mouse_features = [
        calculate_movement_speed(mouse_data),
        calculate_click_frequency(mouse_data)
    ]
    
    # Calculate features from keyboard data (e.g., typing speed, key press frequency)
    keyboard_features = [
        calculate_typing_speed(keyboard_data),
        calculate_key_press_frequency(keyboard_data)
    ]
    
    # Combine mouse and keyboard features
    features = mouse_features + keyboard_features
    
    return [features]

def calculate_movement_speed(mouse_data):
    # Calculate movement speed based on mouse data
    # (Implementation depends on the format of the mouse data)
    pass

def calculate_click_frequency(mouse_data):
    # Calculate click frequency based on mouse data
    # (Implementation depends on the format of the mouse data)
    pass

def calculate_typing_speed(keyboard_data):
    # Calculate typing speed based on keyboard data
    # (Implementation depends on the format of the keyboard data)
    pass

def calculate_key_press_frequency(keyboard_data):
    # Calculate key press frequency based on keyboard data
    # (Implementation depends on the format of the keyboard data)
    pass

if __name__ == '__main__':
    app.run(debug=True

 JavaScript:
// Track mouse movement
document.addEventListener('mousemove', (event) => {
    // Send mouse data to the API
    fetch('/track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            mouse: {
                x: event.clientX,
                y: event.clientY,
                timestamp: Date.now()
            }
        })
    });
});

// Track keyboard input
document.addEventListener('keydown', (event) => {
    // Send keyboard data to the API
    fetch('/track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            keyboard: {
                key: event.key,
                timestamp: Date.now()
            }
        })
    });
});
