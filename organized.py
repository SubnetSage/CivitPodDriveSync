import os
import shutil
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import json
from datetime import datetime

# Function to authenticate with Google Drive using Service Account credentials
def authenticate_drive_api(credentials_json_path):
    creds = Credentials.from_service_account_file(credentials_json_path, scopes=["https://www.googleapis.com/auth/drive.file"])
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
def copy_photos_to_drive(service, source_folder, folder_id):
    if not os.path.exists("copied_files.txt"):
        open("copied_files.txt", "w").close()

    with open("copied_files.txt", "r") as file:
        copied_files = set(file.read().splitlines())

    new_files = [
        file_name for file_name in os.listdir(source_folder)
        if os.path.isfile(os.path.join(source_folder, file_name)) and file_name not in copied_files
    ]

    for file_name in new_files:
        file_path = os.path.join(source_folder, file_name)
        try:
            upload_to_drive(service, file_path, folder_id)
            with open("copied_files.txt", "a") as file:
                file.write(file_name + "\n")
        except Exception as e:
            print(f"Failed to upload {file_name}: {e}")

# Function to add an API token to a URL
def add_api_token(url, api_key):
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['token'] = api_key  # Add or update the token parameter
    new_query = urlencode(query_params, doseq=True)
    updated_url = parsed_url._replace(query=new_query)
    return urlunparse(updated_url)

# Function to download and move a model
def download_and_move_model(url, api_key):
    try:
        updated_url = add_api_token(url, api_key)
        command = f"wget -O temp_model.safetensors \"{updated_url}\""
        print(f"Downloading with the following command:\n{command}")
        os.system(command)

        destination_dir = "/workspace/stable-diffusion-webui/models/Stable-diffusion"
        destination_file = os.path.join(destination_dir, "model.safetensors")

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        shutil.move("temp_model.safetensors", destination_file)
        print(f"Model successfully moved to: {destination_file}")
    
    except Exception as e:
        print(f"Error: {e}")

# Function to save folder_id and api_key to a file
def save_config(folder_id, api_key):
    config = {
        "folder_id": folder_id,
        "api_key": api_key
    }
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

# Function to load folder_id and api_key from a file
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            return config.get("folder_id"), config.get("api_key")
    return None, None

# Main function to handle user input and execute the actions
def main():
    # Define the path to the credentials JSON in the /workspace/ folder
    credentials_json_path = "/workspace/credentials.json"
    
    if not os.path.exists(credentials_json_path):
        print(f"Service account credentials file not found at {credentials_json_path}. Exiting.")
        return
    
    try:
        # Authenticate using service account credentials
        drive_service = authenticate_drive_api(credentials_json_path)
        print("Google Drive authenticated successfully!")

        # Load saved config or ask for new config if not present
        folder_id, api_key = load_config()

        if not folder_id or not api_key:
            folder_id = input("Enter your Google Drive Folder ID: ")
            api_key = input("Enter your API key for downloading models: ")
            save_config(folder_id, api_key)

        # Get the current date for the folder name (format: YYYY-MM-DD)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Define the source folder based on the current date
        source_folder = f"/workspace/stable-diffusion-webui/outputs/txt2img-images/{current_date}"

        # Check if the folder exists
        if not os.path.exists(source_folder):
            print(f"Error: Folder {source_folder} does not exist.")
            return

        # Ask for action choice
        action = input("Choose an action: \n1. Download and Move a Model\n2. Copy Photos to Google Drive\nChoose 1 or 2: ")

        if action == "1":
            url = input("Enter the URL to download the model: ")
            download_and_move_model(url, api_key)

        if action == "2":
            print("Starting to copy photos to Google Drive...")
            while True:
                copy_photos_to_drive(drive_service, source_folder, folder_id)
                time.sleep(120)  # Wait for 2 minutes before uploading again

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
