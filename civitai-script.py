import os
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

def download_model(url, api_key):
    try:
        # Process the URL to include the API token
        updated_url = add_api_token(url, api_key)
        
        # Generate the wget command
        command = f"wget \"{updated_url}\""
        print("\nGenerated wget command:")
        print(command)
        
        # Execute the wget command
        os.system(command)
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
        
        # Attempt to download the model
        download_model(url, api_key)
