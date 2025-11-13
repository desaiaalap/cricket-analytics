"""
Tests for player tracker module.
"""

import pytest
import numpy as np
from src.tracking.player_tracker import PlayerTracker


class TestPlayerTracker:
    """Test suite for PlayerTracker class."""

    def test_initialization(self):
        """Test tracker initialization."""
        tracker = PlayerTracker()
        assert tracker is not None
        assert tracker.video_path is None

    def test_initialization_with_path(self):
        """Test tracker initialization with video path."""
        path = "/path/to/video.mp4"
        tracker = PlayerTracker(video_path=path)
        assert tracker.video_path == path

    def test_detect_players_returns_list(self):
        """Test that detect_players returns a list."""
        tracker = PlayerTracker()
        frame = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
        detections = tracker.detect_players(frame)

        assert isinstance(detections, list)

    def test_track_players_returns_dict(self):
        """Test that track_players returns a dictionary."""
        tracker = PlayerTracker()
        initial_boxes = [(100, 100, 50, 100), (200, 150, 50, 100)]
        tracks = tracker.track_players(initial_boxes)

        assert isinstance(tracks, dict)

    def test_extract_player_movements(self):
        """Test movement extraction from tracks."""
        tracker = PlayerTracker()
        tracks = {
            1: [(100, 100, 50, 100), (110, 105, 50, 100)],
            2: [(200, 150, 50, 100)]
        }
        movements = tracker.extract_player_movements(tracks)

        assert isinstance(movements, dict)
        assert 1 in movements
        assert 'total_distance' in movements[1]
