import json
import os
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from nera.utils.output_helpers import HORIZONTAL_LINE

#------------------------------------------------------------
def check_urls(urls, session):
    """
    Checks the availability of each URL in a list using a HEAD request.
    Args:
    - urls (list of str): The URLs to check.
    - session (requests.Session): The session used for making requests.
    Returns:
    - dict: A dictionary with lists of 'accessible' and 'inaccessible' URLs.
    """
    results = {"accessible": [], "inaccessible": []}
    for url in urls:
        try:
            response = session.head(url, allow_redirects=True)
            if response.status_code == 200:
                results["accessible"].append(url)
            else:
                results["inaccessible"].append(url)
        except requests.RequestException as e:
            results["inaccessible"].append(url)
    return results
#------------------------------------------------------------

#------------------------------------------------------------
def download_file(session, url, download_dir):
    """
    Download a single file.
    If the file already exists in the download directory, it will not be downloaded again.
    If the file is successfully downloaded, a success message is returned along with the file path.
    If the download fails, a failure message is returned along with None.

    Args:
    - session (requests.Session): The session to use for downloading the file.
    - url (str): The URL of the file to download.
    - download_dir (str): The directory to download the file to.

    Returns:
    - tuple: A tuple containing the result message and the file path (or None if the download failed).
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
def download_files(urls, download_dir, num_workers=None):
    """
    Downloads each file from the given list of URLs to the specified directory using multiple workers.
    Tracks downloaded files and writes an index of downloaded file paths to a JSON file.
    Summarizes the download status.

    Args:
    - urls (list of str): The URLs of the files to download.
    - download_dir (str): The directory to download the files to.
    - num_workers (int, optional): The number of worker threads to use for downloading files. If None, the number of workers is determined by the system's CPU count.
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    if num_workers is None:
        num_workers = os.cpu_count() or 4  # Fallback to 4 if os.cpu_count() returns None

    results = {
        "downloaded": [],
        "unavailable": [],  
        "skipped": [],
        "failed": []
    }

    downloaded_files_index = []  # List to keep track of successfully downloaded files


    #STATUS MESSAGE
    print("\n" + HORIZONTAL_LINE)
    print(f"Attempting to download {len(urls)} files to {download_dir}...\n")


    # Check the availability of each URL
    with requests.Session() as session:
        url_status = check_urls(urls, session)
        results["unavailable"] = url_status["inaccessible"]
        #remove the unavailable urls from the list of urls
        urls = url_status["accessible"]

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
    print(HORIZONTAL_LINE + "\n")

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
    download_files(urls, download_dir)  # Automatically determines the number of workers without specifying the num_workers argument
#------------------------------------------------------------

