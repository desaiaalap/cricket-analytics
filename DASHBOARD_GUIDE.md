# 📊 Dashboard Guide - Complete Interactive Analytics Platform

## Overview

The Cricket Analytics platform now includes **5 specialized dashboards**, each designed for different analytical needs—from storytelling to deep player analysis.

---

## 🏠 Quick Start

### Option 1: Just the Home Dashboard (Recommended for First-Time Users)

```bash
docker-compose up --build home
```

**Opens:** http://localhost:8501

The home dashboard provides:
- Quick statistics overview
- Top performers
- Links to all specialized dashboards with descriptions

### Option 2: All Dashboards Simultaneously

```bash
docker-compose --profile full up --build
```

**Opens:**
- 🏠 Home: http://localhost:8501
- 📖 Storytelling: http://localhost:8502
- 🎮 Player Explorer: http://localhost:8503
- 🎬 Match Viewer: http://localhost:8504
- 📊 Classic: http://localhost:8505

---

## 📚 Dashboard Descriptions

### 1. 🏠 Home Dashboard (`home.py`)

**Purpose:** Main landing page and gateway to all analytics

**Features:**
- At-a-glance tournament statistics
- Top 10 batsmen and bowlers
- Platform features overview
- Links to all specialized dashboards

**When to use:**
- First time exploring the platform
- Quick stats lookup
- Navigating to specific analytics

**Run standalone:**
```bash
streamlit run dashboard/home.py
```

---

### 2. 📖 Storytelling Dashboard (`storytelling_app.py`)

**Purpose:** Data-driven narratives about T20 cricket

**Features:**
- **Chapter 1: By The Numbers** - Statistical landscape of T20
- **Chapter 2: The Legends** - Top performers deep dive
- **Chapter 3: The Battle** - Bat vs Ball analysis with phase breakdowns
- **Chapter 4: Partnerships** - Biggest stands and collaborations
- **Chapter 5: What Wins?** - Toss analysis and match-winning factors

**Visualization Style:**
- Magazine-style layout with serif fonts
- Gradient insight cards
- Narrative-focused text
- Story-driven chart presentations

**When to use:**
- Presenting findings to non-technical audiences
- Understanding the "story" behind the data
- Getting inspired by cricket history

**Run standalone:**
```bash
streamlit run dashboard/storytelling_app.py
```

---

### 3. 🎮 Player Explorer (`player_explorer.py`)

**Purpose:** Deep dive into individual player performance

**Features:**

**Batsman Analysis:**
- Comprehensive stats card (runs, average, SR, boundaries)
- Scoring pattern breakdown (fours vs sixes vs singles)
- Per-match averages and efficiency metrics
- Match-by-match form with dual-axis charts
- Detailed performance table

**Bowler Analysis:**
- Key metrics (wickets, economy, average, strike rate)
- Economy gauge visualization
- Performance metrics breakdown
- Match-by-match bowling stats

**Player Comparison:**
- Interactive radar charts
- Head-to-head stat comparisons
- Side-by-side metric displays
- Support for batsmen and bowlers

**When to use:**
- Scouting individual players
- Comparing two players head-to-head
- Analyzing player form trends
- Deep statistical analysis

**Run standalone:**
```bash
streamlit run dashboard/player_explorer.py
```

---

### 4. 🎬 Match Viewer (`match_viewer.py`)

**Purpose:** Replay and analyze individual matches

**Features:**

**Momentum Chart:**
- Runs progression for both innings
- Wickets fallen timeline
- Dual-axis visualization
- Hover-enabled ball-by-ball details

**Manhattan Chart:**
- Runs scored per over
- Side-by-side innings comparison
- Identify explosive overs

**Worm Chart:**
- Run rate progression
- Comparative performance tracking
- Chasing pressure visualization

**Phase Comparison:**
- Powerplay vs Middle vs Death
- Runs and run rate by phase
- Strategic insights

**Key Moments:**
- Biggest hits (sixes breakdown)
- Crucial wickets
- Highest scoring overs

**When to use:**
- Replaying specific matches
- Understanding match momentum shifts
- Analyzing chase strategies
- Identifying key turning points

**Run standalone:**
```bash
streamlit run dashboard/match_viewer.py
```

---

### 5. 📊 Classic Dashboard (`app.py`)

**Purpose:** Traditional analytics dashboard with comprehensive stats

**Features:**
- Tournament overview with key metrics
- Batting analysis (top scorers, SR vs Average)
- Bowling analysis (wicket takers, economy)
- Match insights (toss impact, team performance)
- Player comparison tool

**When to use:**
- General analytics needs
- Multi-page analysis workflow
- Traditional dashboard experience

**Run standalone:**
```bash
streamlit run dashboard/app.py
```

---

## 🐳 Docker Usage

### Basic (Home Dashboard Only)

```bash
docker-compose up --build
```

**Result:**
- ✅ Runs E2E pipeline (download → process → validate)
- ✅ Launches home dashboard on http://localhost:8501

### Full Platform (All Dashboards)

```bash
docker-compose --profile full up --build
```

**Result:**
- ✅ Runs E2E pipeline once
- ✅ Launches all 5 dashboards on separate ports
- ✅ Data shared across all dashboards

**Access:**
- Home: http://localhost:8501
- Storytelling: http://localhost:8502
- Player Explorer: http://localhost:8503
- Match Viewer: http://localhost:8504
- Classic: http://localhost:8505

### Development Mode (With Jupyter)

```bash
docker-compose --profile full --profile dev up --build
```

**Result:**
- All dashboards + Jupyter notebooks
- Jupyter: http://localhost:8888

---

## 🚀 Local Development (No Docker)

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run E2E Pipeline

```bash
python scripts/init_pipeline.py
```

### Launch Individual Dashboards

```bash
# Home
streamlit run dashboard/home.py

# Storytelling
streamlit run dashboard/storytelling_app.py

# Player Explorer
streamlit run dashboard/player_explorer.py

# Match Viewer
streamlit run dashboard/match_viewer.py

# Classic
streamlit run dashboard/app.py
```

---

## 📊 Dashboard Comparison Matrix

| Feature | Home | Storytelling | Player Explorer | Match Viewer | Classic |
|---------|------|--------------|----------------|--------------|---------|
| **Purpose** | Gateway | Narrative | Player Stats | Match Analysis | General |
| **Best For** | Overview | Presentations | Scouting | Match Replay | All-round |
| **Interactivity** | Low | Medium | High | High | Medium |
| **Visual Style** | Modern | Magazine | Technical | Sports | Traditional |
| **Data Depth** | Summary | Medium | Deep | Deep | Medium |
| **Target Audience** | Everyone | Non-tech | Analysts | Fans | Analysts |

---

## 🎨 Design Philosophy

### Home Dashboard
- **Style:** Modern, card-based layout
- **Colors:** Blue gradients, clean whites
- **Focus:** Navigation and discovery

### Storytelling Dashboard
- **Style:** Magazine/editorial
- **Colors:** Purple gradients, serif fonts
- **Focus:** Narrative flow and insights
- **Typography:** Merriweather (serif) + Inter (sans)

### Player Explorer
- **Style:** Technical, data-rich
- **Colors:** Viridis gradient, professional blues
- **Focus:** Detailed analysis and comparison

### Match Viewer
- **Style:** Sports broadcast aesthetic
- **Colors:** Team colors (blue/red)
- **Focus:** Timeline and momentum

### Classic Dashboard
- **Style:** Traditional analytics
- **Colors:** Plotly default palette
- **Focus:** Comprehensive stats

---

## 🔧 Advanced Features

### Shared Analytics Engine

All dashboards use the same `AdvancedAnalytics` module:

```python
from advanced_analytics import AdvancedAnalytics

analytics = AdvancedAnalytics(deliveries, matches, batting, bowling)

# Features available:
partnerships = analytics.analyze_partnerships(min_runs=50)
phase_stats = analytics.analyze_match_phases()
player_form = analytics.analyze_player_form("Player Name")
momentum = analytics.get_match_momentum("match_id")
insights = analytics.get_key_insights()
```

### Caching Strategy

All dashboards use Streamlit caching:

```python
@st.cache_data  # Cache data loading
def load_data():
    # Loads CSV files

@st.cache_resource  # Cache analytics instance
def get_analytics(_deliveries, _matches, _batting, _bowling):
    # Creates analytics object
```

**Benefits:**
- Fast page loads
- Reduced memory usage
- Smooth user experience

---

## 📱 Responsive Design

All dashboards are responsive and work on:
- ✅ Desktop (optimized)
- ✅ Tablet (good)
- ✅ Mobile (basic support)

**Recommended:** Desktop or tablet for best experience

---

## 🎯 Use Cases

### For Data Analysts

**Recommended:** Player Explorer + Match Viewer + Classic
- Deep dive into stats
- Compare players quantitatively
- Analyze match-by-match trends

### For Presenters/Storytellers

**Recommended:** Storytelling Dashboard
- Narrative-driven insights
- Beautiful visualizations
- Easy to explain to non-technical audiences

### For Cricket Fans

**Recommended:** Match Viewer + Home
- Replay favorite matches
- See top performers
- Understand match momentum

### For Team Scouts

**Recommended:** Player Explorer + Classic
- Analyze player form
- Compare candidates
- Track consistency metrics

---

## 🐛 Troubleshooting

### Dashboard Won't Load

**Check:**
1. Data exists: `ls data/processed/`
2. Port availability: `lsof -i :8501`
3. Run init pipeline: `python scripts/init_pipeline.py`

### "No data found" Error

**Solution:**
```bash
# Run E2E pipeline
docker-compose up --build home

# Or manually
python scripts/init_pipeline.py
```

### Multiple Dashboards Port Conflicts

**Solution:**
```bash
# Kill existing processes
pkill -f streamlit

# Or use different ports
streamlit run dashboard/home.py --server.port=8501
streamlit run dashboard/storytelling_app.py --server.port=8502
```

### Slow Performance

**Solutions:**
1. Clear Streamlit cache: Press 'C' in dashboard
2. Reduce data size (filter specific tournaments)
3. Increase Docker memory limit

---

## 📈 Performance

### Load Times

| Dashboard | Initial Load | Subsequent |
|-----------|--------------|------------|
| Home | ~2s | ~0.5s |
| Storytelling | ~3s | ~1s |
| Player Explorer | ~2s | ~0.5s |
| Match Viewer | ~2.5s | ~0.8s |
| Classic | ~2s | ~0.5s |

**Note:** First load includes data loading; subsequent loads use cache

### Resource Usage

| Dashboard | Memory | CPU |
|-----------|--------|-----|
| Home | ~150MB | Low |
| Storytelling | ~200MB | Low |
| Player Explorer | ~180MB | Medium |
| Match Viewer | ~200MB | Medium |
| Classic | ~170MB | Low |

**Total (all dashboards):** ~900MB RAM

---

## 🚢 Deployment

All dashboards are cloud-ready and can be deployed to:

- **Streamlit Cloud:** Free, easiest (recommended for beginners)
- **Heroku:** Good for production
- **Google Cloud Run:** Scalable, pay-per-use
- **AWS/Azure:** Enterprise options

**Deployment command (example for Heroku):**
```bash
heroku create cricket-analytics
heroku stack:set container
git push heroku main
```

---

## 📚 Related Documentation

- **[E2E_GUIDE.md](E2E_GUIDE.md)** - End-to-end pipeline guide
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker setup and usage
- **[START_HERE.md](START_HERE.md)** - Quick start guide
- **[README.md](README.md)** - Project overview

---

## 🎓 Learning Path

### Beginner Path
1. Start with **Home Dashboard** (overview)
2. Explore **Storytelling Dashboard** (understand narratives)
3. Try **Match Viewer** (replay a match)

### Analyst Path
1. Review **Home Dashboard** (get oriented)
2. Use **Player Explorer** (deep player analysis)
3. Use **Classic Dashboard** (comprehensive stats)
4. Reference **Match Viewer** (specific match details)

### Presenter Path
1. Use **Storytelling Dashboard** (for presentations)
2. Export charts as images
3. Build narrative around chapters

---

## 💡 Tips & Tricks

### Streamlit Shortcuts

- **Press 'R':** Rerun the app
- **Press 'C':** Clear cache
- **Ctrl/Cmd + S:** Save (in edit mode)
- **Sidebar toggle:** Collapse/expand

### Saving Charts

1. Hover over any Plotly chart
2. Click camera icon (top-right of chart)
3. Downloads as PNG

### Customizing Dashboards

All dashboards are in `dashboard/` directory:
- Edit Python files to customize
- Streamlit auto-reloads on save
- Modify CSS in the `st.markdown()` sections

---

**Built with:** 🎨 Streamlit • 📊 Plotly • 🐍 Python • 🐳 Docker

**Interactive. Insightful. Intuitive.**
