import os
import pytest

import config

from nera.data_initialization.parse_urls_from_json import parse_urls_from_json
from nera.data_initialization.download_data_files import download_files

class TestDownloadDataFiles:


    @pytest.fixture
    def setup_data(self):
        # Setup data directory and file paths
        contractor_json_file = config.CONTRACTOR_JSON_FILES_DIR / 'all_6xx_Jun_29.json'
        download_dir = config.TEMP_TRAINING_DIR
        return contractor_json_file, download_dir
    

    def test_download_files(self, setup_data):

        contractor_json_file, download_dir = setup_data

        urls = parse_urls_from_json(contractor_json_file)
        download_files(urls, download_dir) 

        downloaded_files = os.listdir(download_dir) # Get a list of all files in the download directory
        url_filenames = [os.path.basename(url) for url in urls]  # Get the filenames of the URLs (i.e the last part of the URL, like https://www.example.com/file.mp4 -> file.mp4)

        # Assert that there is a file in the download directory whose basename matches each URL 
        assert all(url_filename in downloaded_files for url_filename in url_filenames), "There should be a file in the download directory for each file in the URLS list"