"""
Cricsheet Data Downloader

This module provides functionality to download cricket data directly from Cricsheet.org
instead of manual downloading.

Usage:
    from scripts.cricsheet_downloader import CricsheetDownloader

    downloader = CricsheetDownloader()
    downloader.download_tournament('icc_mens_t20_world_cup_male', 'data/external')
"""

import requests
import zipfile
import os
from pathlib import Path
from typing import List, Dict, Optional
import json
from urllib.parse import urljoin


class CricsheetDownloader:
    """
    Download cricket data from Cricsheet.org

    Cricsheet provides ball-by-ball data for various cricket formats and tournaments.
    Data is available in YAML, JSON, and CSV formats.
    """

    BASE_URL = "https://cricsheet.org/downloads/"

    # Available tournaments and their download URLs
    TOURNAMENTS = {
        # T20 International
        "icc_mens_t20_world_cup": "t20s_male_yaml.zip",
        "icc_womens_t20_world_cup": "t20s_female_yaml.zip",
        "t20_internationals_male": "t20s_male_yaml.zip",
        "t20_internationals_female": "t20s_female_yaml.zip",
        # T20 Leagues
        "ipl": "ipl_male_yaml.zip",
        "bbl": "bbl_male_yaml.zip",
        "cpl": "cpl_male_yaml.zip",
        "psl": "psl_male_yaml.zip",
        "blast": "blast_male_yaml.zip",
        "hundred": "hundred_male_yaml.zip",
        "super_smash": "super_smash_male_yaml.zip",
        # ODI
        "odi_male": "odis_male_yaml.zip",
        "odi_female": "odis_female_yaml.zip",
        # Test
        "test_male": "tests_male_yaml.zip",
        "test_female": "tests_female_yaml.zip",
        # Other formats
        "all_matches": "all_yaml.zip",
    }

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the downloader

        Args:
            base_url: Optional custom base URL (default: Cricsheet downloads page)
        """
        self.base_url = base_url or self.BASE_URL

    def list_available_tournaments(self) -> Dict[str, str]:
        """
        List all available tournaments

        Returns:
            Dictionary mapping tournament names to download filenames
        """
        return self.TOURNAMENTS.copy()

    def get_download_url(self, tournament: str) -> str:
        """
        Get the download URL for a specific tournament

        Args:
            tournament: Tournament identifier (e.g., 'ipl', 'icc_mens_t20_world_cup')

        Returns:
            Full download URL

        Raises:
            ValueError: If tournament not found
        """
        if tournament not in self.TOURNAMENTS:
            available = ", ".join(self.TOURNAMENTS.keys())
            raise ValueError(f"Tournament '{tournament}' not found. Available: {available}")

        filename = self.TOURNAMENTS[tournament]
        return urljoin(self.base_url, filename)

    def download_tournament(
        self,
        tournament: str,
        output_dir: str = "data/external",
        extract: bool = True,
        cleanup_zip: bool = True,
    ) -> Path:
        """
        Download tournament data from Cricsheet

        Args:
            tournament: Tournament identifier (e.g., 'ipl', 'icc_mens_t20_world_cup')
            output_dir: Directory to save downloaded data
            extract: Whether to extract the ZIP file
            cleanup_zip: Whether to delete ZIP file after extraction

        Returns:
            Path to downloaded/extracted data

        Example:
            >>> downloader = CricsheetDownloader()
            >>> downloader.download_tournament('ipl', 'data/external')
            PosixPath('data/external/ipl_male_yaml')
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Get download URL
        url = self.get_download_url(tournament)
        filename = self.TOURNAMENTS[tournament]
        zip_path = output_path / filename

        print(f"📥 Downloading {tournament} from Cricsheet...")
        print(f"   URL: {url}")
        print(f"   Destination: {zip_path}")

        # Download the file
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Get file size
            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192
            downloaded = 0

            # Download with progress
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = (downloaded / total_size) * 100
                            print(
                                f"\r   Progress: {pct:.1f}% ({downloaded:,}/{total_size:,} bytes)",
                                end="",
                            )

            print(f"\n✅ Download complete: {zip_path}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Download failed: {e}")
            raise

        # Extract if requested
        if extract:
            extract_dir = output_path / filename.replace(".zip", "")
            print(f"\n📦 Extracting to {extract_dir}...")

            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)

                # Count extracted files
                yaml_files = list(extract_dir.glob("**/*.yaml"))
                print(f"✅ Extracted {len(yaml_files)} YAML files")

                # Cleanup ZIP if requested
                if cleanup_zip:
                    zip_path.unlink()
                    print(f"🗑️  Removed ZIP file: {filename}")

                return extract_dir

            except zipfile.BadZipFile as e:
                print(f"❌ Extraction failed: {e}")
                raise

        return zip_path

    def download_multiple_tournaments(
        self, tournaments: List[str], output_dir: str = "data/external", **kwargs
    ) -> Dict[str, Path]:
        """
        Download multiple tournaments

        Args:
            tournaments: List of tournament identifiers
            output_dir: Directory to save downloaded data
            **kwargs: Additional arguments passed to download_tournament()

        Returns:
            Dictionary mapping tournament names to extracted paths

        Example:
            >>> downloader = CricsheetDownloader()
            >>> paths = downloader.download_multiple_tournaments(['ipl', 'bbl'])
        """
        results = {}

        print(f"📥 Downloading {len(tournaments)} tournaments...\n")

        for i, tournament in enumerate(tournaments, 1):
            print(f"\n[{i}/{len(tournaments)}] {tournament}")
            print("=" * 60)

            try:
                path = self.download_tournament(tournament, output_dir, **kwargs)
                results[tournament] = path
                print(f"✅ Success: {tournament}")

            except Exception as e:
                print(f"❌ Failed: {tournament} - {e}")
                results[tournament] = None

        print("\n" + "=" * 60)
        print(f"✅ Completed: {sum(1 for v in results.values() if v)} / {len(tournaments)}")

        return results

    def get_tournament_info(self, tournament: str) -> Dict:
        """
        Get information about a tournament

        Args:
            tournament: Tournament identifier

        Returns:
            Dictionary with tournament metadata
        """
        if tournament not in self.TOURNAMENTS:
            raise ValueError(f"Tournament '{tournament}' not found")

        return {
            "name": tournament,
            "filename": self.TOURNAMENTS[tournament],
            "url": self.get_download_url(tournament),
            "format": "YAML",
            "compressed": True,
        }


def download_cricsheet_data(tournament: str, output_dir: str = "data/external") -> Path:
    """
    Convenience function to download Cricsheet data

    Args:
        tournament: Tournament identifier (e.g., 'ipl', 't20_internationals_male')
        output_dir: Directory to save data

    Returns:
        Path to extracted data

    Example:
        >>> from scripts.cricsheet_downloader import download_cricsheet_data
        >>> data_path = download_cricsheet_data('ipl')
        >>> print(f"Data saved to: {data_path}")
    """
    downloader = CricsheetDownloader()
    return downloader.download_tournament(tournament, output_dir)


if __name__ == "__main__":
    # Example usage
    print("🏏 Cricsheet Data Downloader\n")

    downloader = CricsheetDownloader()

    # List available tournaments
    print("Available tournaments:")
    for name, filename in downloader.list_available_tournaments().items():
        print(f"  - {name:30s} ({filename})")

    print("\n" + "=" * 60)
    print("Example: Download IPL data")
    print("=" * 60)
    print("downloader.download_tournament('ipl', 'data/external')")
