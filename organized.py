import os
import time
import shutil
import streamlit as st
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

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
    st.success(f"Uploaded {file_name} with File ID: {uploaded_file.get('id')}")

# Function to copy photos to Google Drive every 5 minutes
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
            st.error(f"Failed to upload {file_name}: {e}")

# Function to add an API token to a URL
def add_api_token(url, api_key):
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
        st.info(f"Downloading with the following command:\n{command}")
        os.system(command)

        destination_dir = "/workspace/stable-diffusion-webui/models/Stable-diffusion"
        destination_file = os.path.join(destination_dir, "model.safetensors")

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        shutil.move("temp_model.safetensors", destination_file)
        st.success(f"Model successfully moved to: {destination_file}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit app logic
def main():
    st.title("Stable Diffusion Automation Tool")

    # Paste credentials.json
    credentials_json_text = st.text_area("Paste your Google Drive credentials JSON here")
    if credentials_json_text:
        try:
            credentials_json = eval(credentials_json_text)
            drive_service = authenticate_drive_api(credentials_json)
            st.success("Google Drive authenticated successfully!")

            # Get Google Drive Folder ID
            folder_id = st.text_input("Enter your Google Drive Folder ID")

            # API Key for downloading models
            api_key = st.text_input("Enter your API key for downloading models")

            # Select an action
            action = st.selectbox("Choose an action", ["Select an action", "Download and Move a Model", "Copy Photos to Google Drive"])
            
            if action == "Download and Move a Model":
                url = st.text_input("Paste the URL to download the model")
                if st.button("Download and Move Model"):
                    if url and api_key:
                        download_and_move_model(url, api_key)
                    else:
                        st.error("Please provide a URL and API key.")
            
            elif action == "Copy Photos to Google Drive":
                source_folder = "/workspace/stable-diffusion-webui/outputs"
                if st.button("Start Copying Photos"):
                    if folder_id:
                        st.info("Copying photos to Google Drive...")
                        copy_photos_to_drive(drive_service, source_folder, folder_id)
                    else:
                        st.error("Please provide a Google Drive Folder ID.")
        except Exception as e:
            st.error(f"Invalid JSON format: {e}")
    else:
        st.warning("Please paste your credentials JSON.")

if __name__ == "__main__":
    main()
