"""
Pytest configuration and fixtures.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


@pytest.fixture
def sample_match_data():
    """
    Fixture providing sample match data for testing.
    """
    return pd.DataFrame({
        'match_id': ['M1', 'M2', 'M3', 'M4', 'M5'],
        'team': ['Team A', 'Team B', 'Team A', 'Team C', 'Team B'],
        'opponent': ['Team B', 'Team A', 'Team C', 'Team A', 'Team C'],
        'total_runs': [180, 165, 195, 150, 175],
        'wickets': [7, 10, 5, 8, 6],
        'result': ['won', 'lost', 'won', 'lost', 'won'],
        'venue': ['Stadium A', 'Stadium B', 'Stadium A', 'Stadium C', 'Stadium B'],
        'date': pd.date_range('2024-01-01', periods=5, freq='D')
    })


@pytest.fixture
def sample_player_data():
    """
    Fixture providing sample player data for testing.
    """
    return pd.DataFrame({
        'player_id': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'player_name': ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5'],
        'runs': [50, 75, 30, 90, 45],
        'balls_faced': [35, 50, 25, 60, 40],
        'fours': [4, 6, 2, 8, 3],
        'sixes': [2, 3, 1, 4, 2],
        'wickets': [2, 0, 3, 1, 2]
    })


@pytest.fixture
def sample_features():
    """
    Fixture providing sample feature matrix for ML testing.
    """
    np.random.seed(42)
    n_samples = 100
    return pd.DataFrame({
        'feature_1': np.random.randn(n_samples),
        'feature_2': np.random.randn(n_samples),
        'feature_3': np.random.randn(n_samples),
        'feature_4': np.random.randn(n_samples),
        'feature_5': np.random.randn(n_samples)
    })


@pytest.fixture
def sample_target():
    """
    Fixture providing sample target variable for ML testing.
    """
    np.random.seed(42)
    return pd.Series(np.random.randint(0, 2, 100))


@pytest.fixture
def temp_data_dir(tmp_path):
    """
    Fixture providing temporary directory for data files.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "raw").mkdir()
    (data_dir / "processed").mkdir()
    return data_dir
