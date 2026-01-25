"""
Comprehensive Next-Ball Prediction System
Predicts multiple outcomes for the very next delivery:
- Wicket probability
- Runs scored (0, 1, 2, 3, 4, 6)
- Boundary probability (4 or 6)
- Extras probability
- Dot ball probability
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report, roc_auc_score, mean_squared_error, accuracy_score
import warnings
warnings.filterwarnings('ignore')


class NextBallPredictor:
    """Comprehensive prediction system for next ball outcomes"""

    def __init__(self, data_path="data/processed/all_deliveries.csv"):
        self.data_path = Path(data_path)
        self.models = {}
        self.feature_columns = []
        self.df = None

    def load_data(self):
        """Load ball-by-ball delivery data"""
        print("📊 Loading ball-by-ball data...")
        self.df = pd.read_csv(self.data_path)
        print(f"✅ Loaded {len(self.df):,} deliveries")
        return self

    def engineer_features(self):
        """Create features for all predictions"""
        print("\n🔧 Engineering features for predictions...")

        df = self.df.copy()

        # Parse ball number into over and ball
        df['ball_str'] = df['ball'].astype(str)
        df['over_number'] = df['ball_str'].str.split('.').str[0].astype(float)
        df['ball_number'] = df['ball_str'].str.split('.').str[1].astype(float)

        # Target variables
        df['is_wicket'] = (~df['dismissal'].isna()).astype(int)
        df['runs'] = df['runs_batter'].fillna(0).astype(int)
        df['is_boundary'] = (df['runs'].isin([4, 6])).astype(int)
        df['is_four'] = (df['runs'] == 4).astype(int)
        df['is_six'] = (df['runs'] == 6).astype(int)
        df['is_dot'] = (df['runs_total'] == 0).astype(int)
        df['has_extras'] = (~df['extras_type'].isna()).astype(int)

        # Match phase
        df['phase'] = pd.cut(df['over_number'],
                            bins=[-1, 6, 16, 20],
                            labels=['powerplay', 'middle', 'death'])
        df['is_powerplay'] = (df['phase'] == 'powerplay').astype(int)
        df['is_middle'] = (df['phase'] == 'middle').astype(int)
        df['is_death'] = (df['phase'] == 'death').astype(int)

        # Sort by match and delivery order
        df = df.sort_values(['match_id', 'inning', 'over_number', 'ball_number'])

        # Rename columns to match code
        df = df.rename(columns={'batsman': 'batter', 'over': 'over_number'})

        # Cumulative match state - SHIFT to avoid leakage (only use PAST info)
        df['wickets_lost'] = df.groupby(['match_id', 'inning'])['is_wicket'].cumsum().shift(1).fillna(0)
        df['runs_scored'] = df.groupby(['match_id', 'inning'])['runs_total'].cumsum().shift(1).fillna(0)
        df['balls_bowled'] = df.groupby(['match_id', 'inning']).cumcount()  # This is OK (counts before current)
        df['boundaries_hit'] = df.groupby(['match_id', 'inning'])['is_boundary'].cumsum().shift(1).fillna(0)

        # Current run rate and required run rate
        df['current_run_rate'] = df['runs_scored'] / ((df['balls_bowled'] + 1) / 6)
        df['current_run_rate'] = df['current_run_rate'].fillna(0)

        # Pressure indicators - SHIFT to avoid leakage
        df['runs_in_over'] = df.groupby(['match_id', 'inning', 'over_number'])['runs_total'].cumsum().shift(1).fillna(0)
        df['wickets_in_over'] = df.groupby(['match_id', 'inning', 'over_number'])['is_wicket'].cumsum().shift(1).fillna(0)
        df['dots_in_over'] = df.groupby(['match_id', 'inning', 'over_number'])['is_dot'].cumsum().shift(1).fillna(0)

        # Batter stats (overall performance)
        batter_stats = df.groupby('batter').agg({
            'is_wicket': 'mean',
            'runs': 'mean',
            'is_boundary': 'mean',
            'is_dot': 'mean',
        }).reset_index()
        batter_stats.columns = ['batter', 'batter_dismissal_rate', 'batter_avg_runs',
                                'batter_boundary_rate', 'batter_dot_rate']
        df = df.merge(batter_stats, on='batter', how='left')

        # Bowler stats
        bowler_stats = df.groupby('bowler').agg({
            'is_wicket': 'mean',
            'runs_total': 'mean',
            'is_boundary': 'mean',
            'is_dot': 'mean',
            'has_extras': 'mean',
        }).reset_index()
        bowler_stats.columns = ['bowler', 'bowler_wicket_rate', 'bowler_economy',
                                'bowler_boundary_rate', 'bowler_dot_rate', 'bowler_extras_rate']
        df = df.merge(bowler_stats, on='bowler', how='left')

        # Head-to-head matchup
        h2h = df.groupby(['batter', 'bowler']).agg({
            'is_wicket': 'mean',
            'runs': 'mean',
            'is_boundary': 'mean',
        }).reset_index()
        h2h.columns = ['batter', 'bowler', 'h2h_wicket_rate', 'h2h_avg_runs', 'h2h_boundary_rate']
        df = df.merge(h2h, on=['batter', 'bowler'], how='left')

        # Recent form (last 6 balls for batter) - SHIFT to avoid leakage
        for col in ['runs', 'is_dot', 'is_boundary', 'is_wicket']:
            df[f'batter_recent_{col}'] = (df.groupby(['match_id', 'inning', 'batter'])[col]
                                          .transform(lambda x: x.rolling(6, min_periods=1).sum().shift(1).fillna(0)))

        # Bowler recent form (last 6 balls) - SHIFT to avoid leakage
        for col in ['is_wicket', 'runs_total', 'is_boundary', 'is_dot']:
            df[f'bowler_recent_{col}'] = (df.groupby(['match_id', 'inning', 'bowler'])[col]
                                          .transform(lambda x: x.rolling(6, min_periods=1).sum().shift(1).fillna(0)))

        # Momentum indicators (last 12 balls for team) - SHIFT to avoid leakage
        df['team_recent_runs'] = (df.groupby(['match_id', 'inning'])['runs_total']
                                  .transform(lambda x: x.rolling(12, min_periods=1).sum().shift(1).fillna(0)))
        df['team_recent_wickets'] = (df.groupby(['match_id', 'inning'])['is_wicket']
                                     .transform(lambda x: x.rolling(12, min_periods=1).sum().shift(1).fillna(0)))

        # Strike rotation
        df['batter_strike_rate'] = (df['batter_recent_runs'] / 6) * 100
        df['batter_strike_rate'] = df['batter_strike_rate'].fillna(100)

        # Fill missing values (numeric columns only)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        self.df = df
        print(f"✅ Created {len(df.columns)} total columns")
        print(f"\n📊 Target variable distributions:")
        print(f"   Wickets: {df['is_wicket'].sum():,} ({df['is_wicket'].mean()*100:.2f}%)")
        print(f"   Dots: {df['is_dot'].sum():,} ({df['is_dot'].mean()*100:.2f}%)")
        print(f"   Boundaries: {df['is_boundary'].sum():,} ({df['is_boundary'].mean()*100:.2f}%)")
        print(f"   Fours: {df['is_four'].sum():,} ({df['is_four'].mean()*100:.2f}%)")
        print(f"   Sixes: {df['is_six'].sum():,} ({df['is_six'].mean()*100:.2f}%)")
        print(f"   Extras: {df['has_extras'].sum():,} ({df['has_extras'].mean()*100:.2f}%)")

        return self

    def prepare_training_data(self):
        """Prepare features and targets"""
        print("\n📋 Preparing training data...")

        # Select features
        self.feature_columns = [
            # Ball context
            'over_number', 'ball_number', 'is_powerplay', 'is_middle', 'is_death',

            # Match state
            'wickets_lost', 'runs_scored', 'balls_bowled', 'current_run_rate',
            'boundaries_hit', 'runs_in_over', 'wickets_in_over', 'dots_in_over',

            # Player stats
            'batter_dismissal_rate', 'batter_avg_runs', 'batter_boundary_rate', 'batter_dot_rate',
            'bowler_wicket_rate', 'bowler_economy', 'bowler_boundary_rate',
            'bowler_dot_rate', 'bowler_extras_rate',

            # Head-to-head
            'h2h_wicket_rate', 'h2h_avg_runs', 'h2h_boundary_rate',

            # Recent form - batter
            'batter_recent_runs', 'batter_recent_is_dot', 'batter_recent_is_boundary',
            'batter_recent_is_wicket', 'batter_strike_rate',

            # Recent form - bowler
            'bowler_recent_is_wicket', 'bowler_recent_runs_total',
            'bowler_recent_is_boundary', 'bowler_recent_is_dot',

            # Team momentum
            'team_recent_runs', 'team_recent_wickets',
        ]

        X = self.df[self.feature_columns]

        # Multiple targets
        targets = {
            'wicket': self.df['is_wicket'],
            'runs': self.df['runs'],
            'boundary': self.df['is_boundary'],
            'four': self.df['is_four'],
            'six': self.df['is_six'],
            'dot': self.df['is_dot'],
            'extras': self.df['has_extras'],
        }

        # Temporal split (80/20)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]

        y_train = {k: v[:split_idx] for k, v in targets.items()}
        y_test = {k: v[split_idx:] for k, v in targets.items()}

        print(f"✅ Training set: {len(X_train):,} balls")
        print(f"✅ Test set: {len(X_test):,} balls")

        return X_train, X_test, y_train, y_test

    def train_all_models(self, X_train, y_train):
        """Train separate models for each outcome"""
        print("\n🤖 Training prediction models...")

        # 1. Wicket prediction (binary)
        print("\n1️⃣ Training wicket predictor...")
        self.models['wicket'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=100,
            min_samples_leaf=50,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['wicket'].fit(X_train, y_train['wicket'])
        print("   ✅ Wicket model trained")

        # 2. Runs prediction (multiclass: 0,1,2,3,4,6)
        print("\n2️⃣ Training runs predictor...")
        self.models['runs'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            min_samples_split=50,
            random_state=42,
            n_jobs=-1
        )
        self.models['runs'].fit(X_train, y_train['runs'])
        print("   ✅ Runs model trained")

        # 3. Boundary prediction (binary)
        print("\n3️⃣ Training boundary predictor...")
        self.models['boundary'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['boundary'].fit(X_train, y_train['boundary'])
        print("   ✅ Boundary model trained")

        # 4. Four prediction (binary)
        print("\n4️⃣ Training four predictor...")
        self.models['four'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['four'].fit(X_train, y_train['four'])
        print("   ✅ Four model trained")

        # 5. Six prediction (binary)
        print("\n5️⃣ Training six predictor...")
        self.models['six'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['six'].fit(X_train, y_train['six'])
        print("   ✅ Six model trained")

        # 6. Dot ball prediction (binary)
        print("\n6️⃣ Training dot ball predictor...")
        self.models['dot'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['dot'].fit(X_train, y_train['dot'])
        print("   ✅ Dot ball model trained")

        # 7. Extras prediction (binary)
        print("\n7️⃣ Training extras predictor...")
        self.models['extras'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['extras'].fit(X_train, y_train['extras'])
        print("   ✅ Extras model trained")

        print(f"\n✅ All {len(self.models)} models trained successfully")
        return self

    def evaluate_all_models(self, X_test, y_test):
        """Evaluate all prediction models"""
        print("\n" + "="*80)
        print("MODEL EVALUATION RESULTS")
        print("="*80)

        results = {}

        for name, model in self.models.items():
            print(f"\n{'='*80}")
            print(f"📊 {name.upper()} PREDICTION")
            print(f"{'='*80}")

            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)

            if name == 'runs':
                # Multiclass accuracy
                accuracy = accuracy_score(y_test[name], y_pred)
                print(f"\nAccuracy: {accuracy:.4f}")

                # Distribution
                print(f"\nPredicted run distribution:")
                pred_dist = pd.Series(y_pred).value_counts().sort_index()
                actual_dist = y_test[name].value_counts().sort_index()

                for runs in sorted(set(list(pred_dist.index) + list(actual_dist.index))):
                    pred_pct = pred_dist.get(runs, 0) / len(y_pred) * 100
                    actual_pct = actual_dist.get(runs, 0) / len(y_test[name]) * 100
                    print(f"  {runs} runs: Predicted {pred_pct:5.2f}% | Actual {actual_pct:5.2f}%")

            else:
                # Binary classification
                if len(set(y_test[name])) > 1:  # Check if both classes exist
                    auc = roc_auc_score(y_test[name], y_pred_proba[:, 1])
                    print(f"\nROC AUC: {auc:.4f}")

                print(f"\n{classification_report(y_test[name], y_pred, digits=3)}")

            # Feature importance (top 5)
            if hasattr(model, 'feature_importances_'):
                print(f"\nTop 5 important features:")
                importances = pd.DataFrame({
                    'feature': self.feature_columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False).head(5)

                for idx, row in importances.iterrows():
                    print(f"  {row['feature']:35s} {row['importance']:.4f}")

            results[name] = {
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }

        return results

    def predict_next_ball(self, match_state):
        """
        Predict all outcomes for next ball

        Args:
            match_state (dict): Current match situation

        Returns:
            dict: Probabilities for all outcomes
        """
        if not self.models:
            raise ValueError("Models not trained. Call train_all_models() first.")

        # Create feature vector
        features = pd.DataFrame([match_state])[self.feature_columns]

        predictions = {}

        # Get predictions from all models
        predictions['wicket_prob'] = self.models['wicket'].predict_proba(features)[0, 1]
        predictions['dot_prob'] = self.models['dot'].predict_proba(features)[0, 1]
        predictions['boundary_prob'] = self.models['boundary'].predict_proba(features)[0, 1]
        predictions['four_prob'] = self.models['four'].predict_proba(features)[0, 1]
        predictions['six_prob'] = self.models['six'].predict_proba(features)[0, 1]
        predictions['extras_prob'] = self.models['extras'].predict_proba(features)[0, 1]

        # Runs distribution
        runs_proba = self.models['runs'].predict_proba(features)[0]
        runs_classes = self.models['runs'].classes_
        predictions['runs_distribution'] = {
            int(runs): float(prob)
            for runs, prob in zip(runs_classes, runs_proba)
        }

        # Most likely runs
        predictions['expected_runs'] = int(runs_classes[np.argmax(runs_proba)])

        return predictions

    def save_models(self, filepath="scripts/ml/next_ball_models.pkl"):
        """Save all trained models"""
        model_data = {
            'models': self.models,
            'feature_columns': self.feature_columns
        }

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"\n💾 All models saved to {filepath}")

    def load_models(self, filepath="scripts/ml/next_ball_models.pkl"):
        """Load trained models"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.models = model_data['models']
        self.feature_columns = model_data['feature_columns']

        print(f"✅ Loaded {len(self.models)} models from {filepath}")
        return self


def main():
    """Train and evaluate comprehensive next-ball prediction system"""
    print("="*80)
    print("COMPREHENSIVE NEXT-BALL PREDICTION SYSTEM")
    print("="*80)

    # Initialize
    predictor = NextBallPredictor()

    # Prepare data
    predictor.load_data()
    predictor.engineer_features()
    X_train, X_test, y_train, y_test = predictor.prepare_training_data()

    # Train all models
    predictor.train_all_models(X_train, y_train)

    # Evaluate
    results = predictor.evaluate_all_models(X_test, y_test)

    # Save models
    predictor.save_models()

    # Example prediction
    print("\n" + "="*80)
    print("EXAMPLE: DEATH OVERS PREDICTION")
    print("="*80)
    print("Scenario: Over 18.3, 2 wickets down, batter on fire, pressure situation")

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
        'boundaries_hit': 15,
        'runs_in_over': 8,
        'wickets_in_over': 0,
        'dots_in_over': 1,
        'batter_dismissal_rate': 0.06,
        'batter_avg_runs': 1.4,
        'batter_boundary_rate': 0.25,
        'batter_dot_rate': 0.30,
        'bowler_wicket_rate': 0.08,
        'bowler_economy': 1.1,
        'bowler_boundary_rate': 0.12,
        'bowler_dot_rate': 0.40,
        'bowler_extras_rate': 0.05,
        'h2h_wicket_rate': 0.10,
        'h2h_avg_runs': 1.2,
        'h2h_boundary_rate': 0.20,
        'batter_recent_runs': 18,
        'batter_recent_is_dot': 1,
        'batter_recent_is_boundary': 2,
        'batter_recent_is_wicket': 0,
        'batter_strike_rate': 180.0,
        'bowler_recent_is_wicket': 1,
        'bowler_recent_runs_total': 8,
        'bowler_recent_is_boundary': 1,
        'bowler_recent_is_dot': 2,
        'team_recent_runs': 22,
        'team_recent_wickets': 0,
    }

    predictions = predictor.predict_next_ball(example_state)

    print(f"\n🎯 PREDICTIONS FOR NEXT BALL:")
    print(f"   {'Wicket probability:':<25} {predictions['wicket_prob']:>6.1%}")
    print(f"   {'Dot ball probability:':<25} {predictions['dot_prob']:>6.1%}")
    print(f"   {'Boundary probability:':<25} {predictions['boundary_prob']:>6.1%}")
    print(f"   {'  - Four:':<25} {predictions['four_prob']:>6.1%}")
    print(f"   {'  - Six:':<25} {predictions['six_prob']:>6.1%}")
    print(f"   {'Extras probability:':<25} {predictions['extras_prob']:>6.1%}")

    print(f"\n📊 RUNS DISTRIBUTION:")
    for runs, prob in sorted(predictions['runs_distribution'].items()):
        bar = '█' * int(prob * 50)
        print(f"   {runs} runs: {prob:>6.1%} {bar}")

    print(f"\n💡 Most likely outcome: {predictions['expected_runs']} runs")

    print("\n" + "="*80)
    print("✅ SYSTEM READY FOR PREDICTIONS")
    print("="*80)

    return predictor


if __name__ == "__main__":
    predictor = main()
