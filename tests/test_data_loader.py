"""
Tests for data loader module.
"""

import pytest
import pandas as pd
from src.etl.data_loader import CricketDataLoader


class TestCricketDataLoader:
    """Test suite for CricketDataLoader class."""

    def test_initialization(self):
        """Test loader initialization."""
        loader = CricketDataLoader()
        assert loader is not None
        assert loader.api_base_url is None

    def test_initialization_with_url(self):
        """Test loader initialization with API URL."""
        url = "https://api.example.com"
        loader = CricketDataLoader(api_base_url=url)
        assert loader.api_base_url == url

    def test_load_match_data_returns_dataframe(self):
        """Test that load_match_data returns a DataFrame."""
        loader = CricketDataLoader()
        result = loader.load_match_data("M123")
        assert isinstance(result, pd.DataFrame)

    def test_load_player_stats_returns_dataframe(self):
        """Test that load_player_stats returns a DataFrame."""
        loader = CricketDataLoader()
        result = loader.load_player_stats("P456")
        assert isinstance(result, pd.DataFrame)

    def test_load_tournament_data_returns_dataframe(self):
        """Test that load_tournament_data returns a DataFrame."""
        loader = CricketDataLoader()
        result = loader.load_tournament_data("IPL", "2023")
        assert isinstance(result, pd.DataFrame)
