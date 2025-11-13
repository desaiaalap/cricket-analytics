"""
Tests for match predictor module.
"""

import pytest
import pandas as pd
import numpy as np
from src.modeling.match_predictor import MatchPredictor


class TestMatchPredictor:
    """Test suite for MatchPredictor class."""

    def test_initialization_all_models(self):
        """Test predictor initialization with all models."""
        predictor = MatchPredictor(model_type='all')
        assert len(predictor.models) == 6  # LR, RF, GB, XGB, LGB, CatBoost

    def test_initialization_single_model(self):
        """Test predictor initialization with single model."""
        predictor = MatchPredictor(model_type='rf')
        assert len(predictor.models) == 1
        assert 'Random Forest' in predictor.models

    @pytest.mark.slow
    def test_train_returns_results(self, sample_features, sample_target):
        """Test that train method returns results dictionary."""
        predictor = MatchPredictor(model_type='rf')
        results = predictor.train(sample_features, sample_target, test_size=0.2)

        assert isinstance(results, dict)
        assert 'Random Forest' in results
        assert 'accuracy' in results['Random Forest']
        assert 'f1_score' in results['Random Forest']

    @pytest.mark.slow
    def test_train_sets_best_model(self, sample_features, sample_target):
        """Test that train method sets best_model."""
        predictor = MatchPredictor(model_type='lr')
        predictor.train(sample_features, sample_target, test_size=0.2)

        assert predictor.best_model is not None

    def test_predict_with_trained_model(self, sample_features, sample_target):
        """Test prediction with trained model."""
        predictor = MatchPredictor(model_type='lr')
        predictor.train(sample_features, sample_target, test_size=0.2)

        predictions = predictor.predict(sample_features.head(10))
        assert len(predictions) == 10
        assert all(pred in [0, 1] for pred in predictions)

    def test_get_feature_importance(self, sample_features, sample_target):
        """Test feature importance extraction."""
        predictor = MatchPredictor(model_type='rf')
        predictor.train(sample_features, sample_target, test_size=0.2)

        importance = predictor.get_feature_importance(top_n=3)
        assert isinstance(importance, dict)
        assert 'Random Forest' in importance

    def test_metrics_in_valid_range(self, sample_features, sample_target):
        """Test that all metrics are in valid ranges."""
        predictor = MatchPredictor(model_type='lr')
        results = predictor.train(sample_features, sample_target, test_size=0.2)

        for model_name, metrics in results.items():
            assert 0 <= metrics['accuracy'] <= 1
            assert 0 <= metrics['precision'] <= 1
            assert 0 <= metrics['recall'] <= 1
            assert 0 <= metrics['f1_score'] <= 1
