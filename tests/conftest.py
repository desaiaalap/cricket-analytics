"""
Pytest configuration and shared fixtures

This file contains pytest fixtures that can be used across all test files.
"""

import pytest
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


@pytest.fixture
def sample_match_data():
    """
    Fixture providing sample match data for testing

    Returns a dictionary representing a minimal valid match structure
    """
    return {
        "meta": {"data_version": "1.0.0", "created": "2024-01-01", "revision": 1},
        "info": {
            "venue": "Melbourne Cricket Ground",
            "city": "Melbourne",
            "dates": ["2024-01-15"],
            "gender": "male",
            "match_type": "T20",
            "teams": ["Australia", "India"],
            "toss": {"winner": "Australia", "decision": "bat"},
            "outcome": {"winner": "Australia", "by": {"runs": 25}},
            "players": {
                "Australia": ["Player A1", "Player A2", "Player A3"],
                "India": ["Player I1", "Player I2", "Player I3"],
            },
        },
        "innings": [
            {
                "team": "Australia",
                "deliveries": [
                    {
                        "0.1": {
                            "batsman": "Player A1",
                            "bowler": "Player I1",
                            "non_striker": "Player A2",
                            "runs": {"batsman": 4, "extras": 0, "total": 4},
                        }
                    },
                    {
                        "0.2": {
                            "batsman": "Player A1",
                            "bowler": "Player I1",
                            "non_striker": "Player A2",
                            "runs": {"batsman": 6, "extras": 0, "total": 6},
                        }
                    },
                    {
                        "0.3": {
                            "batsman": "Player A1",
                            "bowler": "Player I1",
                            "non_striker": "Player A2",
                            "runs": {"batsman": 0, "extras": 0, "total": 0},
                            "wicket": {
                                "player_out": "Player A1",
                                "kind": "caught",
                                "fielders": ["Player I2"],
                            },
                        }
                    },
                ],
            },
            {
                "team": "India",
                "deliveries": [
                    {
                        "0.1": {
                            "batsman": "Player I1",
                            "bowler": "Player A1",
                            "non_striker": "Player I2",
                            "runs": {"batsman": 1, "extras": 0, "total": 1},
                        }
                    }
                ],
            },
        ],
    }


@pytest.fixture
def temp_directory():
    """
    Fixture providing a temporary directory for testing

    Automatically cleans up after the test
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_deliveries_data():
    """
    Fixture providing sample deliveries data as would be parsed from a match
    """
    import pandas as pd

    return pd.DataFrame(
        {
            "innings": [1, 1, 1, 2],
            "over": [0, 0, 0, 0],
            "ball": [1, 2, 3, 1],
            "batting_team": ["Australia", "Australia", "Australia", "India"],
            "batsman": ["Player A1", "Player A1", "Player A1", "Player I1"],
            "bowler": ["Player I1", "Player I1", "Player I1", "Player A1"],
            "non_striker": ["Player A2", "Player A2", "Player A2", "Player I2"],
            "runs_batsman": [4, 6, 0, 1],
            "runs_extras": [0, 0, 0, 0],
            "runs_total": [4, 6, 0, 1],
            "dismissal": [None, None, "caught", None],
        }
    )


@pytest.fixture
def mock_cricsheet_response():
    """
    Fixture providing a mock HTTP response for Cricsheet downloads
    """

    class MockResponse:
        def __init__(self):
            self.status_code = 200
            self.headers = {"content-length": "1000"}

        def iter_content(self, chunk_size=8192):
            # Return fake data in chunks
            return [b"test data chunk 1", b"test data chunk 2"]

        def raise_for_status(self):
            pass

    return MockResponse()


@pytest.fixture
def processed_data_path():
    """
    Fixture providing path to processed data directory

    Returns None if data doesn't exist
    """
    path = Path("data/processed")
    if path.exists():
        return path
    return None


@pytest.fixture(scope="session")
def test_data_dir():
    """
    Session-scoped fixture for test data directory
    """
    return Path(__file__).parent / "test_data"


# Pytest hooks for custom test behavior


def pytest_configure(config):
    """
    Custom pytest configuration
    """
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "network: mark test as requiring network access")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers automatically
    """
    for item in items:
        # Add 'unit' marker to all tests in test_* files by default
        if "test_cricsheet_downloader" in str(item.fspath):
            if "network" not in item.keywords:
                item.add_marker(pytest.mark.network)

        # Add 'integration' marker to integration tests
        if "test_data_processing" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
