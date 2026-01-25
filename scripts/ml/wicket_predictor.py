"""
Next-Ball Wicket Prediction Model
Predicts probability of wicket on the very next delivery using historical data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve
import warnings
warnings.filterwarnings('ignore')


class WicketPredictor:
    """Predicts wicket probability for next ball based on match context"""

    def __init__(self, data_path="data/processed/all_deliveries.csv"):
        self.data_path = Path(data_path)
        self.model = None
        self.feature_columns = []
        self.df = None

    def load_data(self):
        """Load ball-by-ball delivery data"""
        print("📊 Loading ball-by-ball data...")
        self.df = pd.read_csv(self.data_path)
        print(f"✅ Loaded {len(self.df):,} deliveries")
        return self

    def engineer_features(self):
        """Create features for wicket prediction"""
        print("\n🔧 Engineering features for prediction...")

        df = self.df.copy()

        # Target variable: is there a wicket on this ball?
        df['is_wicket'] = (~df['wicket_kind'].isna()).astype(int)

        # Basic ball context
        df['over_number'] = df['over'].astype(float)
        df['ball_number'] = df['ball'].astype(float)

        # Match phase (critical for wicket probability)
        df['phase'] = pd.cut(df['over_number'],
                            bins=[-1, 6, 16, 20],
                            labels=['powerplay', 'middle', 'death'])
        df['is_powerplay'] = (df['phase'] == 'powerplay').astype(int)
        df['is_middle'] = (df['phase'] == 'middle').astype(int)
        df['is_death'] = (df['phase'] == 'death').astype(int)

        # Sort by match and delivery order
        df = df.sort_values(['match_id', 'inning', 'over_number', 'ball_number'])

        # Cumulative match state features
        df['wickets_lost'] = df.groupby(['match_id', 'inning'])['is_wicket'].cumsum()
        df['runs_scored'] = df.groupby(['match_id', 'inning'])['runs_total'].cumsum()
        df['balls_bowled'] = df.groupby(['match_id', 'inning']).cumcount()

        # Current run rate
        df['current_run_rate'] = df['runs_scored'] / ((df['balls_bowled'] + 1) / 6)
        df['current_run_rate'] = df['current_run_rate'].fillna(0)

        # Pressure indicators
        df['runs_in_over'] = df.groupby(['match_id', 'inning', 'over'])['runs_total'].cumsum()
        df['dot_ball'] = (df['runs_total'] == 0).astype(int)

        # Player-level aggregates (historical performance)
        # Batter stats
        batter_stats = df.groupby('batter').agg({
            'is_wicket': 'mean',  # Dismissal rate
            'runs_batter': 'mean',  # Average runs per ball
        }).reset_index()
        batter_stats.columns = ['batter', 'batter_dismissal_rate', 'batter_avg_runs']
        df = df.merge(batter_stats, on='batter', how='left')

        # Bowler stats
        bowler_stats = df.groupby('bowler').agg({
            'is_wicket': 'mean',  # Strike rate (wickets per ball)
            'runs_total': 'mean',  # Economy per ball
        }).reset_index()
        bowler_stats.columns = ['bowler', 'bowler_wicket_rate', 'bowler_avg_runs']
        df = df.merge(bowler_stats, on='bowler', how='left')

        # Head-to-head: specific batter vs bowler
        h2h = df.groupby(['batter', 'bowler']).agg({
            'is_wicket': 'mean',
            'runs_batter': 'mean',
        }).reset_index()
        h2h.columns = ['batter', 'bowler', 'h2h_wicket_rate', 'h2h_avg_runs']
        df = df.merge(h2h, on=['batter', 'bowler'], how='left')

        # Recent form (last 6 balls for batter)
        df['batter_recent_runs'] = df.groupby(['match_id', 'inning', 'batter'])['runs_batter'].rolling(6, min_periods=1).sum().reset_index(0, drop=True)
        df['batter_recent_dots'] = df.groupby(['match_id', 'inning', 'batter'])['dot_ball'].rolling(6, min_periods=1).sum().reset_index(0, drop=True)

        # Bowler recent form (last 6 balls)
        df['bowler_recent_wickets'] = df.groupby(['match_id', 'inning', 'bowler'])['is_wicket'].rolling(6, min_periods=1).sum().reset_index(0, drop=True)
        df['bowler_recent_runs'] = df.groupby(['match_id', 'inning', 'bowler'])['runs_total'].rolling(6, min_periods=1).sum().reset_index(0, drop=True)

        # Fill missing values
        df = df.fillna(0)

        self.df = df
        print(f"✅ Created {len(df.columns)} features")
        print(f"   Wickets in dataset: {df['is_wicket'].sum():,} ({df['is_wicket'].mean()*100:.2f}%)")

        return self

    def prepare_training_data(self):
        """Prepare features and target for model training"""
        print("\n📋 Preparing training data...")

        # Select features for model
        self.feature_columns = [
            # Ball context
            'over_number', 'ball_number', 'is_powerplay', 'is_middle', 'is_death',

            # Match state
            'wickets_lost', 'runs_scored', 'balls_bowled', 'current_run_rate',
            'runs_in_over', 'dot_ball',

            # Player stats
            'batter_dismissal_rate', 'batter_avg_runs',
            'bowler_wicket_rate', 'bowler_avg_runs',

            # Head-to-head
            'h2h_wicket_rate', 'h2h_avg_runs',

            # Recent form
            'batter_recent_runs', 'batter_recent_dots',
            'bowler_recent_wickets', 'bowler_recent_runs',
        ]

        X = self.df[self.feature_columns]
        y = self.df['is_wicket']

        # Split data (temporal split - last 20% of matches for testing)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        print(f"✅ Training set: {len(X_train):,} balls ({y_train.sum():,} wickets)")
        print(f"✅ Test set: {len(X_test):,} balls ({y_test.sum():,} wickets)")

        return X_train, X_test, y_train, y_test

    def train_model(self, X_train, y_train, model_type='random_forest'):
        """Train wicket prediction model"""
        print(f"\n🤖 Training {model_type} model...")

        if model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=100,
                min_samples_leaf=50,
                class_weight='balanced',  # Handle imbalanced data
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        elif model_type == 'logistic':
            self.model = LogisticRegression(
                class_weight='balanced',
                random_state=42,
                max_iter=1000
            )

        self.model.fit(X_train, y_train)
        print("✅ Model trained successfully")

        return self

    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        print("\n📊 Evaluating model performance...")

        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]

        # Metrics
        print("\n" + "="*60)
        print("CLASSIFICATION REPORT")
        print("="*60)
        print(classification_report(y_test, y_pred,
                                   target_names=['No Wicket', 'Wicket'],
                                   digits=3))

        # ROC AUC
        auc = roc_auc_score(y_test, y_pred_proba)
        print(f"ROC AUC Score: {auc:.4f}")

        # Feature importance (for tree-based models)
        if hasattr(self.model, 'feature_importances_'):
            print("\n" + "="*60)
            print("TOP 10 MOST IMPORTANT FEATURES")
            print("="*60)
            importances = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False).head(10)

            for idx, row in importances.iterrows():
                print(f"{row['feature']:30s} {row['importance']:.4f}")

        # Probability calibration check
        print("\n" + "="*60)
        print("PROBABILITY CALIBRATION")
        print("="*60)
        for threshold in [0.05, 0.10, 0.15, 0.20]:
            high_prob = y_pred_proba >= threshold
            if high_prob.sum() > 0:
                actual_rate = y_test[high_prob].mean()
                print(f"When P(wicket) >= {threshold:.0%}: {actual_rate:.1%} actual wicket rate ({high_prob.sum()} balls)")

        return {
            'auc': auc,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }

    def predict_next_ball(self, match_state):
        """
        Predict wicket probability for next ball given current match state

        Args:
            match_state (dict): Current match situation with keys matching feature_columns

        Returns:
            float: Probability of wicket on next ball (0-1)
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")

        # Create feature vector
        features = pd.DataFrame([match_state])[self.feature_columns]

        # Predict
        wicket_prob = self.model.predict_proba(features)[0, 1]

        return wicket_prob

    def save_model(self, filepath="scripts/ml/wicket_model.pkl"):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"\n💾 Model saved to {filepath}")

    def load_model(self, filepath="scripts/ml/wicket_model.pkl"):
        """Load trained model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.feature_columns = model_data['feature_columns']

        print(f"✅ Model loaded from {filepath}")
        return self


def main():
    """Train and evaluate wicket prediction model"""
    print("="*60)
    print("NEXT-BALL WICKET PREDICTION MODEL")
    print("="*60)

    # Initialize predictor
    predictor = WicketPredictor()

    # Load and prepare data
    predictor.load_data()
    predictor.engineer_features()
    X_train, X_test, y_train, y_test = predictor.prepare_training_data()

    # Train model
    predictor.train_model(X_train, y_train, model_type='random_forest')

    # Evaluate
    results = predictor.evaluate_model(X_test, y_test)

    # Save model
    predictor.save_model()

    # Example prediction
    print("\n" + "="*60)
    print("EXAMPLE PREDICTION")
    print("="*60)
    print("Scenario: Death overs, 2 wickets down, high pressure")

    example_state = {
        'over_number': 18.0,
        'ball_number': 3.0,
        'is_powerplay': 0,
        'is_middle': 0,
        'is_death': 1,
        'wickets_lost': 2,
        'runs_scored': 145,
        'balls_bowled': 107,
        'current_run_rate': 8.1,
        'runs_in_over': 8,
        'dot_ball': 0,
        'batter_dismissal_rate': 0.06,
        'batter_avg_runs': 1.2,
        'bowler_wicket_rate': 0.08,
        'bowler_avg_runs': 1.1,
        'h2h_wicket_rate': 0.10,
        'h2h_avg_runs': 1.0,
        'batter_recent_runs': 12,
        'batter_recent_dots': 1,
        'bowler_recent_wickets': 1,
        'bowler_recent_runs': 7,
    }

    wicket_prob = predictor.predict_next_ball(example_state)
    print(f"\n🎯 Predicted wicket probability: {wicket_prob:.1%}")
    print(f"   (Baseline wicket rate: ~5.5%)")

    print("\n" + "="*60)
    print("✅ MODEL TRAINING COMPLETE")
    print("="*60)
    print(f"Use predictor.predict_next_ball(match_state) for predictions")

    return predictor


if __name__ == "__main__":
    predictor = main()
