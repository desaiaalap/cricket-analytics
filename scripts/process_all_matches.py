"""
Process all T20 World Cup matches and create comprehensive datasets

This script uses cricpy functionality to:
1. Load all match YAML files
2. Parse delivery-level data
3. Extract match metadata
4. Create processed datasets for analysis
"""

import sys
sys.path.insert(0, '.')

from scripts.cricpy_loader import load_all_yaml, parse_match, parse_match_info
import pandas as pd
import os
from datetime import datetime

print("="*80)
print("T20 WORLD CUP DATA PROCESSING PIPELINE")
print("="*80)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Configuration
DATA_FOLDER = 'data/external/icc_mens_t20_world_cup_male'
OUTPUT_FOLDER = 'data/processed'

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Step 1: Load all matches
print(f"📂 Loading matches from {DATA_FOLDER}...")
matches = load_all_yaml(DATA_FOLDER)
print(f"✅ Loaded {len(matches)} matches\n")

# Step 2: Process each match
print("🔄 Processing matches...")
all_deliveries = []
match_summaries = []
errors = []

for i, (filename, match_data) in enumerate(matches, 1):
    try:
        # Extract match ID from filename
        match_id = filename.replace('.yaml', '')

        # Parse deliveries
        df = parse_match(match_data)
        df['match_id'] = match_id
        all_deliveries.append(df)

        # Parse match info
        info = parse_match_info(match_data)
        info['match_id'] = match_id
        info['filename'] = filename

        # Add some derived fields
        if info['dates']:
            info['match_date'] = info['dates'][0]

        # Calculate match summary stats
        innings = match_data.get('innings', [])
        if len(innings) >= 2:
            # First innings
            first_inning = innings[0]
            first_inning_name = list(first_inning.keys())[0]
            first_team = first_inning[first_inning_name]['team']

            # Second innings
            second_inning = innings[1]
            second_inning_name = list(second_inning.keys())[0]
            second_team = second_inning[second_inning_name]['team']

            info['first_batting'] = first_team
            info['second_batting'] = second_team

        match_summaries.append(info)

        if i % 20 == 0:
            print(f"  Processed {i}/{len(matches)} matches...")

    except Exception as e:
        print(f"  ⚠️  Error processing {filename}: {e}")
        errors.append({'filename': filename, 'error': str(e)})

print(f"✅ Successfully processed {len(match_summaries)}/{len(matches)} matches")
if errors:
    print(f"⚠️  {len(errors)} matches had errors\n")

# Step 3: Create combined datasets
print("\n💾 Creating datasets...")

# Dataset 1: All deliveries
print("  Creating all_deliveries.csv...")
deliveries_df = pd.concat(all_deliveries, ignore_index=True)
deliveries_df.to_csv(f'{OUTPUT_FOLDER}/all_deliveries.csv', index=False)
print(f"  ✅ Saved {len(deliveries_df):,} deliveries")

# Dataset 2: Match summaries
print("  Creating match_summaries.csv...")
summaries_df = pd.DataFrame(match_summaries)
summaries_df.to_csv(f'{OUTPUT_FOLDER}/match_summaries.csv', index=False)
print(f"  ✅ Saved {len(summaries_df)} match summaries")

# Dataset 3: Player batting aggregates
print("  Creating player_batting_stats.csv...")
legal_deliveries = deliveries_df[deliveries_df['extras_type'] != 'wides'].copy()

batting_stats = legal_deliveries.groupby('batsman').agg({
    'runs_batter': 'sum',
    'ball': 'count',
    'dismissal': lambda x: x.notna().sum(),
    'match_id': 'nunique'
}).reset_index()

batting_stats.columns = ['player', 'runs', 'balls_faced', 'dismissals', 'matches']
batting_stats['average'] = batting_stats.apply(
    lambda row: round(row['runs'] / row['dismissals'], 2) if row['dismissals'] > 0 else row['runs'],
    axis=1
)
batting_stats['strike_rate'] = (batting_stats['runs'] / batting_stats['balls_faced'] * 100).round(2)

# Count boundaries
boundaries = legal_deliveries.groupby('batsman').apply(
    lambda x: pd.Series({
        'fours': (x['runs_batter'] == 4).sum(),
        'sixes': (x['runs_batter'] == 6).sum()
    }), include_groups=False
).reset_index()

batting_stats = batting_stats.merge(boundaries, left_on='player', right_on='batsman', how='left')
batting_stats = batting_stats.drop('batsman', axis=1)
batting_stats = batting_stats.sort_values('runs', ascending=False)

batting_stats.to_csv(f'{OUTPUT_FOLDER}/player_batting_stats.csv', index=False)
print(f"  ✅ Saved batting stats for {len(batting_stats)} players")

# Dataset 4: Player bowling aggregates
print("  Creating player_bowling_stats.csv...")
bowling_stats = deliveries_df.groupby('bowler').agg({
    'ball': 'count',
    'runs_total': 'sum',
    'dismissal': lambda x: x.notna().sum(),
    'match_id': 'nunique'
}).reset_index()

bowling_stats.columns = ['player', 'balls_bowled', 'runs_conceded', 'wickets', 'matches']
bowling_stats['overs'] = bowling_stats['balls_bowled'].apply(lambda x: f"{x // 6}.{x % 6}")
bowling_stats['economy'] = (bowling_stats['runs_conceded'] / bowling_stats['balls_bowled'] * 6).round(2)
bowling_stats['average'] = bowling_stats.apply(
    lambda row: round(row['runs_conceded'] / row['wickets'], 2) if row['wickets'] > 0 else float('inf'),
    axis=1
)
bowling_stats['strike_rate'] = bowling_stats.apply(
    lambda row: round(row['balls_bowled'] / row['wickets'], 2) if row['wickets'] > 0 else float('inf'),
    axis=1
)

bowling_stats = bowling_stats.sort_values('wickets', ascending=False)
bowling_stats.to_csv(f'{OUTPUT_FOLDER}/player_bowling_stats.csv', index=False)
print(f"  ✅ Saved bowling stats for {len(bowling_stats)} players")

# Step 4: Generate summary statistics
print("\n📊 DATASET SUMMARY")
print("="*80)
print(f"Total Deliveries: {len(deliveries_df):,}")
print(f"Total Matches: {len(summaries_df)}")
print(f"Unique Batsmen: {deliveries_df['batsman'].nunique()}")
print(f"Unique Bowlers: {deliveries_df['bowler'].nunique()}")
print(f"Total Runs Scored: {deliveries_df['runs_total'].sum():,}")
print(f"Total Wickets: {deliveries_df['dismissal'].notna().sum()}")
print(f"\nDate Range: {summaries_df['match_date'].min()} to {summaries_df['match_date'].max()}")
print(f"Venues: {summaries_df['venue'].nunique()} unique venues")
print(f"Teams: {len(set([t for teams in summaries_df['teams'] for t in teams]))} teams")

# Save error log if any
if errors:
    pd.DataFrame(errors).to_csv(f'{OUTPUT_FOLDER}/processing_errors.csv', index=False)
    print(f"\n⚠️  Error log saved to {OUTPUT_FOLDER}/processing_errors.csv")

print("\n" + "="*80)
print(f"✅ PROCESSING COMPLETE!")
print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n📁 Output files saved in: {OUTPUT_FOLDER}/")
print("="*80)
