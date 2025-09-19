Here’s a cleaner, more user-focused rewrite of your README. I emphasized the time-saving purpose, organized structure, and made it easier for someone new to follow:

⸻

RunPod Stable Diffusion Automation

This tool helps you save time managing Stable Diffusion models and outputs on RunPod. Instead of wasting hours moving files around, the script handles model downloads, organizes them in the right directories, and automatically syncs generated images to Google Drive — so you can spend more time creating.

⸻

✨ What It Does
	1.	Model Management
	•	Download Stable Diffusion models directly from CivitAI using your API key.
	•	Automatically move them into the correct RunPod model directory.
	2.	Google Drive Sync
	•	Authenticate with a Google service account.
	•	Upload generated images from RunPod to a chosen Google Drive folder.
	3.	Auto Upload
	•	Monitor your RunPod output folder.
	•	Every 2 minutes, new images are automatically uploaded to Google Drive.
	4.	Easy Configuration
	•	Save your Google Drive folder ID and CivitAI API key once.
	•	Automatically reloads them from config.json in future runs.

⸻

🛠 Requirements
	•	Python packages: googleapiclient, google-auth, plus built-ins (os, shutil, json, time)
	•	RunPod environment with Stable Diffusion (A1111)
	•	Model directory: /workspace/stable-diffusion-webui/models/Stable-diffusion
	•	Output directory: /workspace/stable-diffusion-webui/outputs/txt2img-images
	•	Google Drive service account JSON credentials
	•	CivitAI API key

⸻

🚀 Setup
	1.	Upload your Google Drive credentials file (credentials.json) to /workspace/ in RunPod.
	2.	Make sure your RunPod Stable Diffusion instance is running with the expected directories.

⸻

▶ Usage

Run the script:

python script_name.py

First run setup

You’ll be asked for:
	•	Google Drive Folder ID (where images should upload)
	•	CivitAI API Key

These are saved in config.json for future runs.

⸻

🔄 Workflow Options
	1.	Download & Move Model
	•	Enter a CivitAI model URL.
	•	Script appends your API key, downloads it, and places it in the correct RunPod models folder.
	2.	Auto-Upload Photos
	•	Script watches the output folder for new images.
	•	Every 2 minutes, new files are uploaded to your Google Drive folder.

You can choose either or both based on your workflow.

⸻

⚙ Config File Example

{
  "folder_id": "your-google-drive-folder-id",
  "api_key": "your-civitai-api-key"
}


⸻

🧩 Troubleshooting
	•	Credential errors → Check credentials.json is in /workspace/ and valid.
	•	Drive folder issues → Ensure correct folder ID + service account permissions.
	•	Model download failures → Verify CivitAI link + API key.
	•	Directory mismatches → Make sure your RunPod folder paths match the ones in this README.

⸻

⸻

👉 Would you like me to also simplify the README further for non-technical users (like a step-by-step “do this, then this” quick start), or keep it developer-style as above?