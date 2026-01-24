# 🏏 Cricket Analytics - Interactive Data Platform

> **Fully automated end-to-end cricket analytics platform** with interactive storytelling dashboards, advanced analytics, and production-ready deployment.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Data Source](https://img.shields.io/badge/Data-Cricsheet-green.svg)](https://cricsheet.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()
[![Tests](https://img.shields.io/badge/Tests-34%20Passing-brightgreen.svg)]()
[![Dashboards](https://img.shields.io/badge/Dashboards-5%20Interactive-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)]()

---

## ⚡ Super Quick Start

**Never used this before? One command gets you everything:**

```bash
docker-compose up --build
```

**What this does:**
1. ✅ Automatically downloads T20 cricket data from Cricsheet.org
2. ✅ Processes all matches (40,966+ ball-by-ball records)
3. ✅ Launches interactive home dashboard on http://localhost:8501
4. ✅ Ready in ~3-5 minutes (first run) or ~10 seconds (subsequent runs)

**No configuration. No manual steps. Just works!** 🚀

👉 **Having download issues?** See [DATA_SOURCES.md](DATA_SOURCES.md) for troubleshooting

---

## 🎯 What You Get

### 📊 Five Interactive Dashboards

| Dashboard | Purpose | Port |
|-----------|---------|------|
| 🏠 **Home** | Main gateway with quick stats and navigation | 8501 |
| 📖 **Storytelling** | Magazine-style narratives about cricket | 8502 |
| 🎮 **Player Explorer** | Deep dive into player stats and comparisons | 8503 |
| 🎬 **Match Viewer** | Replay matches with momentum charts | 8504 |
| 📊 **Classic** | Traditional comprehensive analytics | 8505 |

**Launch all dashboards:**
```bash
docker-compose --profile full up --build
```

👉 **[Complete Dashboard Guide](DASHBOARD_GUIDE.md)**

### 🔬 Advanced Analytics

- ✅ Partnership analysis (biggest stands, run rates)
- ✅ Match phase analysis (Powerplay, Middle, Death)
- ✅ Player form tracking (match-by-match trends)
- ✅ Match momentum calculation (over-by-over)
- ✅ Head-to-head player comparisons
- ✅ Automated key insights extraction

### 🐳 Production-Ready Deployment

- ✅ Multi-service Docker orchestration
- ✅ Automated E2E pipeline (download → process → visualize)
- ✅ Health checks and auto-restart
- ✅ Cloud deployment ready (Heroku, GCP, AWS, Streamlit Cloud)
- ✅ 34+ automated tests with CI/CD

---

## 📊 Project Statistics

- **181+ T20 World Cup matches** analyzed
- **40,966+ ball-by-ball records** processed
- **525+ unique batsmen** with detailed stats
- **372+ unique bowlers** with performance metrics
- **5 interactive dashboards** for different use cases
- **34+ automated tests** with GitHub Actions CI/CD

---

## 🚀 Usage Options

### Option 1: Docker (Recommended - Zero Setup)

```bash
# Home dashboard only (with auto data download)
docker-compose up --build

# All 5 dashboards simultaneously
docker-compose --profile full up --build

# With Jupyter notebooks for development
docker-compose --profile full --profile dev up --build
```

**Access:**
- Home: http://localhost:8501
- Storytelling: http://localhost:8502
- Player Explorer: http://localhost:8503
- Match Viewer: http://localhost:8504
- Classic: http://localhost:8505
- Jupyter: http://localhost:8888 (dev profile)

### Option 2: Local Python Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run E2E pipeline (downloads data automatically)
python scripts/init_pipeline.py

# 3. Launch any dashboard
streamlit run dashboard/home.py
streamlit run dashboard/storytelling_app.py
streamlit run dashboard/player_explorer.py
streamlit run dashboard/match_viewer.py
```

### Option 3: Jupyter Notebooks

```bash
# Process data first
python scripts/init_pipeline.py

# Launch Jupyter
jupyter notebook

# Open notebooks in order:
# 1. notebooks/01_data_exploration.ipynb
# 2. notebooks/02_batting_analysis.ipynb
# 3. notebooks/03_bowling_analysis.ipynb
# 4. notebooks/04_match_insights.ipynb
```

---

## 📁 Project Structure

```
cricket-analytics/
├── data/
│   ├── external/              # Downloaded JSON/YAML files
│   └── processed/             # Generated CSV datasets
│       ├── all_deliveries.csv
│       ├── match_summaries.csv
│       ├── player_batting_stats.csv
│       └── player_bowling_stats.csv
│
├── scripts/
│   ├── cricpy_loader.py              # Data loading utilities
│   ├── cricsheet_downloader.py       # Automated download (updated 2026)
│   ├── process_all_matches.py        # Batch processing
│   ├── init_pipeline.py              # E2E pipeline orchestrator
│   └── advanced_analytics.py         # Advanced analytics module
│
├── dashboard/
│   ├── home.py                       # Home dashboard
│   ├── storytelling_app.py           # Storytelling dashboard
│   ├── player_explorer.py            # Player analysis
│   ├── match_viewer.py               # Match replay
│   └── app.py                        # Classic dashboard
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_batting_analysis.ipynb
│   ├── 03_bowling_analysis.ipynb
│   └── 04_match_insights.ipynb
│
├── tests/
│   ├── test_cricpy_loader.py
│   ├── test_cricsheet_downloader.py
│   └── test_data_processing.py
│
├── Dockerfile                        # Multi-stage Docker build
├── docker-compose.yml                # Multi-service orchestration
├── requirements.txt                  # Python dependencies
└── pyproject.toml                    # Black/isort configuration
```

---

## 🎨 Dashboard Highlights

### 📖 Storytelling Dashboard

**Magazine-style narrative experience** with:
- 5 chapters telling the story of T20 cricket
- Beautiful gradient cards and serif typography
- Narrative-driven visualizations
- Perfect for presentations and non-technical audiences

**Chapters:**
1. By The Numbers - Statistical landscape
2. The Legends - Top performers spotlight
3. The Battle - Bat vs Ball analysis
4. Partnerships - Biggest stands
5. What Wins? - Match-winning factors

### 🎮 Player Explorer

**Deep player analysis** with:
- Batsman scoring patterns and form trends
- Bowler efficiency metrics and economy analysis
- Interactive radar chart comparisons
- Match-by-match performance tracking

### 🎬 Match Viewer

**Replay any match** with:
- Momentum charts (runs + wickets progression)
- Manhattan charts (runs per over)
- Worm charts (run rate comparison)
- Phase analysis (Powerplay/Middle/Death)
- Key moments highlighting

---

## 🏆 Key Findings

### Top Performers (All Tournaments)

#### 🏏 Leading Run Scorers
| Player | Runs | Average | Strike Rate | Matches |
|--------|------|---------|-------------|---------|
| Virat Kohli | 1,083 | 57.0 | 130.8 | 27 |
| Jos Buttler | 949 | 45.2 | 151.8 | 27 |
| Rohit Sharma | 753 | 27.9 | 131.6 | 28 |

#### ⚾ Leading Wicket Takers
| Player | Wickets | Economy | Average | Matches |
|--------|---------|---------|---------|---------|
| Shakib Al Hasan | 39 | 7.18 | 18.7 | 28 |
| Anrich Nortje | 38 | 5.89 | 11.1 | 18 |
| Wanindu Hasaranga | 35 | 6.17 | 12.1 | 18 |

### Match Insights
- **Toss Impact:** 52% of toss winners win the match
- **Preferred Decision:** Teams field first 62% of the time
- **Average Score:** ~160 runs per innings
- **Most Common Dismissal:** Caught (45% of wickets)

---

## 🛠️ Technologies

**Core Stack:**
- Python 3.10+
- pandas, NumPy (data processing)
- Streamlit (dashboards)
- Plotly (interactive visualizations)
- Docker (containerization)

**Analytics:**
- Custom cricket analytics module
- Partnership tracking algorithms
- Phase-wise analysis
- Momentum calculation

**DevOps:**
- GitHub Actions (CI/CD)
- pytest (testing)
- Black, isort (code quality)
- Multi-stage Docker builds

---

## 📥 Data Sources

**Primary:** [Cricsheet.org](https://cricsheet.org)

### Automatic Download

The project automatically downloads data when you run:
```bash
docker-compose up --build
```

### Updated URLs (2026)

Cricsheet migrated from YAML to JSON format:

- **T20 Internationals (Men):** `t20s_male_json.zip`
- **T20 Internationals (Women):** `t20s_female_json.zip`
- **IPL:** `ipl_male_json.zip`
- **ODI (Men):** `odis_male_json.zip`

**Legacy YAML format still supported as fallback.**

### Troubleshooting Downloads

**If you see download errors (404, 403):**

1. **Check internet connection**
2. **See detailed guide:** [DATA_SOURCES.md](DATA_SOURCES.md)
3. **Manual download option available**
4. **Alternative data sources provided**

👉 **[Complete Data Sources Guide](DATA_SOURCES.md)**

---

## 🧪 Testing & Quality

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=scripts --cov-report=html

# Quick check
pytest tests/ -v --tb=short
```

### Code Quality

```bash
# Format code
python -m black scripts/ tests/ dashboard/ --line-length=100

# Check formatting
python -m black --check scripts/ tests/ dashboard/ --line-length=100
```

### CI/CD

GitHub Actions automatically runs:
- ✅ Tests on Python 3.8, 3.9, 3.10, 3.11
- ✅ Code formatting checks
- ✅ Data processing validation

---

## 🚢 Cloud Deployment

All dashboards are cloud-ready!

### Heroku
```bash
heroku create cricket-analytics
heroku stack:set container
git push heroku main
heroku open
```

### Google Cloud Run
```bash
gcloud run deploy cricket-analytics \
  --source . \
  --platform managed \
  --allow-unauthenticated
```

### Streamlit Cloud
1. Push to GitHub
2. Visit https://share.streamlit.io
3. Connect repository
4. Deploy!

**E2E pipeline runs automatically on first deployment!**

---

## 📚 Documentation

| File | Description |
|------|-------------|
| **[START_HERE.md](START_HERE.md)** | Quick start for beginners |
| **[E2E_GUIDE.md](E2E_GUIDE.md)** | Complete E2E pipeline guide |
| **[DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)** | All 5 dashboards explained |
| **[DATA_SOURCES.md](DATA_SOURCES.md)** | Data download troubleshooting |
| **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** | Docker setup and usage |
| **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** | Comprehensive project summary |

---

## 💡 Use Cases

### For Analysts
- Deep statistical analysis with Player Explorer
- Match-by-match performance tracking
- Head-to-head comparisons
- Export data for custom analysis

### For Presenters
- Use Storytelling Dashboard for compelling narratives
- Beautiful visualizations ready for slides
- Export charts as images
- Data-driven insights

### For Cricket Fans
- Replay matches with Match Viewer
- See top performers
- Understand match momentum
- Explore historical data

### For Developers
- Study the E2E pipeline implementation
- Learn Docker orchestration
- Explore advanced analytics algorithms
- Contribute new features

---

## 🎯 Project Achievements

✅ **Fully Automated E2E Pipeline** - From data download to visualization
✅ **5 Interactive Dashboards** - For different analytical needs
✅ **Advanced Analytics Module** - Partnerships, phases, momentum
✅ **Production-Ready** - Docker, testing, CI/CD, cloud deployment
✅ **Beautiful Visualizations** - Storytelling-focused design
✅ **Comprehensive Documentation** - Guides for every use case
✅ **40,966+ Records Processed** - Complete T20 World Cup history
✅ **Zero Configuration** - Works out of the box

---

## 🔮 Future Enhancements

### Phase 1: More Analytics
- [ ] Batting position analysis
- [ ] Bowler type analysis (pace vs spin)
- [ ] Venue impact analysis
- [ ] Player consistency scoring

### Phase 2: Machine Learning
- [ ] Match outcome prediction
- [ ] Player performance forecasting
- [ ] Team strength ratings
- [ ] Win probability calculator

### Phase 3: Real-time Features
- [ ] Live match tracking
- [ ] Auto-refresh dashboards
- [ ] Real-time notifications
- [ ] API endpoints

---

## 🙏 Acknowledgments

- **[Cricsheet.org](https://cricsheet.org/)** - For comprehensive cricket data
- **ICC** - For organizing T20 World Cup tournaments
- **Streamlit** - For the amazing dashboard framework
- **Plotly** - For interactive visualizations

---

## 📝 License

This project is for educational and analytical purposes. Data sourced from Cricsheet.org under their [terms of use](https://cricsheet.org/about/).

---

## 👨‍💻 Author

**Aalap Desai**
- Email: adesai@altsportsdata.com
- Project: Cricket Analytics Platform
- Status: Production Ready ✅

---

## 📌 Quick Reference

### One-Line Commands

```bash
# Just start everything
docker-compose up --build

# All dashboards
docker-compose --profile full up --build

# Run tests
pytest tests/ -v

# Format code
python -m black scripts/ dashboard/ --line-length=100

# Process data manually
python scripts/init_pipeline.py

# Launch specific dashboard
streamlit run dashboard/storytelling_app.py
```

### Ports Reference

- **8501** - Home Dashboard
- **8502** - Storytelling Dashboard
- **8503** - Player Explorer
- **8504** - Match Viewer
- **8505** - Classic Dashboard
- **8888** - Jupyter Notebooks (dev profile)

---

**Last Updated:** January 2026 | **Status:** ✅ Production Ready | **Version:** 2.0

**From manual downloads to automated storytelling - a complete transformation!** 🎉
