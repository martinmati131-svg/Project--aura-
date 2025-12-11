pyinstaller ^
--name "AuraService" ^
--onefile ^
--windowed ^
--add-data "attention_aware_classifier.joblib:." ^
--add-data "aura_log.csv:." ^
--add-data "credentials.json:." ^
--add-data "token.json:." ^
--add-data "aura_memory_db:aura_memory_db" ^
--hidden-import "uvicorn.logging" ^
--hidden-import "uvicorn.lifespan.on" ^
--hidden-import "chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2" ^
--hidden-import "onnxruntime" ^
--hidden-import "tokenizers" ^
--collect-all "chromadb" ^
prediction_api.py
# prediction_api.py

# ... (Previous imports and globals) ...

# --- NEW: Sentinel Security Logic ---
def check_security_risk(visual_state, key_count, mouse_distance):
    """
    Gov-Grade Security Logic: Detects physical vs digital anomalies.
    """
    alerts = []
    risk_level = "low"

    # 1. THE GHOST PROTOCOL (Critical)
    # Camera sees nobody, but keys are typing.
    if visual_state == 'absent' and (key_count > 10 or mouse_distance > 50):
        alerts.append("GHOST_USER_DETECTED: Active input from empty station.")
        risk_level = "CRITICAL"

    # 2. THE BLIND TYPIST (Suspicious)
    # User is looking away (phone/person) but typing heavily.
    # Could be copying data from a secondary unauthorized device.
    elif visual_state == 'distracted' and key_count > 100:
        alerts.append("SUSPICIOUS_INPUT: High activity while distracted.")
        risk_level = "medium"

    return risk_level, alerts

# ... (Inside @app.post("/predict_state/")) ...

@app.post("/predict_state/")
async def predict_state(data: ActivityInput):
    # ... (Model check code) ...
    
    # --- 1. RUN SENTINEL CHECK FIRST ---
    # We use the global latest_visual_state from the background thread
    security_risk, security_alerts = check_security_risk(
        latest_visual_state, 
        data.key_count, 
        data.mouse_distance
    )

    # --- 2. GATHER CONTEXT (Modified to include Security Alert) ---
    current_activity_desc = (
        f"App: {data.active_app}. Keys: {data.key_count}. Mouse: {data.mouse_distance}. "
        f"Visual: '{latest_visual_state}'. "
        f"Security Level: {security_risk.upper()}."  # <--- Context for the Brain
    )
    
    # ... (Memory Recall and Transformer Encoding steps remain the same) ...
    
    # --- 3. RETURN ENHANCED RESPONSE ---
    return {
        "predicted_state": predicted_state,
        "confidence": round(float(confidence), 2),
        "visual_sense": latest_visual_state,
        # NEW SECURITY FIELDS
        "security_risk": security_risk, 
        "security_alerts": security_alerts
    }
# prediction_api.py (New Pydantic model at the top)
class InsightLog(BaseModel):
    user_hash: str # Anonymized user identifier (e.g., hash of employee ID)
    focus_minutes: int
    distracted_minutes: int
    security_alerts: int
    
# ... (Inside the FastAPI app instance) ...

@app.post("/log_insight/")
async def log_insight(data: InsightLog):
    """
    Receives hourly insights from a remote Aura Agent. 
    This is where we'd insert into a central MongoDB/PostgreSQL database.
    """
    # NOTE: In the prototype, we just print and save to a temporary log
    # In a real enterprise system, this connects to the central DB
    insight = (
        f"{datetime.now().isoformat()}, {data.user_hash}, "
        f"{data.focus_minutes}, {data.distracted_minutes}, {data.security_alerts}\n"
    )
    with open("central_insight_log.csv", "a") as f:
        f.write(insight)
        
    return {"status": "success", "message": "Insight logged."}
from collections import defaultdict
import csv

@app.get("/get_team_report/")
async def get_team_report(days: int = 7):
    """
    Retrieves and aggregates data for the past 'days' for the management dashboard.
    """
    
    # 1. Simulate reading the Central Database (our CSV log)
    team_data = defaultdict(lambda: {'focus': 0, 'distracted': 0, 'alerts': 0})
    
    # In a production environment, this would be an optimized DB query
    try:
        with open("central_insight_log.csv", "r") as f:
            reader = csv.reader(f)
            # Assuming format: [timestamp, user_hash, focus_minutes, distracted_minutes, security_alerts]
            for row in reader:
                if len(row) < 5: continue
                # We aggregate by user_hash and sum the metrics
                user = row[1].strip()
                team_data[user]['focus'] += int(row[2].strip())
                team_data[user]['distracted'] += int(row[3].strip())
                team_data[user]['alerts'] += int(row[4].strip())
    except FileNotFoundError:
        return {"error": "No central insight data found."}

    # 2. Format the output for the dashboard
    report = []
    for user_hash, metrics in team_data.items():
        total_time = metrics['focus'] + metrics['distracted']
        focus_percentage = (metrics['focus'] / total_time) * 100 if total_time > 0 else 0
        
        report.append({
            "user_id_anonymized": user_hash,
            "total_focus_minutes": metrics['focus'],
            "focus_percentage": round(focus_percentage, 1),
            "security_alerts_total": metrics['alerts']
        })

    return {"report_period_days": days, "team_metrics": report}
# prediction_api.py

import platform
import subprocess
import ctypes # Necessary for Windows lock function

# --- NEW: OS Control Function ---
def lock_workstation():
    """
    Executes the command to lock the workstation based on the OS.
    """
    os_name = platform.system()
    
    try:
        if os_name == "Windows":
            # Direct call to the Windows API function
            ctypes.windll.user32.LockWorkStation()
            print("🛑 CRITICAL LOCKDOWN: Windows workstation locked.")
        
        elif os_name == "Darwin": # macOS
            # Command to invoke the screen saver/lock screen
            subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
            print("🛑 CRITICAL LOCKDOWN: macOS workstation locked.")
            
        elif os_name == "Linux":
            # Common commands for Linux desktop environments (requires a screen locker)
            # You might need to check which locker is installed (gnome-screensaver, loginctl, etc.)
            subprocess.run(["loginctl", "lock-session"]) 
            # Fallback for X environments
            # subprocess.run(["xdg-screensaver", "lock"])
            print("🛑 CRITICAL LOCKDOWN: Linux workstation lock initiated.")
            
        else:
            print(f"🛑 WARNING: Lock command unknown for OS: {os_name}")
            return False
            
        return True

    except Exception as e:
        print(f"🛑 ERROR during lockdown attempt: {e}")
        return False

# ... (Inside @app.post("/predict_state/")) ...

@app.post("/predict_state/")
async def predict_state(data: ActivityInput):
    # ... (Sentinel Check and Context Gathering remain the same) ...
    
    security_risk, security_alerts = check_security_risk(
        latest_visual_state, 
        data.key_count, 
        data.mouse_distance
    )
    
    # --- ZERO TRUST ENFORCEMENT POINT ---
    if security_risk == "CRITICAL":
        lock_successful = lock_workstation()
        
        # If lockdown fails, still report the alert
        if not lock_successful:
            security_alerts.append("ERROR: Automatic lockdown failed.")


    # ... (Rest of the original logic to return the response) ...
    
    return {
        "predicted_state": predicted_state,
        "confidence": round(float(confidence), 2),
        "visual_sense": latest_visual_state,
        "security_risk": security_risk, 
        "security_alerts": security_alerts
    }
# prediction_api.py (Add new import at the top)
import hashlib

# ... (New Pydantic model for receiving a raw user ID from the client) ...

class AuthInput(BaseModel):
    employee_id: str # e.g., "JDOE123"

# --- NEW: Hashing Function ---
def hash_user_id(employee_id: str) -> str:
    """Creates a privacy-preserving hash of the employee ID."""
    # Salt the hash to prevent dictionary attacks using a fixed, known string
    SALT = "AuraDigitalTwinV1" 
    hasher = hashlib.sha256()
    hasher.update((employee_id + SALT).encode('utf-8'))
    return hasher.hexdigest()

# ... (Add a new /register endpoint for the client to send its ID once) ...

@app.post("/register_user/")
async def register_user(data: AuthInput):
    """Placeholder for the client to register and get its anonymized ID."""
    anonymized_id = hash_user_id(data.employee_id)
    # In a real system, the client saves this hash and uses it for all future communications.
    return {"anonymized_id": anonymized_id, "status": "success"}

# RETHINKING THE LOGGING ENDPOINT:
# The /log_insight/ endpoint (from step 1) must now accept the hash, not the PII.
# (The implementation in the previous step already used 'user_hash' which aligns with this PPD.)
# prediction_api.py (Add new import at the top)
import hashlib
from pydantic import BaseModel

# --- NEW: Hashing Function ---
def hash_user_id(employee_id: str) -> str:
    """Creates a privacy-preserving, one-way hash of the employee ID."""
    # Using a SALT makes the hash unique to the organization, preventing outside dictionary attacks.
    SALT = "AuraDigitalTwinV1-Gov" 
    hasher = hashlib.sha256()
    # Encode for hashing and combine with the salt
    hasher.update((employee_id + SALT).encode('utf-8')) 
    return hasher.hexdigest()

# ... (Add a new endpoint for the client to register its ID once upon install) ...

class AuthInput(BaseModel):
    employee_id: str # e.g., "JDOE123"

@app.post("/register_user/")
async def register_user(data: AuthInput):
    """
    Endpoint called once by the client to receive its permanent, anonymized ID.
    The client saves this ID for all future communications with the central server.
    """
    anonymized_id = hash_user_id(data.employee_id)
    print(f"User {data.employee_id[:3]}... registered. Hash: {anonymized_id[:10]}...")
    return {"anonymized_id": anonymized_id, "status": "success"}

# IMPORTANT: All future calls to /log_insight/ and other endpoints MUST use this anonymized_id.

# prediction_api.py (Add new import at the top)
import hashlib
from pydantic import BaseModel

# --- NEW: Hashing Function ---
def hash_user_id(employee_id: str) -> str:
    """Creates a privacy-preserving, one-way hash of the employee ID."""
    # Using a SALT makes the hash unique to the organization, preventing outside dictionary attacks.
    SALT = "AuraDigitalTwinV1-Gov" 
    hasher = hashlib.sha256()
    # Encode for hashing and combine with the salt
    hasher.update((employee_id + SALT).encode('utf-8')) 
    return hasher.hexdigest()

# ... (Add a new endpoint for the client to register its ID once upon install) ...

class AuthInput(BaseModel):
    employee_id: str # e.g., "JDOE123"

@app.post("/register_user/")
async def register_user(data: AuthInput):
    """
    Endpoint called once by the client to receive its permanent, anonymized ID.
    The client saves this ID for all future communications with the central server.
    """
    anonymized_id = hash_user_id(data.employee_id)
    print(f"User {data.employee_id[:3]}... registered. Hash: {anonymized_id[:10]}...")
    return {"anonymized_id": anonymized_id, "status": "success"}

# IMPORTANT: All future calls to /log_insight/ and other endpoints MUST use this anonymized_id.

# Full Attention Vector Input to the SGD Classifier
full_input_text = f"Current State: {current_activity_desc}\nPast Memories: {context_str}"
attention_vector = transformer_extractor.encode_text(full_input_text)

# Prediction: X is the attention vector, y is the predicted state
predicted_state = model.predict(attention_vector.reshape(1, -1))[0]

# 
# Executed via the /feedback_update/ endpoint
true_label_encoded = encoder.transform([data.true_state])
model.partial_fit(
    latest_activity_vector.reshape(1, -1), # X (The vector that caused the error)
    true_label_encoded,                   # Y (The correct state)
    classes=np.arange(len(encoder.classes_))
)
# Executed inside the /predict_state/ endpoint
security_risk, security_alerts = check_security_risk(latest_visual_state, data.key_count, data.mouse_distance)

if security_risk == "CRITICAL":
    lock_workstation() # Calls ctypes.windll.user32.LockWorkStation() on Windows

return {"security_risk": security_risk, "security_alerts": security_alerts}

def hash_user_id(employee_id: str) -> str:
    SALT = "AuraDigitalTwinV1-Gov" 
    hasher = hashlib.sha256()
    hasher.update((employee_id + SALT).encode('utf-8')) 
    return hasher.hexdigest()

# prediction_api.py (The Logic to generate the anonymized_id)

import hashlib
from pydantic import BaseModel

# ... (hash_user_id function definition) ...

class AuthInput(BaseModel):
    employee_id: str 

@app.post("/register_user/")
async def register_user(data: AuthInput):
    """
    This endpoint executes your code logic:
    anonymized_id = hash_user_id("TEST_USER_AURA_101") 
    """
    # The system then generates the safe, anonymized key:
    anonymized_id = hash_user_id(data.employee_id)
    
    # Return the secure hash to the client for future use
    return {"anonymized_id": anonymized_id, "status": "success"}

