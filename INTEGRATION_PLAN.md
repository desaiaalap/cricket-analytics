# Cricket Analytics Project - Integration with cricpy

## 🎯 Project Goal
Build a comprehensive T20 World Cup analytics pipeline using cricpy for data processing and analysis.

## 📁 Current Project Structure

```
cricket-analytics/
├── data/
│   ├── external/          # Raw YAML files from Cricsheet
│   │   ├── icc_mens_t20_world_cup_male/  (181 matches)
│   │   └── ilt20_male/                    (100 matches)
│   ├── raw/              # Converted CSV files (partial)
│   └── processed/        # Clean, aggregated data (to be created)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── scripts/
│       └── extract.py    # Old basic extraction (to be replaced)
└── main.py
```

## 🚀 Integration Strategy

Since cricpy package files aren't fully accessible, we'll use two approaches:

### Approach 1: Direct Import (Recommended)
Copy cricpy source code directly into cricket-analytics project:

```
cricket-analytics/
├── cricpy/               # Complete cricpy package copied here
│   ├── __init__.py
│   ├── io/
│   ├── parsers/
│   └── analytics/
└── [rest of project]
```

### Approach 2: Create Symlink
```bash
ln -s /Users/aalapdesai/CricpyProject/cricpy /Users/aalapdesai/cricket-analytics/cricpy
```

## 📊 New Project Structure (Target)

```
cricket-analytics/
├── cricpy/                       # cricpy package (local copy)
├── data/
│   ├── external/                # Raw YAML (unchanged)
│   ├── processed/              # NEW: Processed datasets
│   │   ├── all_deliveries.parquet      # All match deliveries
│   │   ├── match_summaries.csv         # Match-level stats
│   │   ├── player_batting.csv          # Player batting stats
│   │   ├── player_bowling.csv          # Player bowling stats
│   │   └── team_stats.csv              # Team-level stats
│   └── reports/                # NEW: Generated reports
├── notebooks/
│   ├── 01_data_processing.ipynb        # NEW: Load & process with cricpy
│   ├── 02_batting_analysis.ipynb       # NEW: Batting insights
│   ├── 03_bowling_analysis.ipynb       # NEW: Bowling insights
│   ├── 04_team_comparisons.ipynb       # NEW: Team analysis
│   └── 05_match_predictions.ipynb      # NEW: Predictive models
├── scripts/
│   ├── process_all_matches.py          # NEW: Batch processing
│   ├── generate_reports.py             # NEW: Automated reports
│   └── utils.py                        # NEW: Helper functions
└── README.md                            # Project documentation
```

## 🔄 Migration Steps

### Step 1: Setup cricpy ✅
- Copy cricpy package to cricket-analytics
- Test imports work correctly

### Step 2: Data Processing Pipeline
Create `scripts/process_all_matches.py`:
```python
from cricpy import load_all_yaml, parse_match, parse_match_info
import pandas as pd

# Load all 181 T20 World Cup matches
matches = load_all_yaml('data/external/icc_mens_t20_world_cup_male')

# Process into datasets
all_deliveries = []
match_summaries = []

for filename, match_data in matches:
    # Delivery-level data
    df = parse_match(match_data)
    df['match_id'] = filename
    all_deliveries.append(df)

    # Match summary
    info = parse_match_info(match_data)
    match_summaries.append(info)

# Save processed data
pd.concat(all_deliveries).to_parquet('data/processed/all_deliveries.parquet')
pd.DataFrame(match_summaries).to_csv('data/processed/match_summaries.csv')
```

### Step 3: Analysis Notebooks
Build comprehensive analysis using cricpy's analytics functions

### Step 4: Visualization & Insights
Create compelling visualizations and derive insights

## 💡 Analysis Ideas

### Batting Analysis:
- Top run scorers across tournaments
- Strike rate comparisons by batting position
- Powerplay vs death overs performance
- Partnership analysis
- Boundary hitting patterns

### Bowling Analysis:
- Most wickets and best economy rates
- Powerplay specialists vs death bowlers
- Dot ball percentages
- Bowling in different match situations
- Wicket-taking patterns

### Team Analysis:
- Tournament performance trends (2014-2024)
- Home vs away performance
- Batting first vs chasing
- Toss impact analysis

### Match Insights:
- Venue-specific patterns
- Impact of powerplay performance on outcomes
- Winning margins analysis
- Close match characteristics

## 📈 Next Actions

1. ✅ Copy cricpy package
2. Create process_all_matches.py
3. Generate processed datasets
4. Build analysis notebooks
5. Create visualizations
6. Document findings

---

**Ready to build something awesome!** 🚀
