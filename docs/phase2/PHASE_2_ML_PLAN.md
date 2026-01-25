# Phase 2: Machine Learning Features

## 🎯 Objectives

Build 4 core ML prediction systems using the existing 40,966 ball-by-ball dataset:

1. ✅ **Match Outcome Prediction** - Predict match winners before the game
2. ✅ **Player Performance Forecasting** - Predict individual player stats
3. ✅ **Team Strength Ratings** - Calculate dynamic team power rankings
4. ✅ **Win Probability Calculator** - Live win% tracking during matches

---

## 1️⃣ Match Outcome Prediction

### Goal
Predict which team will win BEFORE the match starts based on:
- Team strength ratings
- Head-to-head history
- Venue/conditions
- Recent form

### Features to Engineer
```python
# Team features
- team_win_rate (overall)
- team_win_rate_venue (at this ground)
- team_batting_first_win_rate
- team_chasing_win_rate
- recent_form_5_matches

# Head-to-head
- h2h_win_rate
- h2h_at_venue

# Venue
- venue_avg_first_innings_score
- venue_chasing_success_rate
- venue_total_matches

# Toss
- toss_impact_at_venue
```

### Model
- **Algorithm**: Logistic Regression or Random Forest
- **Training data**: Match-level features from 181 matches
- **Output**: Win probability for each team (0-100%)
- **Validation**: Cross-validation by tournament year

### Deliverable
`scripts/ml/match_predictor.py` - Predict match winners

---

## 2️⃣ Player Performance Forecasting

### Goal
Predict a player's performance in their next match:
- **Batters**: Runs scored, strike rate, boundaries
- **Bowlers**: Wickets taken, economy rate, overs bowled

### Features to Engineer
```python
# Player stats
- career_average
- career_strike_rate / economy
- recent_form_3_matches
- recent_form_10_matches
- performance_vs_opponent
- performance_at_venue

# Opposition strength
- opponent_bowling_strength (for batters)
- opponent_batting_strength (for bowlers)

# Match context
- batting_position (for batters)
- powerplay_specialist / death_specialist (for bowlers)
```

### Models
**Batter Forecast:**
- Runs: Regression (Linear, Random Forest)
- Boundaries: Poisson regression
- Strike Rate: Regression

**Bowler Forecast:**
- Wickets: Poisson regression
- Economy: Regression
- Overs: Classification (4, 3, 2, 1)

### Deliverable
`scripts/ml/player_forecaster.py` - Predict individual player stats

---

## 3️⃣ Team Strength Ratings

### Goal
Calculate dynamic power rankings for all teams based on:
- Recent match results
- Quality of opposition beaten
- Margin of victory
- Venue performance

### Algorithm: ELO Rating System

```python
# ELO for cricket teams
initial_rating = 1500

def update_elo(winner_rating, loser_rating, margin_factor, k=32):
    expected_win = 1 / (1 + 10**((loser_rating - winner_rating) / 400))

    # Adjust for margin (close match vs blowout)
    new_winner = winner_rating + k * margin_factor * (1 - expected_win)
    new_loser = loser_rating + k * margin_factor * (0 - (1 - expected_win))

    return new_winner, new_loser
```

**Margin factor:**
- Close match (< 10 runs or < 2 wickets): 1.0
- Comfortable (10-30 runs or 2-5 wickets): 1.2
- Dominant (> 30 runs or > 5 wickets): 1.5

### Features
- Current ELO rating
- Rating change over time
- Relative strength vs other teams
- Form trajectory (improving/declining)

### Deliverable
`scripts/ml/team_ratings.py` - Calculate and track team ELO ratings

---

## 4️⃣ Win Probability Calculator

### Goal
Calculate live win probability **during** a match based on current state:
- Current score
- Wickets lost
- Overs remaining
- Required run rate
- Historical similar situations

### Approach: Situation-based Model

Train on **every ball state** in the dataset:

```python
# State features (for team batting second)
- runs_needed
- balls_remaining
- wickets_in_hand
- current_run_rate
- required_run_rate
- team_strength_diff (ELO difference)

# Historical lookup
- similar_situations (same runs needed ± 10, same wickets, same overs)
- success_rate_in_similar_situations
```

### Model
- **Algorithm**: Logistic Regression or Gradient Boosting
- **Training**: All 40,966 balls with outcome label (did batting team win?)
- **Output**: Win probability after each ball (0-100%)

### Deliverable
`scripts/ml/win_probability.py` - Live win% calculator
`dashboard/win_probability_tracker.py` - Dashboard showing win% chart

---

## 📁 File Structure

```
scripts/ml/
├── match_predictor.py          # Pre-match outcome prediction
├── player_forecaster.py        # Player performance forecasting
├── team_ratings.py             # ELO rating system
├── win_probability.py          # Live win% calculator
└── models/
    ├── match_outcome_model.pkl
    ├── batter_forecast_model.pkl
    ├── bowler_forecast_model.pkl
    ├── team_elo_ratings.csv
    └── win_prob_model.pkl

dashboard/
├── match_predictions.py        # Pre-match prediction dashboard
├── player_forecast.py          # Player performance predictions
├── team_rankings.py            # Live team strength rankings
└── win_probability_live.py     # Live win% tracker
```

---

## 🚀 Implementation Order

### Week 1: Team Strength Ratings ✅
**Why first?** Needed as input for other models
- Build ELO rating system
- Process all 181 matches chronologically
- Generate team ratings over time
- Visualize rating changes

### Week 2: Match Outcome Prediction
**Uses:** Team ratings
- Engineer match-level features
- Train pre-match prediction model
- Validate on recent tournaments
- Build prediction dashboard

### Week 3: Win Probability Calculator
**Uses:** Team ratings
- Engineer ball-by-ball state features
- Train live win% model
- Create dynamic win% charts
- Integrate into match viewer

### Week 4: Player Performance Forecasting
**Uses:** Team ratings, match predictions
- Build batter forecasting models
- Build bowler forecasting models
- Validate accuracy
- Create forecast dashboard

---

## 📊 Success Metrics

### Match Outcome Prediction
- **Target**: 70%+ accuracy on test set
- **Baseline**: Random guessing = 50%
- **Professional systems**: 65-75%

### Player Forecasting
- **Batters**: MAE < 10 runs on average
- **Bowlers**: MAE < 0.5 wickets on average
- **Baseline**: Mean prediction

### Team Ratings
- **Validation**: Higher-rated team should win 70%+ of the time
- **Correlation**: ELO should correlate with ICC rankings

### Win Probability
- **Calibration**: When model says 70%, team should win 70% of the time
- **Accuracy**: Better than simple run rate comparison

---

## 🎯 Phase 2 Deliverables

1. **4 ML Models** (trained and saved)
2. **4 New Dashboards** (interactive prediction interfaces)
3. **Model Evaluation Reports** (accuracy, limitations)
4. **API Documentation** (how to use prediction functions)

---

## 💡 Key Insights to Discover

From Match Prediction:
- Which teams overperform/underperform vs expectations?
- Venue home advantages
- Toss impact by ground

From Player Forecasting:
- Consistent performers vs volatile players
- Matchup advantages (certain batters vs certain bowlers)
- Venue specialists

From Team Ratings:
- Team strength trends over tournaments
- Rise and fall of teams (2014-2024)
- Strength of different tournaments

From Win Probability:
- Most dramatic comebacks
- Choke points (when favorites lost)
- Clutch performances that swung matches

---

## 🔧 Technical Approach

### Data Preparation
```python
# scripts/ml/prepare_ml_data.py
def create_match_features():
    """Create match-level dataset for outcome prediction"""
    pass

def create_player_features():
    """Create player-level dataset for forecasting"""
    pass

def create_ball_features():
    """Create ball-by-ball dataset for win probability"""
    pass
```

### Model Training
```python
# Use scikit-learn (already installed)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import TimeSeriesSplit

# Temporal validation (no data leakage!)
tscv = TimeSeriesSplit(n_splits=5)
```

### Model Evaluation
```python
# Classification metrics
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss

# Regression metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Calibration
from sklearn.calibration import calibration_curve
```

---

## ⚠️ Data Leakage Prevention

**Critical rules:**
1. ✅ Only use information available BEFORE the prediction point
2. ✅ Temporal splits (train on old, test on new)
3. ✅ No future information in features (shift all cumulative stats)
4. ✅ Player stats calculated on past matches only

---

## 🎓 Learning from Next-Ball Prediction Mistakes

**What we learned:**
- Always shift cumulative features (`.shift(1)`)
- Validate with temporal splits
- Check feature leakage carefully
- Real accuracy is lower than leaked accuracy

**Apply to Phase 2:**
- Be extra careful with match-level features
- Player stats must be "as of yesterday"
- Team ratings updated AFTER matches only
- Win probability uses only current ball state

---

**Ready to start Phase 2!** 🚀

Which component should we build first?
1. Team Strength Ratings (recommended - foundation for others)
2. Match Outcome Prediction
3. Win Probability Calculator
4. Player Performance Forecasting
