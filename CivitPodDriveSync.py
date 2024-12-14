import os
import shutil
import time
import json
import subprocess
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# Function to authenticate with Google Drive using Service Account credentials
def authenticate_drive_api(credentials_json_path):
    creds = Credentials.from_service_account_file(credentials_json_path, scopes=["https://www.googleapis.com/auth/drive"])  # Updated scope for full access
    service = build('drive', 'v3', credentials=creds)
    return service

# Function to validate Google Drive folder access
def validate_folder(service, folder_id):
    try:
        folder = service.files().get(fileId=folder_id, fields="id, name").execute()
        print(f"Successfully accessed folder: {folder.get('name')} (ID: {folder.get('id')})")
        return True
    except Exception as e:
        print(f"Failed to access folder with ID {folder_id}: {e}")
        if "forbidden" in str(e).lower():
            print("Ensure that the service account has been granted access to this folder.")
        return False

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

# Function to clone a repository into a specified directory
def clone_repository(repo_url, target_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)  # Ensure the target directory exists
        command = f"git clone {repo_url} {target_dir}"
        print(f"Cloning repository with the following command:\n{command}")
        os.system(command)
        print(f"Repository successfully cloned into: {target_dir}")
    except Exception as e:
        print(f"Failed to clone repository: {e}")

# Main function to handle user input and execute the actions
def main():
    # Define the path to the credentials JSON in the /workspace/ folder
    credentials_json_path = "/workspace/credentials.json
