# GitHub Upload Guide

## 🎯 Quick Upload Commands

### First Time Setup (New Repo)

```bash
cd /path/to/cricket-analytics

# Initialize git (if not already done)
git init

# Add all files
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Phase 2: Add ML systems (Team ELO, Player-weighted ELO, Squad Optimizer)

- Team ELO rating system (22 teams)
- Player-weighted ELO system (574 players)
- Squad optimization engine
- Team rankings dashboard
- Player rankings (286 qualified players)
- Dream XI builder
- Documentation guides

Phase 2 Progress: 1/4 complete (Team Strength Ratings with enhancements)"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/cricket-analytics.git

# Push to GitHub
git push -u origin main
```

---

### Updating Existing Repo

```bash
cd /path/to/cricket-analytics

# Check status
git status

# Add new/modified files
git add .

# Commit with message
git commit -m "Add Phase 2 ML systems: ELO ratings and squad optimization"

# Push
git push
```

---

## 📦 What Will Be Uploaded

### ✅ Included (Code & Docs)

```
cricket-analytics/
├── scripts/ml/
│   ├── team_ratings.py                    (~400 lines)
│   ├── player_weighted_elo.py             (~400 lines)
│   ├── squad_optimizer.py                 (~500 lines)
│   ├── next_ball_predictor.py             (~500 lines)
│   └── models/
│       ├── .gitkeep                       (preserves folder)
│       ├── team_rankings.csv              (small, 22 teams)
│       ├── player_rankings.csv            (10KB, 286 players)
│       ├── india_best_xi.csv
│       ├── australia_best_xi.csv
│       └── dream_xi_all_time.csv
│
├── dashboard/
│   ├── team_rankings.py                   (~300 lines)
│   └── (5 existing dashboards)
│
├── data/
│   ├── .gitkeep                           (preserves folder)
│   ├── manual/
│   │   └── india_player_pool_template.csv (30 players)
│   └── processed/.gitkeep
│
├── Documentation/
│   ├── SESSION_SUMMARY.md
│   ├── PHASE_2_ML_PLAN.md
│   ├── PLAYER_WEIGHTED_ELO_EXPLAINED.md
│   ├── SQUAD_OPTIMIZATION_GUIDE.md
│   ├── ENHANCED_PLAYER_DATABASE_GUIDE.md
│   ├── PREDICTION_ACCURACY_ANALYSIS.md
│   └── GITHUB_UPLOAD_GUIDE.md             (this file)
│
├── README.md                               (update with Phase 2)
├── .gitignore                              (created today)
├── requirements.txt                        (update)
└── docker-compose.yml
```

### ❌ Excluded (Large/Generated Files)

```
Excluded by .gitignore:
├── data/processed/*.csv                   (40,966 deliveries - too large)
├── data/external/                         (raw YAML files - 181 matches)
├── scripts/ml/models/*.pkl                (binary model files - regenerate)
├── __pycache__/
├── *.pyc
└── .DS_Store
```

**Why excluded:**
- CSV files are too large (40MB+)
- PKL files are binary (can regenerate by running scripts)
- Users can download data by running `python demo.py`

---

## 📝 Update README.md

Add this section to your README before uploading:

```markdown
## 🤖 Phase 2: Machine Learning (In Progress)

### Completed Features

#### 1. Team ELO Rating System ✅
- **22 teams** rated using ELO algorithm (like chess rankings)
- Processes 176 matches chronologically (2014-2024)
- Accounts for victory margins (close vs dominant wins)
- Dynamic ratings that update after every match

**Top 5 Teams:**
1. 🥇 India - 1791 ELO
2. 🥈 Australia - 1678 ELO
3. 🥉 South Africa - 1675 ELO
4. New Zealand - 1656 ELO
5. England - 1635 ELO

#### 2. Player-Weighted ELO System ✅
- **574 individual players** rated
- Team strength = Average of 11 players' ELO ratings
- Accounts for squad changes, injuries, rotation
- Automatically extracts playing XI from match data

**Top 5 Players (min 5 matches):**
1. Rohit Sharma - 1526 ELO
2. Virat Kohli - 1524 ELO
3. Ravindra Jadeja - 1521 ELO
4. Mitchell Marsh - 1520 ELO
5. Suryakumar Yadav - 1519 ELO

#### 3. Squad Optimization Engine ✅
- Select best possible XI from player pool
- Balance roles (batters/bowlers/all-rounders)
- Compare team compositions
- What-if analysis (swap players)
- Dream XI builder (best 11 across all teams)

**Use Cases:**
- World Cup squad selection
- Predict match outcomes based on lineups
- Analyze impact of injuries/rotation
- Data-driven team selection

### Run ML Systems

```bash
# Generate team ratings
python scripts/ml/team_ratings.py

# Generate player-weighted ratings
python scripts/ml/player_weighted_elo.py

# Run squad optimization
python scripts/ml/squad_optimizer.py

# View rankings dashboard
streamlit run dashboard/team_rankings.py
```

### Upcoming Features
- [ ] Match Outcome Predictor
- [ ] Win Probability Calculator
- [ ] Player Performance Forecasting
```

---

## 🔧 Update requirements.txt

Add these dependencies:

```bash
# Append to requirements.txt
echo "scikit-learn>=1.3.0" >> requirements.txt
echo "pickle-mixin>=1.0.2" >> requirements.txt
```

Or manually add:
```txt
scikit-learn>=1.3.0
pickle-mixin>=1.0.2
```

---

## ✅ Pre-Upload Checklist

Before pushing to GitHub:

- [ ] `.gitignore` created (✅ done)
- [ ] `.gitkeep` files added to preserve folders (✅ done)
- [ ] `README.md` updated with Phase 2 progress
- [ ] `requirements.txt` updated with new dependencies
- [ ] Test Docker build still works: `docker-compose build`
- [ ] Remove any API keys or secrets
- [ ] Check file sizes: `du -sh data/processed/*`
- [ ] Verify imports work: `python scripts/ml/team_ratings.py`

---

## 🚀 Post-Upload Instructions (for others)

Add this to README for users cloning your repo:

```markdown
## 🔄 Setup After Cloning

1. **Download cricket data:**
   ```bash
   python demo.py
   # Or manually download from Cricsheet.org
   ```

2. **Process matches:**
   ```bash
   python scripts/init_pipeline.py
   ```

3. **Generate ML models:**
   ```bash
   python scripts/ml/team_ratings.py
   python scripts/ml/player_weighted_elo.py
   ```

4. **Launch dashboards:**
   ```bash
   streamlit run dashboard/home.py
   ```

Note: Model files (`.pkl`) are not included in the repo.
They will be generated when you run the scripts above.
```

---

## 📊 Estimated Upload Size

**Total upload size:** ~5-10 MB

Breakdown:
- Python scripts: ~3 MB
- Documentation: ~500 KB
- Dashboards: ~2 MB
- CSV files (small ones): ~100 KB
- Config files: ~50 KB

**Excluded files (not uploaded):**
- Large CSVs: ~40 MB (regenerated locally)
- Model PKLs: ~500 KB (regenerated locally)

---

## 🎓 Git Best Practices

### Commit Message Format

```
Type: Brief description (50 chars max)

Detailed explanation of what changed and why.
Can be multiple paragraphs.

- Bullet points for specific changes
- Make it clear and descriptive
```

**Examples:**

```bash
git commit -m "feat: Add player-weighted ELO rating system

- Individual ELO ratings for 574 players
- Team match rating = average of 11 player ELOs
- Accounts for squad changes and player form
- Extract playing XI automatically from ball-by-ball data"
```

```bash
git commit -m "feat: Add squad optimization engine

- Select best XI from available players
- Balance roles (batters/bowlers/all-rounders)
- Compare teams (India vs Australia)
- What-if analysis (Player A vs Player B)
- Dream XI builder across all teams"
```

### Branch Strategy (Optional)

For larger features:

```bash
# Create feature branch
git checkout -b feature/phase2-ml

# Make changes and commit
git add .
git commit -m "Add ML systems"

# Push feature branch
git push -u origin feature/phase2-ml

# Create Pull Request on GitHub
# Merge when ready
```

---

## 🐛 Troubleshooting

### If Git is not initialized:
```bash
git init
git branch -M main
```

### If remote already exists:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/cricket-analytics.git
```

### If file is too large:
```bash
# Check file size
ls -lh filename

# If >50MB, add to .gitignore
echo "filename" >> .gitignore
git rm --cached filename
```

### If commit history needs cleanup:
```bash
# Amend last commit
git commit --amend

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3
```

---

## 📝 Recommended GitHub Repo Settings

**Visibility:** Public (if showcasing) or Private

**Description:**
```
Cricket Analytics Platform with ML-powered predictions: ELO ratings, squad optimization, match forecasting. Built with Python, Streamlit, Docker.
```

**Topics/Tags:**
```
cricket, analytics, machine-learning, elo-rating, data-science,
streamlit, docker, sports-analytics, python, t20-cricket
```

**README badges:**
```markdown
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
```

---

## ✅ Final Command Sequence

```bash
cd cricket-analytics

# 1. Update README
nano README.md  # Add Phase 2 section

# 2. Update requirements
echo "scikit-learn>=1.3.0" >> requirements.txt

# 3. Check status
git status

# 4. Add all files
git add .

# 5. Commit
git commit -m "Phase 2: Add ML systems (ELO ratings, squad optimization)

Features:
- Team ELO rating system (22 teams)
- Player-weighted ELO (574 players)
- Squad optimization engine
- Team/player rankings dashboards
- Dream XI builder
- Comprehensive documentation

Phase 2 Progress: 1/4 complete"

# 6. Push to GitHub
git push -u origin main
```

---

**All set for GitHub! 🚀**

Tomorrow you can continue with:
- Match Outcome Predictor
- Win Probability Calculator
- Player Performance Forecasting
