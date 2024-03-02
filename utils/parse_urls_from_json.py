import json


#------------------------------------------------------------
def parse_urls_from_json(file_path):
    # Open the JSON file and load its content
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the base directory URL and the relative paths
    base_dir = data['basedir']
    rel_paths = data['relpaths']
    
    # Initialize an empty list to store the full URLs
    full_urls = []
    
    # Loop through each relative path
    for rel_path in rel_paths:
        # Form the full URL for the .mp4 file
        mp4_url = base_dir + rel_path
        # Replace .mp4 with .jsonl to form the second type of URL
        jsonl_url = mp4_url.replace('.mp4', '.jsonl')
        
        # Append both URLs to the list
        full_urls.append(mp4_url)
        full_urls.append(jsonl_url)
    
    # Return the list of URLs
    #return full_urls
        
    # Return 5 Urls for testing purposes TODO: switch this back to returning all urls when done testing
    return full_urls[:10]
#------------------------------------------------------------




#------------------------------------------------------------
# Example usage
#------------------------------------------------------------
if __name__ == "__main__":
    # Test the function with a sample JSON file
    #only print up to the first 5 url pairs (10 total urls to avoid cluttering the output)
    file_path = '../data/all_6xx_Jun_29.json' # BE SURE TO UPDATE THIS IF WE MOVE THIS SCRIPT
    urls = parse_urls_from_json(file_path)
    print(urls[:10])
#------------------------------------------------------------