import os
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed


#------------------------------------------------------------
def download_file(session, url, download_dir):
    """
    Helper function to download a single file.
    If the file already exists in the download directory, it will not be downloaded again.

    Args:
    - session (requests.Session): The session to use for downloading the file.
    - url (str): The URL of the file to download.
    - download_dir (str): The directory to download the file to.
    """

    # Get the file name from the URL
    file_name = url.split('/')[-1]
    file_path = os.path.join(download_dir, file_name)


    # Skip download if the file already exists
    if os.path.exists(file_path):
        return f"File {file_name} already exists in {download_dir}. Skipping download."
    else:
        # Attempt to download the file to the specified directory using the given session
        with session.get(url, stream=True) as response:
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                return f"Downloaded {file_name} to {download_dir}"
            else:
                return f"Failed to download {file_name}. Status code: {response.status_code}"
#------------------------------------------------------------


#------------------------------------------------------------
def download_files(urls, download_dir, num_workers=None):
    """
    Downloads each file from the given list of URLs to the specified directory using multiple workers.

    Args:
    - urls (list of str): The URLs of the files to download.
    - download_dir (str): The directory to download the files to.
    - num_workers (int, optional): The number of worker threads to use for downloading files. If None, the number
    """

    # STATUS MESSAGE
    print(f"\nDownloading {len(urls)} files to {download_dir}")

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    if num_workers is None:
        num_workers = os.cpu_count() or 4  # Fallback to 4 if os.cpu_count() returns None

    # Use a session to persist the connection for all requests
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Create a future for each URL
            futures = [executor.submit(download_file, session, url, download_dir) for url in urls]
            
            for future in as_completed(futures):
                print(future.result())
#------------------------------------------------------------
                



#------------------------------------------------------------
# Example usage
#------------------------------------------------------------
if __name__ == "__main__":

    from parse_urls_from_json import parse_urls_from_json

    proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    contractor_index_files = os.path.join(proj_root, 'data', 'Contractor_Index_Files')
    all_6xx_Jun_29 = os.path.join(contractor_index_files, 'all_6xx_Jun_29.json')
    download_dir = os.path.join(proj_root, 'data', 'temp_training')

    urls = parse_urls_from_json(all_6xx_Jun_29)
    download_files(urls, download_dir)  # Automatically determines the number of workers without specifying the num_workers argument
#------------------------------------------------------------

