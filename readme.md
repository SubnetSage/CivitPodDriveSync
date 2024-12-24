Absolutely, here's the updated readme file with step-by-step instructions for the code:

```markdown
# Stable Diffusion Automation Script for RunPod

This script automates the process of downloading Stable Diffusion models from CivitAI, organizing them in the appropriate directories, and managing the workflow of generating and uploading images from a Stable Diffusion instance hosted on RunPod.

---

## Features

1. **Model Management**:
    - Downloads Stable Diffusion models from CivitAI using API tokens.
    - Automatically moves the downloaded models to the correct directory on RunPod.

2. **Google Drive Integration**:
    - Authenticates with Google Drive via a service account.
    - Uploads generated images from RunPod's Stable Diffusion output directory to a specified Google Drive folder.

3. **Automated Photo Sync**:
    - Continuously monitors RunPod's output directory for new images and uploads them to Google Drive every 2 minutes.

4. **Configuration Management**:
    - Saves and loads the Google Drive folder ID and CivitAI API key for seamless setup.

---

## Requirements

1. **Python Libraries**:
    - `googleapiclient`
    - `google-auth`
    - `os`, `shutil`, `json`, `time`

2. **RunPod Environment**:
    - Stable Diffusion A111 instance hosted on RunPod.
    - Output directory for images: `/workspace/stable-diffusion-webui/outputs/txt2img-images/<YYYY-MM-DD>`

3. **Google Drive Credentials**:
    - A service account JSON file with the required permissions to access the target Google Drive folder.

4. **CivitAI API Key**:
    - A valid API key to authenticate and download models.

---

## Setup and Usage

### 1. Prepare Environment

1. Place your Google service account credentials file (`credentials.json`) in the `/workspace/` directory on RunPod.
2. Ensure the Stable Diffusion instance on RunPod is running and has access to the required directories:
    - `/workspace/stable-diffusion-webui/models/Stable-diffusion`
    - `/workspace/stable-diffusion-webui/outputs/txt2img-images`

### 2. Run the Script

```bash
python script_name.py
```

### 3. Initial Configuration
- On the first run, you will be prompted to provide:
    - **Google Drive Folder ID**: The ID of the Drive folder where images will be uploaded.
    - **CivitAI API Key**: Your API key to download models.
- These details are saved in a `config.json` file for future use.

---

## Workflow

### 1. Download and Organize Models (Option 1)

- Select the **Download and Move a Model** option.
- Provide the URL of the model on CivitAI.
- The script will:
    - Append your API key to the URL.
    - Download the model to a temporary location.
    - Move the model to the `/workspace/stable-diffusion-webui/models/Stable-diffusion/` directory on RunPod.

### 2. Upload Generated Photos to Google Drive (Option 2)

- Select the **Copy Photos to Google Drive** option.
- The script will monitor the output directory (`/workspace/stable-diffusion-webui/outputs/txt2img-images/<YYYY-MM-DD>`) for new images and upload them to the specified Google Drive folder every 2 minutes.

**Note:** You can choose to run either option (1 or 2) based on your needs.

---

## Configuration File

The script saves configuration details in `config.json`:
```json
{
  "folder_id": "Your Google Drive Folder ID",
  "api_key": "Your CivitAI API Key"
}
```

---

## Notes

- Ensure the necessary directories exist before running the script. If a required folder or file is missing, the script will handle it gracefully and retry after the defined interval (e.g., 2 minutes for photo uploads).
- Verify that your service account has the correct permissions for read/write access to the Google Drive folder.

---

## Troubleshooting

1. **Credential Errors**:
    - Ensure `credentials.json` is placed in the `/workspace/` directory and contains valid service account credentials.

2. **Folder Access Issues**:
    - Verify the Google Drive folder ID and ensure the service account has access.

3. **Model Download Failures**:
    - Ensure the CivitAI URL and API key are correct.

4. **RunPod Directory Issues**:
    - Verify the directory structure on RunPod matches the expected paths.

---

## License

This project is licensed
