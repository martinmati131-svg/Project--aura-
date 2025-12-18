# prediction_api.py (New Mobile Data Model)
from pydantic import BaseModel, Field
from typing import Optional

class MobileInsightLog(BaseModel):
    # Core Identity (Secured via PPD)
    user_hash: str = Field(..., description="Anonymized ID of the user (e.g., SHA256 hash).")

    # New Location/Context Senses
    is_commute: bool = Field(False, description="True if movement patterns suggest a commute.")
    is_home_base: bool = Field(False, description="True if user is at their primary home location.")
    
    # New Wellness Senses
    sleep_duration_hours: Optional[float] = Field(None, description="Total hours of sleep tracked.")
    resting_hr_bpm: Optional[int] = Field(None, description="Average resting heart rate.")
    
    # Simple Mobile Activity
    screen_time_minutes: int = Field(0, description="Total screen-on time since last sync.")

    # Status update for security layer
    is_mobile_active: bool = Field(False, description="True if the mobile app is open/active.")

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
# prediction_api.py (Add this new function)

def generate_session_summary(recent_context: str, last_activity: str) -> str:
    """
    Simulates calling a Generative AI model to summarize the user's past work.
    
    In a real system, this prompt would be sent to an LLM:
    "You are a productivity coach. Summarize the user's last focused session 
    based on the following context and last file worked on. Be encouraging."
    """
    if not recent_context:
        return "You were away for a while! Let's get started on those power dreams."

    # Use a creative prompt that integrates the Vector DB context
    summary_prompt = (
        f"Aura has analyzed your recent work context. Your mind was last focused on: "
        f"{recent_context.split(' | ')[0]}. " 
        f"You were primarily editing the file: '{last_activity}'. "
        f"Recommendation: Review your last commit message or the file's top section to quickly regain flow."
    )
    
    # In a real environment, the LLM would turn this prompt into a smooth paragraph.
    return summary_prompt

# --- Modify the /predict_state/ endpoint to include the summary function ---

@app.post("/predict_state/")
async def predict_state(data: ActivityInput):
    # ... (Sentinel Check and Prediction steps remain the same) ...

    predicted_state = model.predict(full_attention_vector.reshape(1, -1))[0]
    
    # --- PROACTIVE INTERVENTION LOGIC ---
    proactive_summary = ""
    # Only generate a summary if the user has been predicted "Absent" (returning to work)
    # AND if the previous state was "Focused"
    if latest_visual_state == 'focused' and predicted_state == 'focused': # Checking for active return to work
        
        # Use a simplified check to see if the user was recently inactive
        if data.key_count < 5 and data.mouse_distance < 10: 
            # If input is low but user is now visually present, they likely just sat down.
            # Generate the summary to bridge the context gap.
            proactive_summary = generate_session_summary(
                context_str, # Context retrieved from the Vector DB
                data.active_app # The file they are currently in
            )

    return {
        "predicted_state": predicted_state,
        "confidence": round(float(confidence), 2),
        "visual_sense": latest_visual_state,
        "security_risk": security_risk,
        "proactive_summary": proactive_summary # <-- NEW FIELD
    }

# prediction_api.py (New Mobile Endpoint)

@app.post("/log_mobile_insight/")
async def log_mobile_insight(data: MobileInsightLog):
    """
    Receives periodic, anonymized wellness and context data from the Mobile Sense Agent.
    This data is used to enrich the centralized predictive models (e.g., Burnout).
    """
    
    # --- ENTERPRISE LOGGING (Simulated) ---
    # In a real system, this data would go into a dedicated Wellness/Context DB table.
    try:
        log_entry = (
            f"{datetime.now().isoformat()},"
            f"{data.user_hash},"
            f"Commute:{data.is_commute},"
            f"Sleep:{data.sleep_duration_hours or 'N/A'},"
            f"HR:{data.resting_hr_bpm or 'N/A'},"
            f"ScreenTime:{data.screen_time_minutes}\n"
        )
        with open("mobile_context_log.csv", "a") as f:
            f.write(log_entry)
            
        print(f"📱 MOBILE INSIGHT LOGGED for user {data.user_hash[:6]}: Sleep {data.sleep_duration_hours}h.")
        
    except Exception as e:
        # PII violation or bad data is common on mobile, so log exceptions carefully.
        print(f"ERROR logging mobile data: {e}")
        return {"status": "error", "message": "Failed to log data"}

    return {"status": "success", "message": "Mobile context logged successfully."}

# prediction_api.py (New Pydantic model)

class IntentionInput(BaseModel):
    user_hash: str = Field(..., description="Anonymized ID of the user.")
    intention_text: str = Field(..., description="The user's declared top goal for the session/day.")
    
# --- New Intention Endpoint ---

@app.post("/set_intention/")
async def set_intention(data: IntentionInput):
    """
    Receives and logs the user's top intention (powerdream) for the current session.
    This intention is used to guide the Prediction Engine and Proactive Coach.
    """
    
    # --- ENTERPRISE LOGGING (Simulated) ---
    # In a real system, this would be stored in a dedicated, quickly accessible
    # database (like Redis or a fast-lookup table) mapped to the user_hash.
    try:
        log_entry = (
            f"{datetime.now().isoformat()},"
            f"{data.user_hash},"
            f"'{data.intention_text}'\n"
        )
        with open("daily_intentions_log.csv", "a", encoding="utf-8") as f:
            f.write(log_entry)
            
        print(f"🎯 INTENTION SET for user {data.user_hash[:6]}: '{data.intention_text[:30]}...'")
        
    except Exception as e:
        print(f"ERROR setting intention: {e}")
        return {"status": "error", "message": "Failed to set intention."}

    return {"status": "success", "message": "Intention set successfully."}
# prediction_api.py (Inside @app.post("/predict_state/") function)

# 1. RETRIEVE CURRENT INTENTION (Simulated lookup)
# In production, you would query the fast intention storage here.
# For the prototype, assume we have a way to fetch the last intention string.
current_intention = get_last_intention_from_log(data.user_hash) # Function to read the last entry

# 2. ENHANCE THE ATTENTION VECTOR INPUT
current_activity_desc = (
    f"App: {data.active_app}. Keys: {data.key_count}. Mouse: {data.mouse_distance}. "
    f"Visual: '{latest_visual_state}'. "
    f"USER INTENTION: '{current_intention}'" # <--- NEW INPUT
)

# 3. Transformer creates the Attention Vector based on the Intention:
full_input_text = f"Current State: {current_activity_desc}\nPast Memories: {context_str}"
attention_vector = transformer_extractor.encode_text(full_input_text)
# prediction_api.py (Add new Pydantic model)
class LocationCheckInput(BaseModel):
    user_hash: str = Field(..., description="Anonymized ID of the user.")
    current_latitude: float
    current_longitude: float
    is_work_location: bool = Field(False, description="Flag set by mobile app's geo-fence.")
    
# --- New Location Check Endpoint ---

@app.post("/check_location_push/")
async def check_location_push(data: LocationCheckInput):
    """
    Called by the Mobile Sense Agent to check if a Proactive Push (Intention reminder) 
    should be sent based on location and previous state.
    """
    
    # 1. CRITICAL CONTEXT CHECK (Was the user just traveling/away?)
    # We assume the push should only occur when they transition *into* work mode.
    if not data.is_work_location:
        return {"send_push": False, "message": "User is not at a designated work location."}

    # 2. RETRIEVE LATEST INTENTION (From the log/cache created earlier)
    # This simulates fetching the user's previously set 'powerdream' goal.
    try:
        # Placeholder function to retrieve the last goal
        last_intention = get_last_intention_from_log(data.user_hash) 
    except Exception:
        return {"send_push": False, "message": "No active intention found."}


    # 3. INTERVENTION LOGIC (Push Rule)
    # Rule: If the user just arrived at a work location AND has a pending intention.
    if last_intention and data.is_work_location:
        
        push_message = (
            f"🧠 Welcome! Time to tackle your Power Dream. "
            f"Your focus goal is: '{last_intention}'"
        )
        
        # In a real system, you would set a flag in the central DB 
        # to mark the intention as "prompted" to avoid spamming the user.
        
        return {
            "send_push": True, 
            "message": "Work location arrival detected.",
            "push_title": "Aura Flow Coach: Goal Reminder",
            "push_body": push_message
        }

    return {"send_push": False, "message": "Work location reached, but no intention pending."}
# prediction_api.py (Add new endpoint)
import csv
from collections import defaultdict
from datetime import datetime, timedelta

@app.get("/get_wellness_report/")
async def get_wellness_report(user_hash: str, days: int = 7):
    """
    Calculates the Burnout KPI for a specific user over the last N days.
    """
    
    # 1. AGGREGATE DESKTOP (Focus Time)
    focus_data = defaultdict(lambda: 0)
    # [timestamp, user_hash, focus_minutes, distracted_minutes, security_alerts]
    try:
        with open("central_insight_log.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 3 or row[1].strip() != user_hash: continue
                focus_data[user_hash] += int(row[2].strip()) # Total focus minutes
    except FileNotFoundError: pass

    # 2. AGGREGATE MOBILE (Wellness Data)
    wellness_data = defaultdict(lambda: {'sleep': 0, 'hr': 0, 'count': 0})
    # [timestamp, user_hash, Commute, Sleep, HR, ScreenTime]
    try:
        with open("mobile_context_log.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 5 or row[1].strip() != user_hash: continue
                
                sleep = float(row[3].split(':')[1]) if row[3].split(':')[1].replace('.', '', 1).isdigit() else 0
                hr = int(row[4].split(':')[1]) if row[4].split(':')[1].isdigit() else 0
                
                if sleep > 0 and hr > 0:
                    wellness_data[user_hash]['sleep'] += sleep
                    wellness_data[user_hash]['hr'] += hr
                    wellness_data[user_hash]['count'] += 1
    except FileNotFoundError: pass


    # 3. CALCULATE THE BURN OUT SCORE (The KPI)
    total_focus_minutes = focus_data[user_hash]
    
    if wellness_data[user_hash]['count'] == 0:
         return {"error": "Insufficient wellness data to calculate KPI."}
        
    avg_sleep = wellness_data[user_hash]['sleep'] / wellness_data[user_hash]['count']
    avg_hr = wellness_data[user_hash]['hr'] / wellness_data[user_hash]['count']
    
    # Assumptions for 7-day period: 8 hours/day (56 hours) available work time.
    total_available_minutes = days * 8 * 60 

    # --- Burnout Score Calculation ---
    # Focus Ratio (Risk Factor): How much time was spent focused vs. available time
    focus_ratio = total_focus_minutes / total_available_minutes 

    # Recovery Ratio (Mitigation Factor): Sleep Quality / Stress (Inverse HR)
    recovery_ratio = avg_sleep / avg_hr

    # Burnout Score: (Focus/Risk) - (Recovery/Mitigation)
    burnout_score = focus_ratio - recovery_ratio 
    
    # Scale and interpret the score (e.g., 0.05 is High Risk)
    
    return {
        "user_hash": user_hash,
        "total_focus_minutes": total_focus_minutes,
        "average_sleep_hours": round(avg_sleep, 2),
        "average_resting_hr": round(avg_hr, 1),
        "burnout_score_raw": round(burnout_score, 4),
        "risk_level": "HIGH" if burnout_score > 0.05 else "LOW" # Simple threshold
    }
# prediction_api.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_welcome_email(recipient_email, activation_key):
    """
    Sends the automated onboarding email via SendGrid API.
    """
    message = Mail(
        from_email='onboarding@powerdreams.shop',
        to_emails=recipient_email,
        subject='Your Aura Digital Twin is Ready 🚀',
        html_content=f"""
        <h1>Welcome to the Flow State!</h1>
        <p>Thank you for your purchase. Your Aura Digital Twin is ready to help you achieve your power dreams.</p>
        <p><strong>Your Unique Activation Key:</strong> {activation_key}</p>
        <p><strong>Next Steps:</strong></p>
        <ul>
            <li>Download the Installer: <a href='https://powerdreams.shop/download'>Click Here</a></li>
            <li>Run the 'deploy_aura.ps1' script.</li>
            <li>Input your activation key when prompted.</li>
        </ul>
        <p>Stay focused, <br>The Aura Team</p>
        """
    )
    try:
        # You would store your API Key in an environment variable for security
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# prediction_api.py (Aura Wellness Module)

@app.get("/get_focus_fuel/")
async def get_focus_fuel(user_hash: str, cognitive_load: str):
    """
    Suggests a recipe from the 'my-recipes' library based on the user's current 
    mental state (High Load, Fatigue, or Pre-Focus).
    """
    
    # Logic: Match recipe tags (from your GitHub repo) to cognitive states
    if cognitive_load == "HIGH_FATIGUE":
        # Suggest something light and restorative
        suggestion = {"recipe": "Salmon & Avocado Bowl", "benefit": "Omega-3s for brain recovery"}
    elif cognitive_load == "PRE_DEEP_WORK":
        # Suggest slow-release energy
        suggestion = {"recipe": "Quinoa Power Salad", "benefit": "Stable glucose for 4-hour focus"}
    else:
        suggestion = {"recipe": "Quick Protein Shake", "benefit": "Rapid fuel for short breaks"}

    return {
        "user_hash": user_hash,
        "recommendation": suggestion,
        "source": "https://github.com/martinmati131-svg/my-recipes"
    }
