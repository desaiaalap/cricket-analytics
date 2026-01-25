# 🚀 Quick Start - Cricket Analytics

**Get started in 3 simple steps (< 5 minutes)**

---

## Step 1: Install (1 minute)

```bash
# Clone the repository
git clone https://github.com/yourusername/cricket-analytics.git
cd cricket-analytics

# Install dependencies
pip install -r requirements.txt
```

**That's it!** No complex setup needed.

---

## Step 2: Download Data (2 minutes)

```bash
# Download T20 World Cup data automatically
python -c "
from scripts.cricsheet_downloader import download_cricsheet_data
download_cricsheet_data('t20_internationals_male', 'data/external')
"
```

Or use Python interactively:

```python
from scripts.cricsheet_downloader import download_cricsheet_data

# Download T20 World Cup data
data_path = download_cricsheet_data('t20_internationals_male', 'data/external')
print(f"✅ Downloaded to: {data_path}")
```

---

## Step 3: Process & Analyze (1 minute)

```bash
# Process all matches
python scripts/process_all_matches.py

# Open analysis notebooks
jupyter notebook
```

Then open any notebook:
- `notebooks/02_batting_analysis.ipynb` - Batting insights
- `notebooks/03_bowling_analysis.ipynb` - Bowling insights
- `notebooks/04_match_insights.ipynb` - Match dynamics

---

## 🎯 What You Get

After these 3 steps, you'll have:

✅ **40,966+ ball-by-ball records** processed
✅ **525 batsmen** with complete statistics
✅ **372 bowlers** with performance metrics
✅ **4 clean datasets** ready for analysis
✅ **3 interactive notebooks** with visualizations

---

## 📊 Quick Example

Want to see top scorers immediately?

```python
import pandas as pd

# Load batting stats
batting = pd.read_csv('data/processed/player_batting_stats.csv')

# Top 10 run scorers
top_scorers = batting.nlargest(10, 'runs')[['player', 'runs', 'average', 'strike_rate']]
print(top_scorers)
```

Output:
```
                   player  runs  average  strike_rate
0            Virat Kohli  1083     57.0        130.8
1            Jos Buttler   949     45.2        151.8
2          Rohit Sharma   753     27.9        131.6
...
```

---

## 🛠️ Alternative: Use Makefile (Even Easier!)

If you have `make` installed:

```bash
# One command does everything!
make setup          # Install dependencies
make download-sample # Download sample data
make process-data   # Process matches
make notebooks      # Start Jupyter
```

---

## 🔍 Available Data Sources

You can download any of these tournaments:

**T20 Leagues:**
- `ipl` - Indian Premier League
- `bbl` - Big Bash League
- `cpl` - Caribbean Premier League
- `psl` - Pakistan Super League

**International:**
- `t20_internationals_male` - All men's T20Is
- `t20_internationals_female` - All women's T20Is
- `odi_male` / `odi_female` - ODIs
- `test_male` / `test_female` - Tests

Just change the tournament name:
```python
download_cricsheet_data('ipl', 'data/external')  # For IPL
```

---

## ❓ Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "No data found"
Make sure you ran Step 2 (download data) first.

### "Jupyter not found"
```bash
pip install jupyter
```

---

## 🎓 What's Next?

Once you've completed the quick start:

1. **Explore the notebooks** - See the analysis in action
2. **Modify the code** - Try different tournaments
3. **Build your own analysis** - Use the processed datasets
4. **Check the full README** - Learn about advanced features

---

## 📚 Full Documentation

- **[README.md](README.md)** - Complete project overview
- **[TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - Running tests
- **[CRICSHEET_DOWNLOADER_GUIDE.md](docs/CRICSHEET_DOWNLOADER_GUIDE.md)** - Download guide

---

**Need help?** Open an issue on GitHub or contact: adesai@altsportsdata.com

---

**Total time to get started: < 5 minutes** ⏱️
