import pytest
import config

from nera.data_initialization.parse_urls_from_json import parse_urls_from_json


class TestParseUrlsFromJson:


    @pytest.fixture
    def setup_data(self):
        # Setup data directory and file paths
        contractor_json_file = config.CONTRACTOR_JSON_FILES_DIR / 'all_6xx_Jun_29.json'
        return contractor_json_file


    def test_parse_urls_returns_list(self, setup_data):
        urls = parse_urls_from_json(setup_data)
        assert isinstance(urls, list), "URLs should be in a list"


    def test_parse_urls_list_not_empty(self, setup_data):
        urls = parse_urls_from_json(setup_data)
        assert len(urls) > 0, "URLs list should not be empty"


    def test_parse_urls_list_contains_strings(self, setup_data):
        urls = parse_urls_from_json(setup_data)
        assert all(isinstance(url, str) for url in urls), "All elements in the list should be strings"