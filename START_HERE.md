# ⚡ START HERE

## Option 1: Docker (Easiest - Fully Automated E2E!)

**Have Docker installed? Just run:**

```bash
docker-compose up --build
```

**This ONE command does EVERYTHING:**
- ✅ Downloads cricket data automatically from Cricsheet.org
- ✅ Processes all matches and generates statistics
- ✅ Launches interactive dashboard on **http://localhost:8501**

**No manual steps. No configuration. True end-to-end automation!** 🎉

👉 **[See E2E_GUIDE.md](E2E_GUIDE.md)** for complete E2E details
👉 **[See DOCKER_GUIDE.md](DOCKER_GUIDE.md)** for Docker reference

---

## Option 2: Python Demo

**Have Python? Run this:**

```bash
python demo.py
```

Everything is automatic. ✨

---

## What Happens?

The demo will:
1. ✅ Check if you have the needed libraries (installs if missing)
2. ✅ Download cricket data automatically
3. ✅ Process all the matches
4. ✅ Show you cool insights about T20 cricket!

**Total time: 3-5 minutes** (most of it is downloading data)

---

## Already Set Up?

### View the Analysis
```bash
jupyter notebook
```
Then open: `notebooks/02_batting_analysis.ipynb`

### Quick Stats
```python
import pandas as pd

# Top run scorers
batting = pd.read_csv('data/processed/player_batting_stats.csv')
print(batting.nlargest(5, 'runs')[['player', 'runs', 'average']])
```

---

## Learn More

- **[QUICKSTART.md](QUICKSTART.md)** - 3-step manual setup
- **[README.md](README.md)** - Full documentation
- **[Makefile](Makefile)** - Useful commands

---

## Need Help?

**Something not working?**
1. Make sure you have Python 3.8+ installed: `python --version`
2. Try installing manually: `pip install -r requirements.txt`
3. Open an issue on GitHub

**Email:** adesai@altsportsdata.com

---

**Remember: Just run `python demo.py` and you're done!** 🚀
