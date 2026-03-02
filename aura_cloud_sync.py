import os
from google.cloud import storage
from datetime import datetime

# CONFIGURATION
BUCKET_NAME = "project-aura-vault" # Change to your actual bucket name
SERVICE_ACCOUNT_JSON = "/home/pi/aura-keys/service-account.json"
LOCAL_LOG_DIR = "/home/pi/.ros/log/latest/" # Default ROS 2 log path

def upload_to_aura_vault():
    try:
        # Initialize the GCS Client
        client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
        bucket = client.get_bucket(BUCKET_NAME)

        print(f"--- Project Aura: Cloud Sync Initiated ---")
        
        # Scan for ROS 2 log files
        for filename in os.listdir(LOCAL_LOG_DIR):
            if filename.endswith((".db3", ".mcap", ".log")):
                local_path = os.path.join(LOCAL_LOG_DIR, filename)
                
                # Create a unique cloud path using today's date
                date_str = datetime.now().strftime("%Y-%m-%d")
                cloud_path = f"telemetry/{date_str}/{filename}"
                
                blob = bucket.blob(cloud_path)
                
                print(f"Uploading {filename} to {BUCKET_NAME}...")
                blob.upload_from_filename(local_path)
                print(f"Success: {filename} is now in the cloud.")

    except Exception as e:
        print(f"Sentinel API Alert: Cloud Sync Failed. Error: {e}")

if __name__ == "__main__":
    upload_to_aura_vault()