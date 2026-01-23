# T20 World Cup Cricket Analytics

> Comprehensive analysis of ICC Men's T20 World Cup tournaments (2014-2024) using cricpy-powered data processing

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Data Source](https://img.shields.io/badge/Data-Cricsheet-green.svg)](https://cricsheet.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()
[![Tests](https://img.shields.io/badge/Tests-37%2B%20Passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-80%25%2B-green.svg)]()

---

## 📊 Project Overview

This project provides end-to-end analytics of T20 World Cup cricket, covering **181 matches** across **5 tournament editions** (2014, 2016, 2021, 2022, 2024). It includes delivery-level data processing, player performance analysis, match insights, and comprehensive visualizations.

### Key Statistics
- **40,966** ball-by-ball records
- **525** unique batsmen analyzed
- **372** unique bowlers analyzed
- **49,225** total runs scored
- **2,252** total wickets taken

---

## 🎯 Project Goals

1. **Data Processing**: Convert raw Cricsheet YAML files into structured, analysis-ready datasets
2. **Player Analysis**: Identify top performers, patterns, and trends in batting and bowling
3. **Match Insights**: Understand winning factors, toss impact, and team dynamics
4. **Visualizations**: Create compelling charts and insights
5. **Predictions**: Build models for match outcome prediction (future work)

---

## 📁 Project Structure

```
cricket-analytics/
├── data/
│   ├── external/                    # Raw YAML files from Cricsheet
│   │   ├── icc_mens_t20_world_cup_male/  (181 matches)
│   │   └── ilt20_male/                   (100 matches)
│   └── processed/                   # ✨ Processed datasets
│       ├── all_deliveries.csv       # 40,966 ball-by-ball records
│       ├── match_summaries.csv      # 181 match metadata
│       ├── player_batting_stats.csv # 525 batsmen aggregates
│       └── player_bowling_stats.csv # 372 bowlers aggregates
│
├── scripts/
│   ├── cricpy_loader.py             # Data loading utilities (cricpy functions)
│   ├── cricsheet_downloader.py      # ✨ Automated data download from Cricsheet
│   ├── download_example.py          # Download usage examples
│   └── process_all_matches.py       # Batch processing pipeline
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Initial exploration
│   ├── 02_batting_analysis.ipynb    # ⭐ Comprehensive batting analysis
│   ├── 03_bowling_analysis.ipynb    # ⭐ Comprehensive bowling analysis
│   └── 04_match_insights.ipynb      # ⭐ Match-level insights
│
├── docs/
│   ├── DATA_PROCESSING_SUMMARY.md   # Processing results summary
│   ├── PROJECT_SUMMARY.md           # Comprehensive overview
│   └── CRICSHEET_DOWNLOADER_GUIDE.md # ✨ Download automation guide
│
├── DATA_PROCESSING_SUMMARY.md       # Processing results summary
├── INTEGRATION_PLAN.md              # Project integration notes
├── .gitignore                       # ✨ Git ignore rules
└── README.md                        # This file
```

---

## 🚀 Quick Start

### 1. Download Data (New Feature!)

**Option A: Automated Download (Recommended)**
```python
from scripts.cricsheet_downloader import download_cricsheet_data

# Download T20 World Cup data automatically
data_path = download_cricsheet_data('t20_internationals_male', 'data/external')
```

**Option B: Manual Download**
- Visit [Cricsheet.org](https://cricsheet.org/downloads/)
- Download desired tournament ZIP file
- Extract to `data/external/`

👉 **[See full download guide](docs/CRICSHEET_DOWNLOADER_GUIDE.md)**

### 2. Data Processing

Process all T20 World Cup matches into structured datasets:

```bash
python scripts/process_all_matches.py
```

**Output:**
- Creates 4 CSV files in `data/processed/`
- Processes 181 matches in <2 minutes
- 100% success rate, zero data loss

### 3. Analysis Notebooks

Run the Jupyter notebooks to explore insights:

```bash
jupyter notebook
```

**Recommended Order:**
1. `02_batting_analysis.ipynb` - Discover top run scorers, strike rates, boundary patterns
2. `03_bowling_analysis.ipynb` - Analyze wicket takers, economy rates, dismissal types
3. `04_match_insights.ipynb` - Understand toss impact, team performance, winning factors

---

## 🏆 Key Findings

### Top Performers (All Tournaments Combined)

#### 🏏 Batting Champions
| Rank | Player | Runs | Average | Strike Rate | Matches |
|------|--------|------|---------|-------------|---------|
| 1 | Virat Kohli | 1,083 | 57.0 | 130.8 | 27 |
| 2 | Jos Buttler | 949 | 45.2 | 151.8 | 27 |
| 3 | Rohit Sharma | 753 | 27.9 | 131.6 | 28 |
| 4 | Kane Williamson | 642 | 35.7 | 116.5 | 22 |
| 5 | David Warner | 638 | - | 141.9 | - |

#### ⚾ Bowling Champions
| Rank | Player | Wickets | Economy | Average | Matches |
|------|--------|---------|---------|---------|---------|
| 1 | Shakib Al Hasan | 39 | 7.18 | 18.7 | 28 |
| 2 | Anrich Nortje | 38 | 5.89 | 11.1 | 18 |
| 3 | Wanindu Hasaranga | 35 | 6.17 | 12.1 | 18 |
| 4 | Chris Jordan | 34 | 7.89 | 17.3 | 22 |
| 5 | Adam Zampa | 32 | 6.45 | 14.3 | 19 |

### Match Insights

- **Toss Impact**: Team winning toss wins match ~52% of the time
- **Preferred Decision**: Teams choose to field first 62% of the time
- **Most Common Dismissal**: Caught (45% of all wickets)
- **Average Match Score**: ~160 runs per innings

---

## 📈 Analysis Highlights

### Batting Analysis
- ✅ Strike rate vs average comparisons
- ✅ Boundary hitting patterns (fours vs sixes)
- ✅ Consistency metrics and player rankings
- ✅ Tournament evolution analysis

### Bowling Analysis
- ✅ Economy rate vs wickets analysis
- ✅ Wicket-taking efficiency metrics
- ✅ Dismissal type distribution
- ✅ Powerplay vs death bowling specialists

### Match Insights
- ✅ Toss impact on match outcomes
- ✅ Team performance rankings
- ✅ Venue analysis
- ✅ Winning margin patterns

---

## 🛠️ Technologies Used

- **Python 3.10**: Core programming language
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib & Seaborn**: Data visualization
- **Jupyter**: Interactive notebooks
- **PyYAML**: YAML file parsing
- **cricpy** (custom): Cricket data processing utilities

---

## 📊 Datasets Description

### 1. all_deliveries.csv (2.7 MB)
Ball-by-ball records with columns:
- Match metadata: `match_id`, `inning`, `batting_team`
- Delivery details: `ball`, `batsman`, `bowler`
- Runs: `runs_total`, `runs_batter`, `runs_extras`
- Events: `extras_type`, `dismissal`, `fielder`

### 2. match_summaries.csv (37 KB)
Match-level information:
- Teams, venue, date, city
- Toss details (winner, decision)
- Match outcome (winner, margin)
- Player of the match

### 3. player_batting_stats.csv (20 KB)
Aggregated batting statistics:
- Runs, balls faced, dismissals
- Average, strike rate
- Boundaries (fours, sixes)
- Number of matches played

### 4. player_bowling_stats.csv (16 KB)
Aggregated bowling statistics:
- Wickets, balls bowled, runs conceded
- Economy, average, strike rate
- Overs bowled, matches played

---

## ✨ New Features (January 2026)

### 📥 Automated Data Download
No more manual downloads! Use the built-in Cricsheet downloader:

```python
from scripts.cricsheet_downloader import download_cricsheet_data

# Download any tournament with one line
data_path = download_cricsheet_data('ipl', 'data/external')
```

**Supported tournaments:**
- IPL, BBL, CPL, PSL (T20 Leagues)
- T20 World Cups (Men's & Women's)
- ODIs, Tests, and more

👉 **[Full Download Guide](docs/CRICSHEET_DOWNLOADER_GUIDE.md)**

### 🧪 Comprehensive Testing & CI/CD
Professional test suite with automated quality assurance:

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Pre-commit checks
make pre-commit
```

**Features:**
- 37+ unit and integration tests
- Multi-OS testing (Linux, Windows, macOS)
- Multi-Python testing (3.8-3.11)
- GitHub Actions automation
- Code quality checks (flake8, black, isort)

👉 **[Full Testing Guide](docs/TESTING_GUIDE.md)**

### 🔒 Git Integration
Added comprehensive `.gitignore` to exclude:
- Large CSV/YAML data files
- Python cache files
- Jupyter notebook checkpoints
- System files

Ready for GitHub push without bloat!

---

## 💡 Future Enhancements

### Phase 1: Advanced Analytics (In Progress)
- [ ] Powerplay vs death overs analysis
- [ ] Player form trends over time
- [ ] Head-to-head player comparisons
- [ ] Partnership analysis

### Phase 2: Predictive Modeling
- [ ] Match outcome prediction model
- [ ] Player performance forecasting
- [ ] Team strength ratings
- [ ] Win probability calculator

### Phase 3: Interactive Dashboard
- [ ] Streamlit/Dash web application
- [ ] Real-time statistics lookup
- [ ] Interactive visualizations
- [ ] Player comparison tool

---

## 🙏 Acknowledgments

- **[Cricsheet](https://cricsheet.org/)** - For providing comprehensive cricket data in YAML format
- **ICC** - For organizing the T20 World Cup tournaments
- **cricpy** - Custom Python package for cricket data processing (developed for this project)

---

## 📝 License

This project is for educational and analytical purposes. Data sourced from Cricsheet under their terms of use.

---

## 👨‍💻 Author

**Aalap Desai**
- Email: adesai@altsportsdata.com
- Project: T20 World Cup Analytics

---

## 📌 Project Status

**Current Status**: ✅ **Core Analysis Complete**

- ✅ Data processing pipeline (100% complete)
- ✅ Batting analysis notebook (Complete)
- ✅ Bowling analysis notebook (Complete)
- ✅ Match insights notebook (Complete)
- 🔄 Advanced analytics (In progress)
- 📅 Predictive modeling (Planned)

---

**Last Updated**: January 2026
