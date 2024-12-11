import os
import json
import time
import shutil
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# Authenticate Google Drive using pasted credentials
def authenticate_drive_api(credentials_json):
    # Write the credentials to a temporary file
    temp_credentials_file = "temp_credentials.json"
    with open(temp_credentials_file, "w") as f:
        json.dump(credentials_json, f)

    # Authenticate using the temporary credentials file
    creds = Credentials.from_service_account_file(temp_credentials_file, scopes=["https://www.googleapis.com/auth/drive"])
    service = build('drive', 'v3', credentials=creds)

    # Clean up the temporary file
    os.remove(temp_credentials_file)
    return service

# Upload a file to Google Drive
def upload_to_drive(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    media = MediaFileUpload(file_path, resumable=True)
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"Uploaded {file_name} with File ID: {uploaded_file.get('id')}")

# Copy photos to Google Drive every 5 minutes
def copy_photos_to_drive(service, source_folder, folder_id):
    while True:
        print("Checking for new files...")
        for file_name in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file_name)
            if os.path.isfile(file_path):
                try:
                    upload_to_drive(service, file_path, folder_id)
                    # Optionally delete the file after uploading
                    # os.remove(file_path)
                except Exception as e:
                    print(f"Failed to upload {file_name}: {e}")
        print("Waiting for 5 minutes...")
        time.sleep(300)  # Wait for 5 minutes

# Add an API token to a URL
def add_api_token(url, api_key):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['token'] = api_key  # Add or update the token parameter
    new_query = urlencode(query_params, doseq=True)
    updated_url = parsed_url._replace(query=new_query)
    return urlunparse(updated_url)

# Download a model and move it to the destination
def download_and_move_model(url, api_key):
    try:
        updated_url = add_api_token(url, api_key)
        command = f"wget -O temp_model.safetensors \"{updated_url}\""
        print("\nDownloading with the following command:")
        print(command)
        os.system(command)

        destination_dir = "/workspace/stable-diffusion-webui/models/Stable-diffusion"
        destination_file = os.path.join(destination_dir, "model.safetensors")

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        shutil.move("temp_model.safetensors", destination_file)
        print(f"\nModel successfully moved to: {destination_file}")
    
    except Exception as e:
        print(f"Error: {e}")

# Main logic
if __name__ == "__main__":
    # Accept the credentials.json content as input
    print("Paste the contents of your credentials.json file below and press Enter twice:")
    credentials_input = ""
    while True:
        line = input()
        if not line.strip():  # Empty line indicates end of input
            break
        credentials_input += line
    try:
        credentials_json = json.loads(credentials_input)
    except json.JSONDecodeError:
        print("Invalid JSON. Please try again.")
        exit(1)

    # Authenticate Google Drive
    drive_service = authenticate_drive_api(credentials_json)

    # Get Google Drive Folder ID
    folder_id = input("Enter your Google Drive Folder ID: ").strip()

    # API Key for downloading models
    api_key = input("Enter your API key for downloading models: ").strip()

    # Source folder for copying photos
    source_folder = "/workspace/stable-diffusion-webui/outputs"

    # Start file operations
    while True:
        print("\nOptions:")
        print("1. Download and move a model")
        print("2. Copy photos to Google Drive (runs every 5 minutes)")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            url = input("\nPaste the URL to download the model: ").strip()
            download_and_move_model(url, api_key)
        elif choice == "2":
            copy_photos_to_drive(drive_service, source_folder, folder_id)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
