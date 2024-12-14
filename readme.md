## CivitPodDriveSync

This guide explains how to use a Python script to upload photos from a specific folder to your Google Drive and download a model from a URL to your RunPod instance.

**Requirements:**

* Python 3
* Google Drive API enabled for your project
* Service account credentials JSON file
* CivitAI API key for downloading models (optional)
* **Clone the GitHub repository:** [https://github.com/SubnetSage/CivitAI.git](https://github.com/SubnetSage/CivitAI.git)

**Installation:**

1. **Enable Google Drive API:** Follow the instructions on [https://developers.google.com/drive/api/quickstart/python](https://developers.google.com/drive/api/quickstart/python) to enable the Drive API for your project and download the service account credentials JSON file. Place this file in your `/workspace/` folder named `credentials.json`.

2. **Optional API Key:** If you plan to download models, obtain a CivitAI API key for the model source and update the script accordingly.

3. **Install libraries:** Open a terminal in your workspace and run:

```bash
pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
```

4. **Clone the GitHub repository:**

```bash
git clone https://github.com/SubnetSage/CivitAI.git
```

**Configuration:**

1. **Create a configuration file (optional):** The script can save and load configuration (folder ID and API key) to a file named `config.json`. This eliminates the need to enter details each time.

2. **Manual configuration:** If no configuration file exists, the script will prompt you to enter your Google Drive folder ID and API key (optional) when you first run it.

**Running the script:**

1. Open a terminal in your workspace folder.
2. Run the script with `python your_script_name.py`.

**Functionality:**

* The script authenticates with Google Drive using the service account credentials.
* It checks for a configuration file or prompts for folder ID and API key.
* It validates the provided Google Drive folder ID.
* You can choose one of two actions:

    * **Download and Move a Model (action 1):** Enter the URL of the model to download and provide your CivitAI API key (if required). The script will download the model and move it to the models folder under Stable Diffusion.

    * **Copy Photos to Google Drive (action 2):** Photos from a folder named with the current date (e.g., 2024-12-13) within `/workspace/stable-diffusion-webui/outputs/txt2img-images` will be uploaded to the specified Google Drive folder every 2 minutes (or whatever you specify in the script).

**Notes:**

* Ensure the source folder for uploading photos exists before running the script.
* Edit the script paths (`credentials.json`, folder structure) to match your setup.
* This script demonstrates basic functionalities. You can modify it to fit your specific needs.

**Additional Resources:**

* Google Drive API documentation: [https://developers.google.com/drive/api/quickstart/python](https://developers.google.com/drive/api/quickstart/python)
