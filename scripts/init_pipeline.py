"""
End-to-End Pipeline Initialization Script

This script runs the complete pipeline:
1. Check if data exists
2. Download data if missing
3. Process data
4. Validate outputs

Usage:
    python scripts/init_pipeline.py
"""

import sys
from pathlib import Path

from cricsheet_downloader import download_cricsheet_data


def check_data_exists(data_dir: Path) -> bool:
    """Check if processed data already exists"""
    required_files = [
        "player_batting_stats.csv",
        "player_bowling_stats.csv",
        "match_summary.csv",
        "ball_by_ball.csv",
    ]

    processed_dir = data_dir / "processed"
    if not processed_dir.exists():
        return False

    for filename in required_files:
        if not (processed_dir / filename).exists():
            return False

    return True


def check_raw_data_exists(data_dir: Path) -> bool:
    """Check if raw YAML data exists"""
    external_dir = data_dir / "external"
    if not external_dir.exists():
        return False

    # Look for YAML files
    yaml_files = list(external_dir.glob("**/*.yaml"))
    return len(yaml_files) > 0


def download_data(data_dir: Path, tournament: str = "t20_internationals_male"):
    """Download cricket data from Cricsheet"""
    print("\n" + "=" * 70)
    print("STEP 1: DOWNLOADING DATA")
    print("=" * 70)

    output_dir = data_dir / "external"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📥 Downloading {tournament} from Cricsheet.org...")
    print(f"   This may take a few minutes depending on your connection.\n")

    try:
        path = download_cricsheet_data(tournament, str(output_dir))
        print(f"\n✅ Data downloaded successfully to: {path}")
        return True
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False


def process_data():
    """Process the downloaded data"""
    print("\n" + "=" * 70)
    print("STEP 2: PROCESSING DATA")
    print("=" * 70)

    print("\n📊 Processing matches and generating statistics...")
    print("   This will create player stats, match summaries, and ball-by-ball data.\n")

    try:
        # Run the processing script using subprocess
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "scripts/process_all_matches.py"],
            capture_output=False,
            text=True,
        )

        if result.returncode == 0:
            print("\n✅ Data processing completed successfully")
            return True
        else:
            print("\n⚠️  Data processing completed with warnings")
            return False
    except Exception as e:
        print(f"\n❌ Processing failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def validate_outputs(data_dir: Path):
    """Validate that all expected output files exist"""
    print("\n" + "=" * 70)
    print("STEP 3: VALIDATION")
    print("=" * 70)

    processed_dir = data_dir / "processed"

    required_files = {
        "player_batting_stats.csv": "Player batting statistics",
        "player_bowling_stats.csv": "Player bowling statistics",
        "match_summaries.csv": "Match summaries",
        "all_deliveries.csv": "Ball-by-ball data",
    }

    print("\n📋 Checking output files...\n")

    all_found = True
    for filename, description in required_files.items():
        filepath = processed_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"   ✅ {filename:30s} ({size:,} bytes) - {description}")
        else:
            print(f"   ❌ {filename:30s} MISSING - {description}")
            all_found = False

    return all_found


def main():
    """Run the complete end-to-end pipeline"""
    print("\n" + "=" * 70)
    print("🏏 CRICKET ANALYTICS - END-TO-END PIPELINE")
    print("=" * 70)
    print("\nThis script will:")
    print("  1. Check if data exists")
    print("  2. Download data if needed (from Cricsheet.org)")
    print("  3. Process all matches")
    print("  4. Generate statistics and summaries")
    print("  5. Validate outputs")
    print("\n" + "=" * 70)

    # Setup paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"

    # Check if processed data already exists
    if check_data_exists(data_dir):
        print("\n✅ Processed data already exists!")
        print("   Skipping download and processing.")
        print("   To force re-processing, delete the data/processed directory.\n")
        return True

    # Check if raw data exists
    if check_raw_data_exists(data_dir):
        print("\n📁 Raw YAML data found. Skipping download.\n")
    else:
        # Download data
        if not download_data(data_dir):
            print("\n❌ Pipeline failed at download stage")
            return False

    # Process data
    if not process_data():
        print("\n❌ Pipeline failed at processing stage")
        return False

    # Validate outputs
    if not validate_outputs(data_dir):
        print("\n❌ Pipeline validation failed - some output files are missing")
        return False

    # Success!
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\n📊 Your cricket analytics data is ready!")
    print("\nNext steps:")
    print("  - Run 'streamlit run dashboard/app.py' to view the interactive dashboard")
    print("  - Open 'jupyter notebook' to explore the analysis notebooks")
    print("  - Check 'data/processed/' for CSV files\n")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
