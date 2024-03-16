import config
import os
import pytest
import sys

# Add the parent directory to the sys.path so that we can import modules from the nera package
# This will get cleaned up later, but package structure is still in flux atm.
# TODO - clean up sys.path manipulation in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from nera.data_initialization.parse_urls_from_json import parse_urls_from_json

class TestParseUrlsFromJson:

    @pytest.fixture
    def setup_data(self):
        # Setup data directory and file paths
        contractor_json_file = config.CONTRACTOR_JSON_FILES_DIR / 'all_6xx_Jun_29.json'
        return contractor_json_file

    def test_parse_urls_from_json(self, setup_data):

        contractor_json_file = setup_data
        
        urls = parse_urls_from_json(contractor_json_file) # Parse URLs from the JSON file
        
        assert isinstance(urls, list), "URLs should be in a list"
        assert len(urls) > 0, "URLs list should not be empty"
        assert all(isinstance(url, str) for url in urls), "All elements in the list should be strings"
            