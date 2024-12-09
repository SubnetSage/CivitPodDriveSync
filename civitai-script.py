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
    api_key = input("Enter your API key: ")
    urls = [
        "/api/download/models/12345?token=YOUR_TOKEN_HERE",
        "https://civitai.com/api/download/models/128713?type=Model&format=SafeTensor&size=pruned&fp=fp16"
    ]
    
    # Process each URL
    for url in urls:
        print(add_api_token(url, api_key))
