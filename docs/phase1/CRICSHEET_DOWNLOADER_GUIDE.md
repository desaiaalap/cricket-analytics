# 📥 Cricsheet Data Downloader Guide

## Overview

The Cricsheet Downloader automates downloading cricket data from [Cricsheet.org](https://cricsheet.org/) instead of manual downloading. This feature was added to streamline the data acquisition process.

---

## 🚀 Quick Start

### Simple Download (One Line)

```python
from scripts.cricsheet_downloader import download_cricsheet_data

# Download IPL data
data_path = download_cricsheet_data('ipl', 'data/external')
print(f"Data saved to: {data_path}")
```

### Using the Downloader Class

```python
from scripts.cricsheet_downloader import CricsheetDownloader

downloader = CricsheetDownloader()

# Download and extract
downloader.download_tournament(
    tournament='ipl',
    output_dir='data/external',
    extract=True,
    cleanup_zip=True
)
```

---

## 📋 Available Tournaments

The downloader supports the following tournaments:

### T20 Internationals
- `t20_internationals_male` - All men's T20 internationals
- `t20_internationals_female` - All women's T20 internationals
- `icc_mens_t20_world_cup` - Men's T20 World Cup
- `icc_womens_t20_world_cup` - Women's T20 World Cup

### T20 Leagues
- `ipl` - Indian Premier League
- `bbl` - Big Bash League (Australia)
- `cpl` - Caribbean Premier League
- `psl` - Pakistan Super League
- `blast` - T20 Blast (England)
- `hundred` - The Hundred (England)
- `super_smash` - Super Smash (New Zealand)

### Other Formats
- `odi_male` - Men's ODIs
- `odi_female` - Women's ODIs
- `test_male` - Men's Tests
- `test_female` - Women's Tests
- `all_matches` - All matches (large file)

---

## 💻 Usage Examples

### Example 1: List Available Tournaments

```python
from scripts.cricsheet_downloader import CricsheetDownloader

downloader = CricsheetDownloader()

# List all available tournaments
tournaments = downloader.list_available_tournaments()

for name, filename in tournaments.items():
    print(f"{name:30s} -> {filename}")
```

### Example 2: Download Single Tournament

```python
from scripts.cricsheet_downloader import CricsheetDownloader

downloader = CricsheetDownloader()

# Download T20 World Cup data
data_path = downloader.download_tournament(
    tournament='icc_mens_t20_world_cup',
    output_dir='data/external',
    extract=True,        # Extract ZIP file
    cleanup_zip=True     # Remove ZIP after extraction
)

print(f"✅ Data downloaded to: {data_path}")
```

### Example 3: Download Multiple Tournaments

```python
from scripts.cricsheet_downloader import CricsheetDownloader

downloader = CricsheetDownloader()

# Download multiple T20 leagues
tournaments = ['ipl', 'bbl', 'cpl', 'psl']

results = downloader.download_multiple_tournaments(
    tournaments=tournaments,
    output_dir='data/external'
)

# Check results
for tournament, path in results.items():
    if path:
        print(f"✅ {tournament}: {path}")
    else:
        print(f"❌ {tournament}: Failed")
```

### Example 4: Get Tournament Information

```python
from scripts.cricsheet_downloader import CricsheetDownloader

downloader = CricsheetDownloader()

# Get info about a tournament
info = downloader.get_tournament_info('ipl')

print(f"Name: {info['name']}")
print(f"URL: {info['url']}")
print(f"Format: {info['format']}")
```

---

## 🔧 Function Reference

### `CricsheetDownloader` Class

#### `__init__(base_url=None)`
Initialize the downloader.

**Parameters:**
- `base_url` (str, optional): Custom base URL (default: Cricsheet downloads)

#### `list_available_tournaments()`
Get all available tournaments.

**Returns:** Dictionary mapping tournament names to filenames

#### `download_tournament(tournament, output_dir='data/external', extract=True, cleanup_zip=True)`
Download tournament data.

**Parameters:**
- `tournament` (str): Tournament identifier
- `output_dir` (str): Directory to save data
- `extract` (bool): Whether to extract ZIP
- `cleanup_zip` (bool): Whether to delete ZIP after extraction

**Returns:** Path to downloaded/extracted data

#### `download_multiple_tournaments(tournaments, output_dir='data/external', **kwargs)`
Download multiple tournaments.

**Parameters:**
- `tournaments` (list): List of tournament identifiers
- `output_dir` (str): Directory to save data
- `**kwargs`: Additional arguments for download_tournament()

**Returns:** Dictionary mapping tournament names to paths

#### `get_tournament_info(tournament)`
Get information about a tournament.

**Parameters:**
- `tournament` (str): Tournament identifier

**Returns:** Dictionary with tournament metadata

### Convenience Functions

#### `download_cricsheet_data(tournament, output_dir='data/external')`
Simple one-line download function.

**Parameters:**
- `tournament` (str): Tournament identifier
- `output_dir` (str): Directory to save data

**Returns:** Path to extracted data

---

## 🎯 Integration with Existing Workflow

### Complete Workflow: Download → Process → Analyze

```python
# Step 1: Download data
from scripts.cricsheet_downloader import download_cricsheet_data

data_path = download_cricsheet_data('ipl', 'data/external')
print(f"✅ Downloaded to: {data_path}")

# Step 2: Process data
from scripts.cricpy_loader import load_all_yaml, parse_match
import pandas as pd

matches = load_all_yaml(str(data_path))
all_deliveries = []

for filename, match_data in matches:
    df = parse_match(match_data)
    all_deliveries.append(df)

deliveries_df = pd.concat(all_deliveries, ignore_index=True)
print(f"✅ Processed {len(deliveries_df):,} deliveries")

# Step 3: Analyze
print(f"Total runs: {deliveries_df['runs_total'].sum()}")
print(f"Total wickets: {deliveries_df['dismissal'].notna().sum()}")
```

---

## 📊 Data Format

Downloaded data is in **YAML format** with the following structure:

```yaml
meta:
  data_version: 1.0.0
  created: 2024-01-01
  revision: 1
info:
  venue: "Melbourne Cricket Ground"
  city: Melbourne
  dates: [2024-01-15]
  gender: male
  match_type: T20
  teams: [Australia, India]
  outcome:
    winner: Australia
    by:
      runs: 25
innings:
  - team: Australia
    deliveries:
      - 0.1:
          batsman: Player A
          bowler: Player B
          runs:
            batsman: 4
            total: 4
```

---

## ⚠️ Important Notes

### File Sizes
- **Small tournaments** (~10-50 MB): BBL, PSL, CPL
- **Medium tournaments** (~50-200 MB): IPL, T20 Internationals
- **Large tournaments** (>500 MB): All matches, ODIs, Tests

### Network Requirements
- Stable internet connection required
- Downloads may take 1-10 minutes depending on file size
- Progress is shown during download

### Storage Requirements
- Ensure sufficient disk space
- Extracted files are larger than ZIP files
- Use `cleanup_zip=True` to save space

### .gitignore Integration
The `.gitignore` file is configured to exclude downloaded data:
```
data/external/**/*.yaml
data/processed/*.csv
*.zip
```

---

## 🛠️ Troubleshooting

### Error: "Tournament not found"
**Cause:** Invalid tournament identifier

**Solution:** Use `list_available_tournaments()` to see valid names

### Error: Network/Connection Issues
**Cause:** Network timeout or Cricsheet.org unavailable

**Solution:**
- Check internet connection
- Try again later
- Use manual download from cricsheet.org

### Error: ZIP Extraction Failed
**Cause:** Corrupted or incomplete download

**Solution:**
- Delete the ZIP file
- Download again
- Check available disk space

---

## 🔄 Updating Data

To get the latest data, simply re-download:

```python
from scripts.cricsheet_downloader import download_cricsheet_data

# Re-download to get latest matches
data_path = download_cricsheet_data('ipl', 'data/external')
```

Cricsheet data is updated regularly with new matches.

---

## 📝 Example: Automated IPL Analysis Pipeline

```python
#!/usr/bin/env python
"""Automated IPL data download and analysis"""

from scripts.cricsheet_downloader import CricsheetDownloader
from scripts.cricpy_loader import load_all_yaml, parse_match
from scripts.process_all_matches import process_data
import pandas as pd

def main():
    # 1. Download latest IPL data
    print("📥 Downloading IPL data...")
    downloader = CricsheetDownloader()
    data_path = downloader.download_tournament('ipl', 'data/external')

    # 2. Process data
    print("⚙️  Processing matches...")
    matches = load_all_yaml(str(data_path))
    deliveries = []

    for filename, match_data in matches:
        df = parse_match(match_data)
        deliveries.append(df)

    all_deliveries = pd.concat(deliveries, ignore_index=True)

    # 3. Save processed data
    all_deliveries.to_csv('data/processed/ipl_deliveries.csv', index=False)
    print(f"✅ Saved {len(all_deliveries):,} deliveries")

    # 4. Quick analysis
    print("\n📊 Quick Stats:")
    print(f"  Total runs: {all_deliveries['runs_total'].sum():,}")
    print(f"  Total wickets: {all_deliveries['dismissal'].notna().sum():,}")
    print(f"  Total matches: {len(matches)}")

if __name__ == '__main__':
    main()
```

---

## 🙏 Credits

Data provided by [Cricsheet.org](https://cricsheet.org/) - An amazing resource for cricket analytics.

---

**Last Updated**: January 2026
