"""
Tests for data processor module.
"""

import pytest
import pandas as pd
from src.etl.data_processor import DataProcessor


class TestDataProcessor:
    """Test suite for DataProcessor class."""

    def test_clean_match_data_removes_duplicates(self, sample_match_data):
        """Test that clean_match_data removes duplicates."""
        # Add duplicate row
        df = pd.concat([sample_match_data, sample_match_data.iloc[[0]]])
        processor = DataProcessor()
        cleaned = processor.clean_match_data(df)

        assert len(cleaned) < len(df)
        assert cleaned.duplicated().sum() == 0

    def test_clean_match_data_handles_empty_df(self):
        """Test that clean_match_data handles empty DataFrame."""
        processor = DataProcessor()
        empty_df = pd.DataFrame()
        result = processor.clean_match_data(empty_df)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_engineer_features_returns_dataframe(self, sample_match_data):
        """Test that engineer_features returns a DataFrame."""
        processor = DataProcessor()
        result = processor.engineer_features(sample_match_data)

        assert isinstance(result, pd.DataFrame)

    def test_engineer_features_handles_empty_df(self):
        """Test that engineer_features handles empty DataFrame."""
        processor = DataProcessor()
        empty_df = pd.DataFrame()
        result = processor.engineer_features(empty_df)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_aggregate_player_stats_returns_dataframe(self, sample_player_data):
        """Test that aggregate_player_stats returns a DataFrame."""
        processor = DataProcessor()
        result = processor.aggregate_player_stats(sample_player_data, ['player_name'])

        assert isinstance(result, pd.DataFrame)
