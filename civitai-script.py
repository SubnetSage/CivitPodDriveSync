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

# Example usage
if __name__ == "__main__":
    api_key = input("Enter your API key: ").strip()
    while True:
        # Allow user to paste a link or exit
        url = input("\nPaste the URL (or type 'exit' to quit): ").strip()
        if url.lower() == "exit":
            print("Goodbye!")
            break
        
        try:
            # Process and print the updated link
            updated_url = add_api_token(url, api_key)
            print("\nUpdated URL:")
            print(updated_url)
        except Exception as e:
            print(f"Error processing the URL: {e}")
