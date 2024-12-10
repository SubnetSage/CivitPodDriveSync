import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import time

# Define constants
OUTPUT_DIR = "/workspace/stable-diffusion-webui/outputs"
CREDENTIALS_FILE = "path/to/credentials.json"  # Replace with your path
COPIED_FILES_LOG = "copied_files.txt"

# Google Drive setup
def get_drive_service():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE)
    return build("drive", "v3", credentials=creds)

def upload_to_google_drive(service, folder_id, file_path):
    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"Uploaded: {file_path} (ID: {file.get('id')})")

def get_copied_files():
    if os.path.exists(COPIED_FILES_LOG):
        with open(COPIED_FILES_LOG, "r") as file:
            return set(file.read().splitlines())
    return set()

def log_copied_file(file_path):
    with open(COPIED_FILES_LOG, "a") as file:
        file.write(file_path + "\n")

# Main function to copy new files
def copy_new_photos_to_drive(folder_id):
    drive_service = get_drive_service()
    copied_files = get_copied_files()

    # Get list of all files in output directory
    for root, _, files in os.walk(OUTPUT_DIR):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Check if the file is already copied
            if file_path in copied_files:
                continue

            try:
                # Upload to Google Drive
                upload_to_google_drive(drive_service, folder_id, file_path)
                log_copied_file(file_path)  # Log the file as copied
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")

if __name__ == "__main__":
    folder_id = input("Enter your Google Drive folder ID: ").strip()
    while True:
        copy_new_photos_to_drive(folder_id)
        print("Waiting for 5 minutes...")
        time.sleep(300)  # Wait for 5 minutes
