"""
Unit tests for Cricpy Loader

Tests the YAML loading and parsing functionality
"""

import unittest
import sys
import os
from pathlib import Path
import pandas as pd
import yaml

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from cricpy_loader import load_yaml, parse_match_info, parse_match


class TestLoadYaml(unittest.TestCase):
    """Test cases for YAML loading"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_yaml = {
            "meta": {"data_version": "1.0.0", "created": "2024-01-01", "revision": 1},
            "info": {
                "venue": "Test Stadium",
                "city": "Test City",
                "dates": ["2024-01-15"],
                "gender": "male",
                "match_type": "T20",
                "teams": ["Team A", "Team B"],
                "outcome": {"winner": "Team A", "by": {"runs": 25}},
            },
        }

    def test_parse_match_info_basic(self):
        """Test parsing basic match information"""
        info = parse_match_info(self.test_yaml)

        # Check required fields
        self.assertEqual(info["venue"], "Test Stadium")
        self.assertEqual(info["city"], "Test City")
        self.assertEqual(info["gender"], "male")
        self.assertEqual(info["match_type"], "T20")

    def test_parse_match_info_teams(self):
        """Test parsing team information"""
        info = parse_match_info(self.test_yaml)

        self.assertIn("teams", info)
        self.assertEqual(info["teams"], ["Team A", "Team B"])
        self.assertEqual(len(info["teams"]), 2)

    def test_parse_match_info_outcome(self):
        """Test parsing match outcome"""
        info = parse_match_info(self.test_yaml)

        self.assertEqual(info["outcome_winner"], "Team A")
        self.assertIn("outcome_by", info)

    def test_parse_match_info_missing_fields(self):
        """Test parsing with missing optional fields"""
        minimal_yaml = {"info": {"venue": "Test Stadium", "teams": ["Team A", "Team B"]}}

        # Should not raise error
        info = parse_match_info(minimal_yaml)
        self.assertEqual(info["venue"], "Test Stadium")


class TestParseMatch(unittest.TestCase):
    """Test cases for match parsing"""

    def setUp(self):
        """Set up test match data"""
        self.test_match = {
            "info": {"venue": "Test Stadium", "teams": ["Team A", "Team B"]},
            "innings": [
                {
                    "1st innings": {
                        "team": "Team A",
                        "deliveries": [
                            {
                                "0.1": {
                                    "batsman": "Player 1",
                                    "bowler": "Player 2",
                                    "non_striker": "Player 3",
                                    "runs": {"batsman": 4, "extras": 0, "total": 4},
                                }
                            },
                            {
                                "0.2": {
                                    "batsman": "Player 1",
                                    "bowler": "Player 2",
                                    "non_striker": "Player 3",
                                    "runs": {"batsman": 0, "extras": 0, "total": 0},
                                }
                            },
                        ],
                    }
                }
            ],
        }

    def test_parse_match_returns_dataframe(self):
        """Test that parse_match returns a DataFrame"""
        df = parse_match(self.test_match)
        self.assertIsInstance(df, pd.DataFrame)

    def test_parse_match_columns(self):
        """Test that parsed DataFrame has expected columns"""
        df = parse_match(self.test_match)

        expected_columns = [
            "inning",
            "batting_team",
            "ball",
            "batsman",
            "bowler",
            "runs_batter",
            "runs_extras",
            "runs_total",
        ]

        for col in expected_columns:
            self.assertIn(col, df.columns)

    def test_parse_match_data_integrity(self):
        """Test that parsed data maintains integrity"""
        df = parse_match(self.test_match)

        # Should have 2 deliveries
        self.assertEqual(len(df), 2)

        # Check first delivery
        first_delivery = df.iloc[0]
        self.assertEqual(first_delivery["batsman"], "Player 1")
        self.assertEqual(first_delivery["bowler"], "Player 2")
        self.assertEqual(first_delivery["runs_batter"], 4)
        self.assertEqual(first_delivery["runs_total"], 4)

    def test_parse_match_empty_innings(self):
        """Test parsing match with no innings data"""
        empty_match = {"info": {"venue": "Test Stadium", "teams": ["A", "B"]}, "innings": []}

        df = parse_match(empty_match)
        self.assertEqual(len(df), 0)


class TestDataTypeValidation(unittest.TestCase):
    """Test data type validation and conversions"""

    def test_runs_are_numeric(self):
        """Test that runs are properly converted to numeric types"""
        test_match = {
            "info": {"venue": "Test", "teams": ["A", "B"]},
            "innings": [
                {
                    "1st innings": {
                        "team": "A",
                        "deliveries": [
                            {
                                "0.1": {
                                    "batsman": "P1",
                                    "bowler": "P2",
                                    "non_striker": "P3",
                                    "runs": {"batsman": 6, "extras": 0, "total": 6},
                                }
                            }
                        ],
                    }
                }
            ],
        }

        df = parse_match(test_match)

        # Runs columns should be numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(df["runs_batter"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(df["runs_total"]))

    def test_ball_number_extraction(self):
        """Test that ball numbers are properly extracted"""
        test_match = {
            "info": {"venue": "Test", "teams": ["A", "B"]},
            "innings": [
                {
                    "1st innings": {
                        "team": "A",
                        "deliveries": [
                            {
                                "5.3": {
                                    "batsman": "P1",
                                    "bowler": "P2",
                                    "non_striker": "P3",
                                    "runs": {"batsman": 1, "extras": 0, "total": 1},
                                }
                            }
                        ],
                    }
                }
            ],
        }

        df = parse_match(test_match)

        # Ball number stored as string "5.3"
        self.assertEqual(df.iloc[0]["ball"], "5.3")


if __name__ == "__main__":
    unittest.main()
