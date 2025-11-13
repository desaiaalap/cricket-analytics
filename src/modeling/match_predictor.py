"""
Match outcome prediction models.
Implements multiple ML algorithms for comparison.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import logging

logger = logging.getLogger(__name__)


class MatchPredictor:
    """
    Multi-model match outcome predictor.
    Trains and compares multiple ML algorithms.
    """

    def __init__(self, model_type: str = 'all'):
        """
        Initialize the predictor with specified model type.

        Args:
            model_type: Type of model to use ('all', 'rf', 'xgb', 'lgb', 'catboost', 'lr', 'gb')
        """
        self.model_type = model_type
        self.models = {}
        self.scaler = StandardScaler()
        self.best_model = None
        self.results = {}

        self._initialize_models()
        logger.info(f"MatchPredictor initialized with model type: {model_type}")

    def _initialize_models(self):
        """Initialize all models based on model_type."""
        if self.model_type == 'all':
            self.models = {
                'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
                'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss'),
                'LightGBM': lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1),
                'CatBoost': CatBoostClassifier(iterations=100, random_state=42, verbose=0)
            }
        elif self.model_type == 'rf':
            self.models = {'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)}
        elif self.model_type == 'xgb':
            self.models = {'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')}
        elif self.model_type == 'lgb':
            self.models = {'LightGBM': lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)}
        elif self.model_type == 'catboost':
            self.models = {'CatBoost': CatBoostClassifier(iterations=100, random_state=42, verbose=0)}
        elif self.model_type == 'lr':
            self.models = {'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)}
        elif self.model_type == 'gb':
            self.models = {'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)}

    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict[str, Dict[str, float]]:
        """
        Train all models and return performance metrics.

        Args:
            X: Feature DataFrame
            y: Target Series
            test_size: Proportion of data for testing

        Returns:
            Dictionary of model performance metrics
        """
        logger.info(f"Training models on {len(X)} samples with {X.shape[1]} features")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train each model
        for name, model in self.models.items():
            logger.info(f"Training {name}...")

            # Train
            model.fit(X_train_scaled, y_train)

            # Predictions
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, 'predict_proba') else None

            # Calculate metrics
            self.results[name] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            }

            if y_pred_proba is not None:
                self.results[name]['roc_auc'] = roc_auc_score(y_test, y_pred_proba)

            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
            self.results[name]['cv_mean'] = cv_scores.mean()
            self.results[name]['cv_std'] = cv_scores.std()

            logger.info(f"{name} - Accuracy: {self.results[name]['accuracy']:.4f}, "
                       f"F1: {self.results[name]['f1_score']:.4f}")

        # Identify best model
        self.best_model = max(self.results.items(), key=lambda x: x[1]['accuracy'])[0]
        logger.info(f"Best model: {self.best_model}")

        return self.results

    def predict(self, X: pd.DataFrame, use_best: bool = True) -> np.ndarray:
        """
        Make predictions using trained model(s).

        Args:
            X: Feature DataFrame
            use_best: Use best performing model

        Returns:
            Predictions array
        """
        X_scaled = self.scaler.transform(X)

        if use_best and self.best_model:
            model = self.models[self.best_model]
            return model.predict(X_scaled)

        # Return predictions from all models
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X_scaled)

        return predictions

    def get_feature_importance(self, top_n: int = 10) -> Dict[str, pd.DataFrame]:
        """
        Get feature importance from tree-based models.

        Args:
            top_n: Number of top features to return

        Returns:
            Dictionary of feature importance DataFrames
        """
        importance_dict = {}

        for name, model in self.models.items():
            if hasattr(model, 'feature_importances_'):
                importance_dict[name] = pd.DataFrame({
                    'feature': range(len(model.feature_importances_)),
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False).head(top_n)

        return importance_dict
