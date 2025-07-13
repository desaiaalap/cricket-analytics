A central repo for all cricket-related projects:

T20 scouting dashboard

Match outcome prediction

Player tracking (video)

Bonus: sentiment analysis or injury tracking in future

Folder Structure:
cricket-analytics/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/  ← Cricsheet or other YAML/CSV downloads
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_match_prediction.ipynb
│   └── 04_sentiment_analysis.ipynb
├── dashboards/
│   └── t20_scouting_dashboard.twbx
├── src/
│   ├── etl/
│   ├── modeling/
│   └── tracking/
├── video_analysis/
│   ├── raw_videos/
│   ├── processed_frames/
│   └── tracking_output.csv
├── docs/
│   └── project_overview.md
├── blog_drafts/
│   └── scouting_blog.md
├── README.md
└── requirements.txt
