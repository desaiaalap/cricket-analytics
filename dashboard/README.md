# 📊 Cricket Analytics Dashboard

Interactive web dashboard built with Streamlit for exploring T20 cricket data.

## Quick Start

### Local (without Docker)

```bash
# Install dependencies
pip install streamlit plotly

# Run dashboard
streamlit run dashboard/app.py
```

Open: http://localhost:8501

### With Docker

```bash
docker-compose up dashboard
```

Open: http://localhost:8501

---

## Features

### 📊 Overview
- Total matches, deliveries, players
- Key tournament statistics
- Toss impact analysis

### 🏏 Batting Analysis
- Top 10 run scorers with interactive charts
- Strike rate vs average scatter plots
- Filter by minimum matches played
- Sortable data tables

### ⚾ Bowling Analysis
- Top 10 wicket takers with visualizations
- Economy vs average analysis
- Performance metrics

### 🎯 Match Insights
- Toss decision distribution (pie chart)
- Toss impact on match outcomes
- Top venues by match count
- Win pattern analysis

### 🔍 Player Comparison
- Compare up to 5 batsmen or bowlers
- Multi-metric radar charts
- Side-by-side statistics
- Interactive selection

---

## Dashboard Pages

Navigate using the sidebar:

1. **Overview** - High-level statistics
2. **Batting Analysis** - Detailed batting metrics
3. **Bowling Analysis** - Bowling performance
4. **Match Insights** - Match-level analysis
5. **Player Comparison** - Compare players

---

## Filters

- **Minimum Matches Played** - Filter out players with few matches (sidebar slider)

---

## Technology Stack

- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation
- **Python 3.8+** - Core language

---

## Development

### Run with Auto-reload

```bash
streamlit run dashboard/app.py --server.runOnSave true
```

### Customize

Edit `dashboard/app.py` to:
- Add new pages
- Create new visualizations
- Add more filters
- Customize styling

---

## Screenshots

*(Add screenshots here after deploying)*

---

## Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

### Heroku

```bash
# Add Procfile
echo "web: streamlit run dashboard/app.py --server.port=\$PORT" > Procfile

# Deploy
heroku create cricket-analytics
git push heroku main
```

### Docker

See [DOCKER_GUIDE.md](../DOCKER_GUIDE.md)

---

## Troubleshooting

**"Data not found" error:**
- Make sure you've run `python scripts/process_all_matches.py`
- Check that `data/processed/` contains CSV files

**Port already in use:**
```bash
streamlit run dashboard/app.py --server.port 8502
```

**Slow performance:**
- Data is cached automatically
- Clear cache: Press 'C' in browser → Clear cache

---

Built with ❤️ using Streamlit
