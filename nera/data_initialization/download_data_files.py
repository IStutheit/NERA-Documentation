"""
Grabs the urls from the contractor data to be downloaded and stored.
"""
import json
import os
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
#from nera.utils.output_helpers import HORIZONTAL_LINE

#------------------------------------------------------------
def check_urls(urls, session, limit=None):
    """
    ##Checks the availability of each URL in a list using a HEAD request, stopping when the limit of accessible URLs is reached.
    
    ---
    
    ### Args:
    > urls (list of str): The URLs to check.
    > session (requests.Session): The session used for making requests.
    > limit (int, optional): The maximum number of accessible URLs to find before stopping. If None, all URLs are checked.
    
    ### Returns:
    > dict: A dictionary with lists of 'accessible' and 'inaccessible' URLs.
    """
    results = {"accessible": [], "inaccessible": []}
    for url in urls:
        if limit is not None and len(results["accessible"]) >= limit:
            # Stop checking more URLs once the limit of accessible URLs is reached
            break
        try:
            response = session.head(url, allow_redirects=True)
            if response.status_code == 200:
                results["accessible"].append(url)
            else:
                results["inaccessible"].append(url)
        except requests.RequestException:
            results["inaccessible"].append(url)
    return results
#------------------------------------------------------------

#------------------------------------------------------------
def download_file(session, url, download_dir):
    """
    ## Helper function to download a single file.
    
    ---
    
    If the file already exists in the download directory, it will not be downloaded again.
    If the file is successfully downloaded, a success message is returned along with the file path.
    If the download fails, a failure message is returned along with None.

    ---

    ### Args:
    
    >session (requests.Session): The session to use for downloading the file.
    
    >url (str): The URL of the file to download.
    
    >download_dir (str): The directory to download the file to.

    ### Returns:
    > tuple: A tuple containing the result message and the file path (or None if the download failed).
    
    """
    # Get the file name from the URL
    file_name = url.split('/')[-1]
    file_path = os.path.join(download_dir, file_name)

    # Skip download if the file already exists
    if os.path.exists(file_path):
        return f"File {file_name} already exists in {download_dir}. Skipping download.", None
    else:
        # Attempt to download the file to the specified directory using the given session
        with session.get(url, stream=True) as response:
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                return f"Downloaded {file_name} to {download_dir}", file_path
            else:
                return f"Failed to download {file_name}. Status code: {response.status_code}", None

#------------------------------------------------------------


#------------------------------------------------------------
def download_files(urls, download_dir, limit=None, num_workers=None):
    """
    ##Downloads each file from the given list of URLs to the specified directory using multiple workers.
    
    ---
    
    Tracks downloaded files and writes an index of downloaded file paths to a JSON file.
    Summarizes the download status.
    
    ---

    ###Args:
    
    >urls (list of str): The URLs of the files to download.
    
    >download_dir (str): The directory to download the files to.
    
    >num_workers (int, optional): The number of worker threads to use for downloading files. If None, the number of workers is determined by the system's CPU count.
    
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    if num_workers is None:
        num_workers = os.cpu_count() or 4  # Fallback to 4 if os.cpu_count() returns None

    results = {
        "downloaded": [],
        "skipped": [],
        "unavailable": [],  
        "failed": []
    }

    downloaded_files_index = []  # List to keep track of successfully downloaded files


    #STATUS MESSAGE
    print("\n--------------------------------------------")
    print("Checking the availability of URLs...")

    # Check the availability of each URL
    with requests.Session() as session:
        # Pass the limit to the check_urls function
        url_status = check_urls(urls, session, limit=limit)
        results["unavailable"] = url_status["inaccessible"]
        urls = url_status["accessible"]


    # If a limit is specified, only download the first 'limit' files. If there are fewer available files than the limit, download all available files, and adjust the limit message.
    if limit is not None:
        if len(urls) > limit:
            urls = urls[:limit]
            print(f"{len(urls)} files were available, but limiting to {limit} files per request.") #STATUS MESSAGE
        elif len(urls) < limit:
            print(f"Only {len(urls)} files were available, even though the limit was set to {limit}.") #STATUS MESSAGE

    
    #STATUS MESSAGE
    print(f"Attempting to download files...\n")

    with requests.Session() as session, ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(download_file, session, url, download_dir): url for url in urls}
        
        for future in as_completed(futures):
            result, file_path = future.result()
            if "already exists" in result:
                results["skipped"].append(result)
            elif file_path:  # Adjusted to check if file_path is not None
                results["downloaded"].append(result)
                downloaded_files_index.append(file_path)  # Track the file path
            else:
                results["failed"].append(result)

    #sort each list in the results dictionary alphabetically
    for key, value in results.items():
        results[key] = sorted(value)

    # Write the list of downloaded files to a JSON file
    with open(os.path.join(download_dir, 'NERA_TRAINING_DATA_INDEX_FILE.json'), 'w') as f:
        #json.dump(results["downloaded"], f)
        json.dump(downloaded_files_index, f)

    
    #STATUS MESSAGE
    print("Download Summary:")
    for key, value in results.items():
        print(f"\n{key.capitalize()} ({len(value)}):")
        for message in value:
            print(f"- {message}")
    print("--------------------------------------------\n")

#------------------------------------------------------------
                



#------------------------------------------------------------
# Example usage
#------------------------------------------------------------
if __name__ == "__main__":

    from parse_urls_from_json import parse_urls_from_json

    proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    contractor_index_files = os.path.join(proj_root, 'data', 'Contractor_Index_Files')
    #json_file = os.path.join(contractor_index_files, 'all_6xx_Jun_29.json')
    #json_file = os.path.join(contractor_index_files, 'all_9xx_Jun_29.json')
    json_file = os.path.join(contractor_index_files, '6xx_tree_chop.json')

    download_dir = os.path.join(proj_root, 'data', 'tree_chop_data')

    urls = parse_urls_from_json(json_file)
    download_files(urls, download_dir, limit=10)  # Automatically determines the number of workers without specifying the num_workers argument
#------------------------------------------------------------

