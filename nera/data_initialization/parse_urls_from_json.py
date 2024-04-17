import json
import os

#from nera.utils.output_helpers import HORIZONTAL_LINE


# TODO - There are two additional URLS that are available for each Contractor link. Do we need to be using these? 
# They contain the game options, and the checkpoint zip file. 
# (-options.json and .zip respectively in place of .mp4)



#------------------------------------------------------------
def parse_urls_from_json(file_path, limit=None):
    """
    Extracts the URLs from the given JSON file and returns a list of URLs.

    Each dataset has several urls, but the basename of the .mp4 from the index file is a unique identifier.
    This basename will be the same for all urls in the same dataset, so we can use this to identify unique datasets)

    Args:
    - file_path (str): The path to the JSON file containing the URLs.
    - limit (int, optional): The number of URLs to extract. If None, all URLs will be extracted.
    """

    #STATUS MESSAGE
    print("\n--------------------------------------------")
    print("Attempting to extract URLs...\n")


    # Open the JSON file and load its content
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the base directory URL and the relative paths
    base_dir = data['basedir']
    rel_paths = data['relpaths']
    
    full_urls = []
    
    for rel_path in rel_paths:
        # Form the full URL for the .mp4 file
        mp4_url = base_dir + rel_path

        # Replace .mp4 with .jsonl to form the second type of URL
        jsonl_url = mp4_url.replace('.mp4', '.jsonl')

        full_urls.append(mp4_url)
        full_urls.append(jsonl_url)
    
    #Only use the first 5 datasets for testing purposes. TODO switch this back to using all datasets when done testing
    #full_urls = full_urls[:10]
    if limit is not None:
        full_urls = full_urls[:limit]

    
    # Get the unique dataset names from the list of URLs.
    urlFilenames = [os.path.basename(url).split('.')[0] for url in full_urls]
    dataset_names = list(set(urlFilenames))
        

    #STATUS MESSAGE
    print(f"Extracted {len(full_urls)} URLs for {len(set(dataset_names))} unique datasets from {file_path}")

    #avoid printing all the dataset names if there are too many (powershell apparently REALLY hates massive print statements)
    if len(set(dataset_names)) < 100:
        for name in dataset_names:
            print(name)
    print("--------------------------------------------\n")


    # Return the list of URLs
    return full_urls
#------------------------------------------------------------




#------------------------------------------------------------
# Example usage
#------------------------------------------------------------
if __name__ == "__main__":

    proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    contractor_index_files = os.path.join(proj_root, 'data', 'Contractor_Index_Files')
    #json_file = os.path.join(contractor_index_files, 'all_6xx_Jun_29.json')
    #json_file = os.path.join(contractor_index_files, 'all_9xx_Jun_29.json')
    json_file = os.path.join(contractor_index_files, '6xx_tree_chop.json')

    urls = parse_urls_from_json(json_file, limit=10)
    print("EXAMPLE RUN USING A LIMIT OF 10 URLS!")
    print(urls)
#------------------------------------------------------------
