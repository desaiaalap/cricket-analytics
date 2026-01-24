#!/usr/bin/env python3
"""
Cricket Analytics - Quick Demo
Just run: python demo.py

This script will:
1. Download sample data (if not present)
2. Process it
3. Show you cool insights!

No configuration needed!
"""

import os
import sys
from pathlib import Path


def print_header(text):
    """Print a nice header"""
    print("\n" + "=" * 70)
    print(f"🏏 {text}")
    print("=" * 70 + "\n")


def check_and_install_dependencies():
    """Check if dependencies are installed"""
    print_header("Step 1: Checking Dependencies")

    required = ["pandas", "yaml", "requests"]
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package} is installed")
        except ImportError:
            missing.append(package)
            print(f"   ❌ {package} is missing")

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Installing now...")
        os.system("pip install -r requirements.txt -q")
        print("   ✅ Dependencies installed!")

    print("\n✅ All dependencies ready!\n")


def download_sample_data():
    """Download sample T20 data if not present"""
    print_header("Step 2: Getting Sample Data")

    data_dir = Path("data/external/t20s_male_yaml")

    if data_dir.exists() and list(data_dir.glob("*.yaml")):
        print(f"   ✅ Data already exists ({len(list(data_dir.glob('*.yaml')))} files)")
        return

    print("   📥 Downloading T20 World Cup data...")
    print("   (This will take 1-2 minutes)\n")

    try:
        from scripts.cricsheet_downloader import download_cricsheet_data

        download_cricsheet_data("t20_internationals_male", "data/external")
        print("\n   ✅ Data downloaded successfully!")
    except Exception as e:
        print(f"\n   ⚠️  Download failed: {e}")
        print("   Please check your internet connection and try again")
        sys.exit(1)


def process_data():
    """Process the matches"""
    print_header("Step 3: Processing Matches")

    processed_file = Path("data/processed/player_batting_stats.csv")

    if processed_file.exists():
        print("   ✅ Data already processed")
        return

    print("   ⚙️  Processing matches...")
    print("   (This will take 30-60 seconds)\n")

    try:
        # Import and run processing
        os.system("python scripts/process_all_matches.py")
        print("\n   ✅ Processing complete!")
    except Exception as e:
        print(f"\n   ⚠️  Processing failed: {e}")
        sys.exit(1)


def show_insights():
    """Display cool insights"""
    print_header("Step 4: Cricket Insights! 🎯")

    try:
        import pandas as pd

        # Load data
        batting = pd.read_csv("data/processed/player_batting_stats.csv")
        bowling = pd.read_csv("data/processed/player_bowling_stats.csv")
        matches = pd.read_csv("data/processed/match_summaries.csv")

        # Top run scorers
        print("🏏 TOP 10 RUN SCORERS:")
        print("-" * 70)
        top_batsmen = batting.nlargest(10, "runs")[
            ["player", "runs", "average", "strike_rate", "matches"]
        ]
        print(top_batsmen.to_string(index=False))

        print("\n")

        # Top wicket takers
        print("⚾ TOP 10 WICKET TAKERS:")
        print("-" * 70)
        top_bowlers = bowling.nlargest(10, "wickets")[
            ["player", "wickets", "economy", "average", "matches"]
        ]
        print(top_bowlers.to_string(index=False))

        print("\n")

        # Match stats
        print("📊 TOURNAMENT STATISTICS:")
        print("-" * 70)
        print(f"   Total matches analyzed: {len(matches)}")
        print(f"   Total deliveries: {len(pd.read_csv('data/processed/all_deliveries.csv')):,}")
        print(f"   Unique batsmen: {len(batting)}")
        print(f"   Unique bowlers: {len(bowling)}")
        print(f"   Total runs scored: {batting['runs'].sum():,}")
        print(f"   Total wickets taken: {bowling['wickets'].sum():,}")

        # Toss impact
        matches_with_outcome = matches[matches["outcome_winner"].notna()]
        toss_winners_who_won_match = matches_with_outcome[
            matches_with_outcome["toss_winner"] == matches_with_outcome["outcome_winner"]
        ]
        toss_win_pct = (
            len(toss_winners_who_won_match) / len(matches_with_outcome) * 100
        )
        print(f"   Toss winners also won match: {toss_win_pct:.1f}%")

    except FileNotFoundError:
        print("⚠️  Processed data not found. Please run processing first.")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️  Error loading data: {e}")
        sys.exit(1)


def show_next_steps():
    """Show what to do next"""
    print_header("What's Next? 🚀")

    print("📓 Open Jupyter notebooks for interactive analysis:")
    print("   jupyter notebook")
    print("   Then open: notebooks/02_batting_analysis.ipynb\n")

    print("📊 View the processed data:")
    print("   ls data/processed/\n")

    print("🔍 Try different tournaments:")
    print("   from scripts.cricsheet_downloader import download_cricsheet_data")
    print("   download_cricsheet_data('ipl', 'data/external')  # Indian Premier League\n")

    print("📚 Read the documentation:")
    print("   cat QUICKSTART.md\n")

    print("✅ You're all set! Happy analyzing! 🏏\n")


def main():
    """Main demo function"""
    print("\n" + "=" * 70)
    print("🏏 CRICKET ANALYTICS - AUTOMATED DEMO")
    print("=" * 70)
    print("\nThis will set up everything and show you cool cricket insights!")
    print("No configuration needed - just sit back and watch! ☕")

    try:
        check_and_install_dependencies()
        download_sample_data()
        process_data()
        show_insights()
        show_next_steps()

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("\nPlease check the logs and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
