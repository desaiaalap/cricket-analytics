# 📊 Data Sources Guide

## Primary Data Source: Cricsheet.org

**Website:** https://cricsheet.org

Cricsheet provides free ball-by-ball cricket data for all formats and competitions.

---

## ✅ Automatic Download (Recommended)

The project automatically downloads data from Cricsheet when you run:

```bash
docker-compose up --build
```

Or manually:

```bash
python scripts/init_pipeline.py
```

---

## 🔄 Updated URLs (2026)

**Important:** Cricsheet migrated from YAML to JSON format.

### Current URLs (JSON Format)
- **T20 Internationals (Men):** `https://cricsheet.org/downloads/t20s_male_json.zip`
- **T20 Internationals (Women):** `https://cricsheet.org/downloads/t20s_female_json.zip`
- **IPL:** `https://cricsheet.org/downloads/ipl_male_json.zip`
- **Big Bash League:** `https://cricsheet.org/downloads/bbl_male_json.zip`
- **ODI (Men):** `https://cricsheet.org/downloads/odis_male_json.zip`
- **Test Cricket (Men):** `https://cricsheet.org/downloads/tests_male_json.zip`

### Legacy URLs (YAML Format - May be deprecated)
- **T20 Internationals (Men):** `https://cricsheet.org/downloads/t20s_male_yaml.zip`
- **T20 Internationals (Women):** `https://cricsheet.org/downloads/t20s_female_yaml.zip`

---

## 🐛 Troubleshooting Downloads

### Problem 1: 404 Not Found

**Symptoms:**
```
❌ Download failed: 404 Client Error: Not Found for url: https://cricsheet.org/downloads/t20s_male_yaml.zip
```

**Solution:**
The downloader has been updated to use JSON format URLs. Update your code:

```bash
# Pull latest changes
git pull origin main

# Or manually update cricsheet_downloader.py
```

**Automatic Fallback:**
The downloader now automatically tries YAML format if JSON fails.

---

### Problem 2: Network/Firewall Issues

**Symptoms:**
```
❌ Download failed: 403 Forbidden
```

**Solutions:**

#### Option A: Manual Download
1. Visit https://cricsheet.org/downloads/
2. Download: `t20s_male_json.zip` (or `t20s_male_yaml.zip`)
3. Extract to: `data/external/t20s_male_json/`
4. Run: `python scripts/process_all_matches.py`

#### Option B: Use Sample Data
```bash
# The repository includes sample data for testing
# Check if sample data exists:
ls data/external/sample/

# If present, process it:
python scripts/process_all_matches.py
```

#### Option C: Alternative Cricket Data Sources

1. **ESPNCricinfo Statsguru**
   - Website: https://stats.espncricinfo.com/
   - Format: Manual export to CSV
   - Coverage: Comprehensive historical data

2. **cricketdata R Package**
   - GitHub: https://github.com/robjhyndman/cricketdata
   - Format: R data frames
   - Coverage: International cricket

3. **Kaggle Datasets**
   - Search: "Cricket ball by ball" on Kaggle
   - Format: CSV
   - Coverage: Various competitions

---

## 📥 Manual Data Setup

If automatic download fails, follow these steps:

### Step 1: Download Data Manually

1. Go to: https://cricsheet.org/downloads/
2. Download: `t20s_male_json.zip` (or any tournament)
3. Save to your computer

### Step 2: Extract Data

```bash
# Create directory
mkdir -p data/external/t20s_male_json

# Extract (Linux/Mac)
unzip ~/Downloads/t20s_male_json.zip -d data/external/t20s_male_json/

# Extract (Windows PowerShell)
Expand-Archive -Path "$HOME\Downloads\t20s_male_json.zip" -DestinationPath "data\external\t20s_male_json"
```

### Step 3: Process Data

```bash
python scripts/process_all_matches.py
```

### Step 4: Launch Dashboard

```bash
streamlit run dashboard/home.py
```

---

## 🔍 Verifying Data

After download/extraction, verify you have data:

```bash
# Check for JSON files
ls data/external/t20s_male_json/*.json | head -5

# Or YAML files
ls data/external/t20s_male_yaml/*.yaml | head -5

# Should see match files like:
# 123456.json
# 123457.json
# etc.
```

Expected structure:
```
data/
├── external/
│   └── t20s_male_json/   (or t20s_male_yaml)
│       ├── 1234567.json
│       ├── 1234568.json
│       └── ... (100+ match files)
└── processed/            (created after processing)
    ├── all_deliveries.csv
    ├── match_summaries.csv
    ├── player_batting_stats.csv
    └── player_bowling_stats.csv
```

---

## 📊 Data Formats

### JSON Format (Current)
```json
{
  "info": {
    "teams": ["Team A", "Team B"],
    "dates": ["2024-01-15"],
    "venue": "Stadium Name"
  },
  "innings": [
    {
      "team": "Team A",
      "overs": [...]
    }
  ]
}
```

### YAML Format (Legacy)
```yaml
info:
  teams:
    - Team A
    - Team B
  dates:
    - 2024-01-15
  venue: Stadium Name
innings:
  - team: Team A
    overs: [...]
```

**Note:** Our code supports both formats automatically.

---

## 🆘 Still Having Issues?

### Check These:

1. **Internet Connection**
   ```bash
   ping cricsheet.org
   ```

2. **Cricsheet Status**
   - Visit: https://cricsheet.org
   - Check if website is accessible

3. **Python Dependencies**
   ```bash
   pip install requests pyyaml pandas
   ```

4. **File Permissions**
   ```bash
   # Linux/Mac
   chmod -R 755 data/

   # Check write permissions
   touch data/external/test.txt && rm data/external/test.txt
   ```

### Error Messages Explained

| Error | Meaning | Solution |
|-------|---------|----------|
| 404 Not Found | URL changed/file moved | Update downloader code |
| 403 Forbidden | Access denied/firewall | Try VPN or manual download |
| Connection timeout | Network issue | Check internet, try again |
| Bad ZIP file | Corrupted download | Delete and re-download |
| Permission denied | File access issue | Check folder permissions |

---

## 🚀 Quick Start (Skip Download)

If you just want to explore the platform without downloading data:

### Option 1: Use Existing Processed Data
```bash
# If data/processed/ already has CSV files
streamlit run dashboard/home.py
```

### Option 2: Generate Sample Data
```bash
# Create minimal sample data for testing
python scripts/create_sample_data.py  # (if available)
```

---

## 📚 Resources

- **Cricsheet Documentation:** https://cricsheet.org/format/json/
- **Data Dictionary:** https://cricsheet.org/format/
- **GitHub Issues:** Report download problems to Cricsheet
- **Project Issues:** Report issues to this repository

---

## ✅ Data Update Frequency

- **Cricsheet Updates:** After each match/series completion
- **Recommended:** Re-download weekly/monthly for latest matches
- **Command:** `rm -rf data/external/ && docker-compose up --build`

---

**Last Updated:** January 2026
**Data Format:** JSON (primary), YAML (legacy support)
**Status:** Automated download with fallback mechanisms

---

**Sources:**
- [Cricsheet Downloads](https://cricsheet.org/downloads/)
- [cricketdata R Package](https://cran.r-project.org/web/packages/cricketdata/vignettes/cricketdata_R_pkg.html)
