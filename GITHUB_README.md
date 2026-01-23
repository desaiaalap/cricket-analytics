# 🏏 Cricket Analytics Lab

> A unified portfolio of data-driven cricket analytics projects using Cricsheet data, machine learning, and computer vision. Built with a focus on T20 format analysis.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Data Source](https://img.shields.io/badge/Data-Cricsheet-green.svg)](https://cricsheet.org/)
[![Status](https://img.shields.io/badge/Phase%201-Complete-success.svg)]()

---

## 🎯 Project Vision

A comprehensive cricket analytics portfolio showcasing:
- **Data Engineering** - ETL pipelines and data processing at scale
- **Statistical Analysis** - Performance metrics and player rankings
- **Machine Learning** - Predictive modeling for match outcomes
- **Computer Vision** - Player tracking and motion analysis
- **Interactive Dashboards** - Real-time scouting and comparison tools

**Goal**: Demonstrate strong storytelling, modeling, and real-time analytics techniques applied to cricket, transferable to other team sports.

---

## 📊 Projects Overview

### ✅ **Phase 1: T20 World Cup Analytics** (COMPLETE)

Comprehensive analysis of 181 T20 World Cup matches (2014-2024) with delivery-level granularity.

**What's Delivered:**
- 📊 **40,966 ball-by-ball records** processed
- 🏏 **525 batsmen** with complete statistics
- ⚾ **372 bowlers** with performance metrics
- 📈 **3 analysis notebooks** (Batting, Bowling, Match Insights)
- 💾 **4 production datasets** ready for further analysis

**Key Features:**
- Automated ETL pipeline processing Cricsheet YAML files
- Player performance rankings and comparisons
- Toss impact and winning factor analysis
- Tournament evolution trends (2014-2024)
- Professional visualizations and insights

👉 **[Explore Phase 1](docs/phase1_t20_analytics.md)**

---

### 🔄 **Phase 2: Match Outcome Prediction** (IN PROGRESS)

Machine learning models to predict T20 match outcomes based on historical data.

**Planned Features:**
- [ ] Feature engineering from delivery-level data
- [ ] Player form and momentum indicators
- [ ] Venue-specific performance metrics
- [ ] ML models (Random Forest, XGBoost, Neural Networks)
- [ ] Win probability calculator
- [ ] Model performance evaluation and comparison

**Datasets**: Using Phase 1 processed data + additional features

**Target Accuracy**: 65-70% match outcome prediction

👉 **Status**: Feature engineering in progress

---

### 📅 **Phase 3: T20 Scouting Dashboard** (PLANNED)

Interactive Tableau/Streamlit dashboard for player comparison and team analysis.

**Planned Features:**
- [ ] Player comparison tool (batting & bowling KPIs)
- [ ] Team strength ratings and head-to-head
- [ ] Form trends over time
- [ ] Powerplay vs death overs specialists
- [ ] Custom filters (venue, tournament, opponent)
- [ ] Export reports functionality

**Technology**: Tableau Public or Streamlit

**Target Users**: Coaches, analysts, fantasy cricket players

👉 **Status**: Design phase

---

### 📅 **Phase 4: Player Tracking with OpenCV** (PLANNED)

Computer vision analysis of bowling and fielding motion from match videos.

**Planned Features:**
- [ ] Bowler run-up and release point tracking
- [ ] Fielder positioning heat maps
- [ ] Ball trajectory analysis
- [ ] Bowling action classification
- [ ] Movement pattern analysis
- [ ] Video annotation tool

**Technology**: OpenCV, YOLO, MediaPipe

**Data Source**: Match highlights and footage

👉 **Status**: Research phase

---

### 📅 **Phase 5: Sentiment Analysis** (PLANNED)

Fan sentiment tracking around major T20 tournaments using social media data.

**Planned Features:**
- [ ] Twitter/Reddit sentiment analysis
- [ ] Player popularity trends
- [ ] Match excitement scoring
- [ ] Viral moment detection
- [ ] Geographic sentiment mapping
- [ ] Real-time dashboard

**Technology**: NLP, TextBlob/VADER, Twitter API

**Target Events**: T20 World Cup, IPL

👉 **Status**: Planned

---

## 📁 Repository Structure

```
cricket-analytics/
├── data/
│   ├── raw/                         # Original Cricsheet files
│   ├── processed/                   # ✅ Cleaned datasets (Phase 1)
│   │   ├── all_deliveries.csv       # 40,966 ball-by-ball records
│   │   ├── match_summaries.csv      # 181 match metadata
│   │   ├── player_batting_stats.csv # 525 batsmen aggregates
│   │   └── player_bowling_stats.csv # 372 bowlers aggregates
│   └── external/                    # Cricsheet YAML downloads
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # ✅ Initial EDA (Phase 1)
│   ├── 02_batting_analysis.ipynb    # ✅ Batting analytics (Phase 1)
│   ├── 03_bowling_analysis.ipynb    # ✅ Bowling analytics (Phase 1)
│   ├── 04_match_insights.ipynb      # ✅ Match insights (Phase 1)
│   ├── 05_feature_engineering.ipynb # 🔄 ML features (Phase 2)
│   └── 06_match_prediction.ipynb    # 📅 Prediction models (Phase 2)
│
├── scripts/
│   ├── cricpy_loader.py             # ✅ Data parsing utilities
│   ├── process_all_matches.py       # ✅ Batch processing pipeline
│   └── ml_pipeline.py               # 📅 ML training pipeline (Phase 2)
│
├── dashboards/
│   └── t20_scouting_dashboard/      # 📅 Interactive dashboard (Phase 3)
│
├── video_analysis/
│   ├── raw_videos/                  # 📅 Match footage (Phase 4)
│   ├── processed_frames/            # 📅 Extracted frames
│   └── tracking_output.csv          # 📅 Tracking data
│
├── src/
│   ├── etl/                         # ✅ Data processing modules
│   ├── modeling/                    # 📅 ML models (Phase 2)
│   └── tracking/                    # 📅 CV algorithms (Phase 4)
│
├── docs/
│   ├── phase1_t20_analytics.md      # ✅ Phase 1 documentation
│   ├── DATA_PROCESSING_SUMMARY.md   # ✅ Processing results
│   └── PROJECT_SUMMARY.md           # ✅ Comprehensive overview
│
├── blog_drafts/
│   └── t20_analytics_insights.md    # ✅ Blog post draft
│
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

**Legend:**
- ✅ Complete
- 🔄 In Progress
- 📅 Planned

---

## 🏆 Phase 1 Highlights (COMPLETE)

### Top Performers Discovered

#### 🏏 Batting Leaders
| Player | Runs | Average | Strike Rate | Tournaments |
|--------|------|---------|-------------|-------------|
| **Virat Kohli** | 1,083 | 57.0 | 130.8 | 27 matches |
| **Jos Buttler** | 949 | 45.2 | **151.8** | 27 matches |
| **Rohit Sharma** | 753 | 27.9 | 131.6 | 28 matches |

#### ⚾ Bowling Leaders
| Player | Wickets | Economy | Average | Tournaments |
|--------|---------|---------|---------|-------------|
| **Shakib Al Hasan** | 39 | 7.18 | 18.7 | 28 matches |
| **Anrich Nortje** | 38 | **5.89** | 11.1 | 18 matches |
| **Wanindu Hasaranga** | 35 | 6.17 | 12.1 | 18 matches |

### Key Insights
- ✅ Toss winners have 52% match win rate
- ✅ 62% of teams prefer fielding first
- ✅ Caught dismissals account for 45% of wickets
- ✅ Average T20 WC innings score: ~160 runs

---

## 🚀 Quick Start (Phase 1)

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn pyyaml jupyter
```

### Run Analysis
```bash
# 1. Process data (optional - datasets included)
python scripts/process_all_matches.py

# 2. Launch Jupyter notebooks
jupyter notebook

# 3. Open any analysis notebook:
#    - notebooks/02_batting_analysis.ipynb
#    - notebooks/03_bowling_analysis.ipynb
#    - notebooks/04_match_insights.ipynb
```

### Quick Data Access
```python
import pandas as pd

# Load processed datasets
batting = pd.read_csv('data/processed/player_batting_stats.csv')
bowling = pd.read_csv('data/processed/player_bowling_stats.csv')
deliveries = pd.read_csv('data/processed/all_deliveries.csv')

# Example: Top 10 run scorers
print(batting.nlargest(10, 'runs')[['player', 'runs', 'strike_rate']])
```

---

## 💻 Technologies

### Current Stack (Phase 1)
- **Python 3.10** - Core language
- **pandas & NumPy** - Data manipulation
- **Matplotlib & Seaborn** - Visualization
- **Jupyter** - Interactive analysis
- **PyYAML** - Data parsing

### Planned Additions
- **Scikit-learn & XGBoost** - Machine learning (Phase 2)
- **Tableau/Streamlit** - Interactive dashboards (Phase 3)
- **OpenCV & MediaPipe** - Computer vision (Phase 4)
- **NLTK/spaCy** - NLP and sentiment analysis (Phase 5)

---

## 📈 Project Roadmap

### ✅ Q4 2025 - Phase 1 (COMPLETE)
- [x] Data acquisition and processing pipeline
- [x] Exploratory data analysis
- [x] Batting performance analysis
- [x] Bowling effectiveness analysis
- [x] Match insights and trends
- [x] Comprehensive documentation

### 🔄 Q1 2026 - Phase 2 (IN PROGRESS)
- [ ] Feature engineering for ML
- [ ] Model development and training
- [ ] Prediction API development
- [ ] Model evaluation and tuning

### 📅 Q2 2026 - Phase 3 (PLANNED)
- [ ] Dashboard design and wireframes
- [ ] Interactive tool development
- [ ] User testing and refinement
- [ ] Deployment and sharing

### 📅 Q3 2026 - Phase 4 & 5 (PLANNED)
- [ ] Video data collection
- [ ] Computer vision pipeline
- [ ] Social media data acquisition
- [ ] Sentiment analysis models

---

## 📊 Data Coverage

### Current (Phase 1)
- **Tournaments**: 5 editions (2014, 2016, 2021, 2022, 2024)
- **Matches**: 181 complete matches
- **Deliveries**: 40,966 ball-by-ball records
- **Players**: 525 batsmen, 372 bowlers
- **Source**: [Cricsheet](https://cricsheet.org/)

### Planned Expansion
- IPL data (2008-2026)
- BBL, CPL, PSL tournaments
- International T20 bilaterals
- Women's T20 World Cup

---

## 🎓 Skills Demonstrated

This portfolio showcases:
- ✅ **Data Engineering** - ETL pipelines, data processing
- ✅ **Statistical Analysis** - Performance metrics, rankings
- ✅ **Data Visualization** - Professional charts and insights
- ✅ **Python Programming** - Clean, modular code
- ✅ **Documentation** - Professional project docs
- 🔄 **Machine Learning** - Predictive modeling (in progress)
- 📅 **Computer Vision** - Motion tracking (planned)
- 📅 **Dashboard Development** - Interactive tools (planned)

---

## 🤝 Contributing

While this is a personal portfolio project, feedback and suggestions are welcome!
- Open an issue for feature ideas
- Share insights or analysis approaches
- Fork for your own sports analytics

---

## 📝 License

Educational and analytical purposes. Data sourced from Cricsheet under open data terms.

---

## 👨‍💻 Author

**Aalap Desai**
- Email: adesai@altsportsdata.com
- Portfolio: [Link to portfolio]
- LinkedIn: [Link to LinkedIn]

---

## 🙏 Acknowledgments

- **[Cricsheet](https://cricsheet.org/)** - Comprehensive cricket data
- **ICC** - T20 World Cup tournaments
- Cricket analytics community for inspiration

---

## ⭐ Project Status

| Phase | Status | Completion |
|-------|--------|------------|
| **Phase 1: T20 Analytics** | ✅ Complete | 100% |
| **Phase 2: Match Prediction** | 🔄 In Progress | 20% |
| **Phase 3: Scouting Dashboard** | 📅 Planned | 0% |
| **Phase 4: Player Tracking** | 📅 Planned | 0% |
| **Phase 5: Sentiment Analysis** | 📅 Planned | 0% |

**Overall Portfolio Progress: 20%**

---

**Last Updated**: January 2026

*A living portfolio - continuously evolving with new cricket analytics projects*
