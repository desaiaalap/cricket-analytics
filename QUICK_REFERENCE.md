# 🏏 Cricket Analytics - Quick Reference Card

## 📥 Download Data

### One-Line Download
```python
from scripts.cricsheet_downloader import download_cricsheet_data
data_path = download_cricsheet_data('ipl', 'data/external')
```

### Using Downloader Class
```python
from scripts.cricsheet_downloader import CricsheetDownloader
downloader = CricsheetDownloader()
downloader.download_tournament('ipl', 'data/external')
```

### List Available Tournaments
```python
downloader = CricsheetDownloader()
tournaments = downloader.list_available_tournaments()
for name in tournaments.keys():
    print(name)
```

---

## ⚙️ Process Data

### Process All Matches
```bash
python scripts/process_all_matches.py
```

### Load and Parse YAML
```python
from scripts.cricpy_loader import load_all_yaml, parse_match
matches = load_all_yaml('data/external/icc_mens_t20_world_cup_male')
```

---

## 📊 Analyze Data

### Quick Data Load
```python
import pandas as pd

# Load processed datasets
batting = pd.read_csv('data/processed/player_batting_stats.csv')
bowling = pd.read_csv('data/processed/player_bowling_stats.csv')
deliveries = pd.read_csv('data/processed/all_deliveries.csv')
matches = pd.read_csv('data/processed/match_summaries.csv')
```

### Top Performers
```python
# Top 10 run scorers
print(batting.nlargest(10, 'runs')[['player', 'runs', 'average', 'strike_rate']])

# Top 10 wicket takers
print(bowling.nlargest(10, 'wickets')[['player', 'wickets', 'economy', 'average']])
```

---

## 📓 Run Analysis Notebooks

### Launch Jupyter
```bash
jupyter notebook
```

### Notebooks (in order)
1. `notebooks/02_batting_analysis.ipynb` - Batting analytics
2. `notebooks/03_bowling_analysis.ipynb` - Bowling analytics
3. `notebooks/04_match_insights.ipynb` - Match insights

---

## 🔄 Complete Workflow

### End-to-End Pipeline
```python
# 1. Download
from scripts.cricsheet_downloader import download_cricsheet_data
data_path = download_cricsheet_data('ipl', 'data/external')

# 2. Process
from scripts.cricpy_loader import load_all_yaml, parse_match
import pandas as pd

matches = load_all_yaml(str(data_path))
deliveries = [parse_match(m[1]) for m in matches]
all_deliveries = pd.concat(deliveries, ignore_index=True)

# 3. Save
all_deliveries.to_csv('data/processed/ipl_deliveries.csv', index=False)

# 4. Analyze
print(f"Total runs: {all_deliveries['runs_total'].sum():,}")
print(f"Total wickets: {all_deliveries['dismissal'].notna().sum():,}")
```

---

## 🗂️ Available Tournaments

### T20 Leagues
- `ipl` - Indian Premier League
- `bbl` - Big Bash League
- `cpl` - Caribbean Premier League
- `psl` - Pakistan Super League
- `blast` - T20 Blast
- `hundred` - The Hundred
- `super_smash` - Super Smash

### Internationals
- `t20_internationals_male` - All men's T20Is
- `t20_internationals_female` - All women's T20Is
- `icc_mens_t20_world_cup` - T20 World Cup (men)
- `icc_womens_t20_world_cup` - T20 World Cup (women)
- `odi_male` / `odi_female` - ODIs
- `test_male` / `test_female` - Tests

---

## 🚀 Git Commands

### Initialize & Commit
```bash
git init
git add .
git commit -m "Initial commit"
```

### Push to GitHub
```bash
git remote add origin <your-repo-url>
git push -u origin main
```

**Note:** Large data files are automatically excluded by `.gitignore`

---

## 📁 Key File Locations

### Data
- `data/external/` - Raw YAML files (downloaded)
- `data/processed/` - Processed CSV files

### Scripts
- `scripts/cricsheet_downloader.py` - Data downloader
- `scripts/cricpy_loader.py` - Data loader
- `scripts/process_all_matches.py` - Batch processor

### Notebooks
- `notebooks/02_batting_analysis.ipynb` - Batting
- `notebooks/03_bowling_analysis.ipynb` - Bowling
- `notebooks/04_match_insights.ipynb` - Matches

### Documentation
- `README.md` - Main documentation
- `docs/CRICSHEET_DOWNLOADER_GUIDE.md` - Download guide
- `docs/DATA_PROCESSING_SUMMARY.md` - Processing results

---

## 🛠️ Troubleshooting

### Download fails
```python
# Check tournament name
downloader = CricsheetDownloader()
print(downloader.list_available_tournaments())
```

### Processing errors
```bash
# Check data directory exists
ls data/external/

# Re-run processing
python scripts/process_all_matches.py
```

### Import errors
```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn pyyaml jupyter requests
```

---

## 📚 Documentation Links

- **[Main README](README.md)** - Project overview
- **[Downloader Guide](docs/CRICSHEET_DOWNLOADER_GUIDE.md)** - Download documentation
- **[Processing Summary](docs/DATA_PROCESSING_SUMMARY.md)** - Processing results
- **[New Features](NEW_FEATURES_SUMMARY.md)** - Latest additions

---

**Last Updated**: January 2026
