import os
import zipfile
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# CONFIGURATION
AURA_VAULT_ID = "139ohKDb9zvcNgU4J6BIb_5AmwF2qxUi3"
SERVICE_ACCOUNT_FILE = 'drive_creds.json'
PROJECT_DIR = './'  # Path to your Aura Sentinel files

def create_project_zip():
    """Zips the current directory, excluding sensitive or bulky folders."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    zip_name = f"Aura_Sentinel_Backup_{timestamp}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_DIR):
            # Skip virtual environments and git history to save space
            if 'venv' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith(('.py', '.csv', '.html', '.json')) and file != SERVICE_ACCOUNT_FILE:
                    zipf.write(os.path.join(root, file), 
                               os.path.relpath(os.path.join(root, file), PROJECT_DIR))
    return zip_name

def upload_to_drive(file_name):
    """Uploads the zip file to the specified Google Drive folder."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name': file_name,
        'parents': [AURA_VAULT_ID]
    }
    media = MediaFileUpload(file_name, mimetype='application/zip')
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ [VAULT] Backup Successful. File ID: {file.get('id')}")
    
    # Cleanup local zip after upload
    os.remove(file_name)

if __name__ == "__main__":
    zip_file = create_project_zip()
    upload_to_drive(zip_file)
