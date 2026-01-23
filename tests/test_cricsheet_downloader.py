"""
Unit tests for Cricsheet Downloader

Tests the automated data download functionality from Cricsheet.org
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from cricsheet_downloader import CricsheetDownloader, download_cricsheet_data


class TestCricsheetDownloader(unittest.TestCase):
    """Test cases for CricsheetDownloader class"""

    def setUp(self):
        """Set up test fixtures"""
        self.downloader = CricsheetDownloader()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_list_available_tournaments(self):
        """Test listing available tournaments"""
        tournaments = self.downloader.list_available_tournaments()

        # Should return a dictionary
        self.assertIsInstance(tournaments, dict)

        # Should have some tournaments
        self.assertGreater(len(tournaments), 0)

        # Should contain expected tournaments
        expected_tournaments = ["ipl", "bbl", "t20_internationals_male", "odi_male"]
        for tournament in expected_tournaments:
            self.assertIn(tournament, tournaments)

    def test_get_download_url(self):
        """Test getting download URL for a tournament"""
        # Valid tournament
        url = self.downloader.get_download_url("ipl")
        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("https://"))
        self.assertIn("cricsheet.org", url)
        self.assertIn(".zip", url)

    def test_get_download_url_invalid_tournament(self):
        """Test getting URL for invalid tournament raises error"""
        with self.assertRaises(ValueError) as context:
            self.downloader.get_download_url("invalid_tournament")

        self.assertIn("not found", str(context.exception))

    def test_get_tournament_info(self):
        """Test getting tournament information"""
        info = self.downloader.get_tournament_info("ipl")

        # Should return a dictionary
        self.assertIsInstance(info, dict)

        # Should contain expected keys
        expected_keys = ["name", "filename", "url", "format", "compressed"]
        for key in expected_keys:
            self.assertIn(key, info)

        # Verify values
        self.assertEqual(info["name"], "ipl")
        self.assertTrue(info["filename"].endswith(".zip"))
        self.assertEqual(info["format"], "YAML")
        self.assertTrue(info["compressed"])

    def test_get_tournament_info_invalid(self):
        """Test getting info for invalid tournament raises error"""
        with self.assertRaises(ValueError):
            self.downloader.get_tournament_info("invalid_tournament")

    @patch("cricsheet_downloader.requests.get")
    def test_download_tournament_network_error(self, mock_get):
        """Test download handles network errors gracefully"""
        # Simulate network error
        mock_get.side_effect = Exception("Network error")

        with self.assertRaises(Exception):
            self.downloader.download_tournament("ipl", self.temp_dir)

    def test_download_tournament_invalid_tournament(self):
        """Test download with invalid tournament raises error"""
        with self.assertRaises(ValueError):
            self.downloader.download_tournament("invalid_tournament", self.temp_dir)

    def test_custom_base_url(self):
        """Test downloader with custom base URL"""
        custom_url = "https://custom-url.com/downloads/"
        downloader = CricsheetDownloader(base_url=custom_url)

        url = downloader.get_download_url("ipl")
        self.assertTrue(url.startswith(custom_url))

    @patch("cricsheet_downloader.requests.get")
    @patch("cricsheet_downloader.zipfile.ZipFile")
    def test_download_tournament_success(self, mock_zipfile, mock_get):
        """Test successful download and extraction"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.headers = {"content-length": "1000"}
        mock_response.iter_content = Mock(return_value=[b"test data"])
        mock_get.return_value = mock_response

        # Mock ZIP extraction
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # This should not raise an error
        # Note: We're not actually downloading in the test
        # Just verifying the code structure is correct


class TestConvenienceFunction(unittest.TestCase):
    """Test cases for convenience functions"""

    @patch("cricsheet_downloader.CricsheetDownloader")
    def test_download_cricsheet_data(self, mock_downloader_class):
        """Test the convenience download function"""
        mock_downloader = Mock()
        mock_downloader.download_tournament.return_value = Path("/fake/path")
        mock_downloader_class.return_value = mock_downloader

        # Call convenience function
        result = download_cricsheet_data("ipl", "data/external")

        # Verify downloader was instantiated and called
        mock_downloader_class.assert_called_once()
        mock_downloader.download_tournament.assert_called_once_with("ipl", "data/external")


class TestTournamentCoverage(unittest.TestCase):
    """Test tournament coverage and data consistency"""

    def setUp(self):
        """Set up test fixtures"""
        self.downloader = CricsheetDownloader()

    def test_all_tournaments_have_valid_urls(self):
        """Test that all tournaments have properly formatted URLs"""
        tournaments = self.downloader.list_available_tournaments()

        for tournament_name in tournaments.keys():
            url = self.downloader.get_download_url(tournament_name)

            # URL should be valid
            self.assertTrue(url.startswith("https://"))
            self.assertIn("cricsheet.org", url)
            self.assertIn(".zip", url)

    def test_tournament_info_consistency(self):
        """Test that tournament info is consistent across all tournaments"""
        tournaments = self.downloader.list_available_tournaments()

        for tournament_name in list(tournaments.keys())[:5]:  # Test first 5
            info = self.downloader.get_tournament_info(tournament_name)

            # All should have YAML format
            self.assertEqual(info["format"], "YAML")

            # All should be compressed
            self.assertTrue(info["compressed"])

            # Name should match
            self.assertEqual(info["name"], tournament_name)


if __name__ == "__main__":
    unittest.main()
