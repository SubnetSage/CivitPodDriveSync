import os
import time
import shutil
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from datetime import datetime

# Function to authenticate with Google Drive
def authenticate_drive_api(credentials_json):
    creds = Credentials.from_service_account_info(credentials_json, scopes=["https://www.googleapis.com/auth/drive"])
    service = build('drive', 'v3', credentials=creds)
    return service

# Function to upload a file to Google Drive
def upload_to_drive(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    media = MediaFileUpload(file_path, resumable=True)
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"Uploaded {file_name} with File ID: {uploaded_file.get('id')}")

# Function to copy photos to Google Drive every 2 minutes
def copy_photos_to_drive(service, source_folder, folder_id, uploaded_files):
    new_files = [
        file_name for file_name in os.listdir(source_folder)
        if os.path.isfile(os.path.join(source_folder, file_name)) and file_name not in uploaded_files
    ]

    for file_name in new_files:
        file_path = os.path.join(source_folder, file_name)
        try:
            upload_to_drive(service, file_path, folder_id)
            uploaded_files.add(file_name)  # Keep track of uploaded files
        except Exception as e:
            print(f"Failed to upload {file_name}: {e}")

    # Save the updated list of uploaded files to avoid re-uploading
    with open("uploaded_files.pkl", "wb") as file:
        pickle.dump(uploaded_files, file)

# Load previously uploaded files from the pickle file
def load_uploaded_files():
    if os.path.exists("uploaded_files.pkl"):
        with open("uploaded_files.pkl", "rb") as file:
            return pickle.load(file)
    return set()

# Main function
def main():
    # Specify the path to your Google Drive credentials JSON file
    credentials_json_path = "/workspace/credentials.json"  # Update with the correct path if needed
    
    # Load credentials and authenticate with Google Drive
    try:
        with open(credentials_json_path, "r") as file:
            credentials_json = file.read()
        credentials_json = eval(credentials_json)
        drive_service = authenticate_drive_api(credentials_json)
        print("Google Drive authenticated successfully!")

        # Ask for Google Drive folder ID and API key
        folder_id = input("Enter your Google Drive Folder ID: ").strip()
        api_key = input("Enter your API key for downloading models: ").strip()

        # Load previously uploaded files
        uploaded_files = load_uploaded_files()

        # Get the current date for the folder name (format: YYYY-MM-DD)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Define the source folder based on the current date
        source_folder = f"/workspace/stable-diffusion-webui/outputs/txt2img-images/{current_date}"

        # Check if the folder exists
        if not os.path.exists(source_folder):
            print(f"Error: Folder {source_folder} does not exist.")
            return

        # Start copying photos to Google Drive every 2 minutes
        while True:
            copy_photos_to_drive(drive_service, source_folder, folder_id, uploaded_files)
            time.sleep(120)  # Sleep for 2 minutes

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
