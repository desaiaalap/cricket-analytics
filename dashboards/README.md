# Cricket Analytics Dashboard

## Running the Dashboard

### Setup

1. Ensure conda environment is activated:
```bash
conda activate cricket-analytics
```

2. Install dependencies (if not already done):
```bash
pip install -r ../requirements.txt
```

### Launch Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## Features

- **Home**: Overview statistics and recent matches
- **Match Analysis**: Detailed match-by-match breakdown
- **Player Stats**: Individual player performance metrics
- **Predictions**: ML-powered match outcome predictions
- **Team Comparison**: Head-to-head team analysis
- **About**: Information about the dashboard

## Configuration

To customize the dashboard, you can modify:

- `app.py` - Main application logic
- Streamlit theme in `.streamlit/config.toml` (create if needed)

## Data Integration

Currently uses placeholder data. To integrate real data:

1. Connect CricPy API in `src/etl/data_loader.py`
2. Update data loading functions in `app.py`
3. Ensure data is in the correct format expected by visualization functions

## Future Enhancements

- Real-time match updates
- Live prediction during matches
- Sentiment analysis integration
- Video analysis integration
- Export functionality for reports
