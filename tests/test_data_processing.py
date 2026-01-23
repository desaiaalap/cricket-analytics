"""
Integration tests for data processing pipeline

Tests the complete data processing workflow
"""

import unittest
import sys
import os
import pandas as pd
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestDataProcessingPipeline(unittest.TestCase):
    """Test cases for the complete data processing pipeline"""

    def setUp(self):
        """Set up test fixtures"""
        # Check if processed data exists
        self.processed_dir = Path('data/processed')
        self.data_exists = self.processed_dir.exists()

    def test_processed_directory_exists(self):
        """Test that processed data directory exists"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        self.assertTrue(self.processed_dir.exists())

    def test_all_deliveries_csv_exists(self):
        """Test that all_deliveries.csv exists"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'all_deliveries.csv'
        self.assertTrue(csv_path.exists(), "all_deliveries.csv should exist")

    def test_all_deliveries_structure(self):
        """Test structure of all_deliveries.csv"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'all_deliveries.csv'
        if not csv_path.exists():
            self.skipTest("all_deliveries.csv not found")

        df = pd.read_csv(csv_path)

        # Check key columns exist
        expected_columns = ['innings', 'over', 'ball', 'batsman', 'bowler',
                          'runs_batsman', 'runs_total', 'batting_team']

        for col in expected_columns:
            self.assertIn(col, df.columns, f"Column '{col}' should exist")

        # Check data types
        self.assertTrue(pd.api.types.is_numeric_dtype(df['runs_batsman']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['runs_total']))

    def test_match_summaries_csv_exists(self):
        """Test that match_summaries.csv exists"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'match_summaries.csv'
        self.assertTrue(csv_path.exists(), "match_summaries.csv should exist")

    def test_match_summaries_structure(self):
        """Test structure of match_summaries.csv"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'match_summaries.csv'
        if not csv_path.exists():
            self.skipTest("match_summaries.csv not found")

        df = pd.read_csv(csv_path)

        # Check key columns
        expected_columns = ['match_id', 'venue', 'teams', 'winner']

        for col in expected_columns:
            self.assertIn(col, df.columns, f"Column '{col}' should exist")

    def test_batting_stats_csv_exists(self):
        """Test that player_batting_stats.csv exists"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'player_batting_stats.csv'
        self.assertTrue(csv_path.exists(), "player_batting_stats.csv should exist")

    def test_batting_stats_structure(self):
        """Test structure of batting stats"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'player_batting_stats.csv'
        if not csv_path.exists():
            self.skipTest("player_batting_stats.csv not found")

        df = pd.read_csv(csv_path)

        # Check key metrics
        expected_columns = ['player', 'runs', 'average', 'strike_rate']

        for col in expected_columns:
            self.assertIn(col, df.columns, f"Column '{col}' should exist")

        # Check reasonable value ranges
        self.assertTrue((df['runs'] >= 0).all(), "Runs should be non-negative")
        self.assertTrue((df['strike_rate'] >= 0).all(), "Strike rate should be non-negative")

    def test_bowling_stats_csv_exists(self):
        """Test that player_bowling_stats.csv exists"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'player_bowling_stats.csv'
        self.assertTrue(csv_path.exists(), "player_bowling_stats.csv should exist")

    def test_bowling_stats_structure(self):
        """Test structure of bowling stats"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        csv_path = self.processed_dir / 'player_bowling_stats.csv'
        if not csv_path.exists():
            self.skipTest("player_bowling_stats.csv not found")

        df = pd.read_csv(csv_path)

        # Check key metrics
        expected_columns = ['player', 'wickets', 'economy', 'average']

        for col in expected_columns:
            self.assertIn(col, df.columns, f"Column '{col}' should exist")

        # Check reasonable value ranges
        self.assertTrue((df['wickets'] >= 0).all(), "Wickets should be non-negative")
        self.assertTrue((df['economy'] >= 0).all(), "Economy should be non-negative")

    def test_data_consistency(self):
        """Test consistency across datasets"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        deliveries_path = self.processed_dir / 'all_deliveries.csv'
        matches_path = self.processed_dir / 'match_summaries.csv'

        if not (deliveries_path.exists() and matches_path.exists()):
            self.skipTest("Required files not found")

        deliveries_df = pd.read_csv(deliveries_path)
        matches_df = pd.read_csv(matches_path)

        # Number of unique match_ids should match
        if 'match_id' in deliveries_df.columns:
            unique_matches_in_deliveries = deliveries_df['match_id'].nunique()
            matches_count = len(matches_df)

            self.assertEqual(unique_matches_in_deliveries, matches_count,
                           "Match count should be consistent across datasets")


class TestDataQuality(unittest.TestCase):
    """Test data quality and integrity"""

    def setUp(self):
        """Set up test fixtures"""
        self.processed_dir = Path('data/processed')
        self.data_exists = self.processed_dir.exists()

    def test_no_null_critical_fields(self):
        """Test that critical fields have no null values"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        deliveries_path = self.processed_dir / 'all_deliveries.csv'
        if not deliveries_path.exists():
            self.skipTest("all_deliveries.csv not found")

        df = pd.read_csv(deliveries_path)

        # Critical fields should not be null
        critical_fields = ['batsman', 'bowler', 'runs_total']

        for field in critical_fields:
            if field in df.columns:
                null_count = df[field].isnull().sum()
                self.assertEqual(null_count, 0,
                               f"Field '{field}' should not have null values")

    def test_runs_are_reasonable(self):
        """Test that run values are within reasonable ranges"""
        if not self.data_exists:
            self.skipTest("Processed data not available")

        deliveries_path = self.processed_dir / 'all_deliveries.csv'
        if not deliveries_path.exists():
            self.skipTest("all_deliveries.csv not found")

        df = pd.read_csv(deliveries_path)

        # Runs per ball should be between 0-6 (excluding extras)
        max_runs = df['runs_batsman'].max()
        self.assertLessEqual(max_runs, 6, "Maximum runs per ball should be 6")
        self.assertGreaterEqual(df['runs_batsman'].min(), 0, "Minimum runs should be 0")


if __name__ == '__main__':
    unittest.main()
