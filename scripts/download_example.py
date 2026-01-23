"""
Example: Download Cricket Data from Cricsheet

This script demonstrates how to use the CricsheetDownloader to automatically
download cricket data instead of manual downloading.
"""

from cricsheet_downloader import CricsheetDownloader, download_cricsheet_data


def example_1_simple_download():
    """Example 1: Simple download using convenience function"""
    print("=" * 70)
    print("EXAMPLE 1: Simple Download")
    print("=" * 70)

    # Download T20 World Cup data
    data_path = download_cricsheet_data("t20_internationals_male", "data/external")
    print(f"\n✅ Data downloaded to: {data_path}")


def example_2_downloader_class():
    """Example 2: Using the CricsheetDownloader class"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Using Downloader Class")
    print("=" * 70)

    downloader = CricsheetDownloader()

    # List available tournaments
    print("\n📋 Available tournaments:")
    tournaments = downloader.list_available_tournaments()
    for name in sorted(tournaments.keys())[:10]:  # Show first 10
        print(f"  - {name}")

    # Download specific tournament
    print("\n📥 Downloading IPL data...")
    ipl_path = downloader.download_tournament(
        tournament="ipl", output_dir="data/external", extract=True, cleanup_zip=True
    )
    print(f"✅ IPL data saved to: {ipl_path}")


def example_3_multiple_downloads():
    """Example 3: Download multiple tournaments"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Download Multiple Tournaments")
    print("=" * 70)

    downloader = CricsheetDownloader()

    # Download multiple T20 leagues
    tournaments = ["ipl", "bbl", "cpl", "psl"]

    results = downloader.download_multiple_tournaments(
        tournaments=tournaments, output_dir="data/external"
    )

    # Show results
    print("\n📊 Download Summary:")
    for tournament, path in results.items():
        status = "✅ Success" if path else "❌ Failed"
        print(f"  {tournament:20s}: {status}")


def example_4_get_tournament_info():
    """Example 4: Get tournament information"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Get Tournament Info")
    print("=" * 70)

    downloader = CricsheetDownloader()

    # Get info about IPL
    info = downloader.get_tournament_info("ipl")

    print("\n📋 IPL Tournament Info:")
    for key, value in info.items():
        print(f"  {key:15s}: {value}")


if __name__ == "__main__":
    print("🏏 Cricsheet Downloader - Usage Examples\n")

    # Uncomment the example you want to run:

    # example_1_simple_download()
    # example_2_downloader_class()
    # example_3_multiple_downloads()
    example_4_get_tournament_info()

    print("\n" + "=" * 70)
    print("✅ Examples completed!")
    print("=" * 70)
