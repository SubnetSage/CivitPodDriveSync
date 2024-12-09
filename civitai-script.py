import os
import shutil
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def add_api_token(url, api_key):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Add or update the token parameter
    query_params['token'] = api_key
    
    # Construct the new query string
    new_query = urlencode(query_params, doseq=True)
    
    # Build the updated URL
    updated_url = parsed_url._replace(query=new_query)
    return urlunparse(updated_url)

def download_and_move_model(url, api_key):
    try:
        # Process the URL to include the API token
        updated_url = add_api_token(url, api_key)
        
        # Download the file using wget
        command = f"wget -O temp_model.safetensors \"{updated_url}\""
        print("\nDownloading with the following command:")
        print(command)
        os.system(command)
        
        # Define the destination directory and file path
        destination_dir = "/workspace/stable-diffusion-webui/models/Stable-diffusion"
        destination_file = os.path.join(destination_dir, "model.safetensors")
        
        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Move and rename the file
        shutil.move("temp_model.safetensors", destination_file)
        print(f"\nModel successfully moved to: {destination_file}")
    
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    api_key = input("Enter your API key: ").strip()
    while True:
        # Allow user to paste a link or exit
        url = input("\nPaste the URL (or type 'exit' to quit): ").strip()
        if url.lower() == "exit":
            print("Goodbye!")
            break
        
        # Attempt to download and move the model
        download_and_move_model(url, api_key)
