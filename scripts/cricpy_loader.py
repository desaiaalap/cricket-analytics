"""
Cricpy-based data loading and processing for cricket analytics

This module provides cricpy functionality directly in the project.
Copy from CricpyProject once file access is resolved, or use this as standalone.
"""

import os
from typing import Any, Dict, List, Tuple

import pandas as pd
import yaml


def load_yaml(filepath: str) -> Dict:
    """Load a single Cricsheet YAML file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load {filepath}: {e}")
        return None


def load_all_yaml(folder_path: str) -> List[Tuple[str, Dict]]:
    """Load all YAML files from a folder"""
    matches = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            path = os.path.join(folder_path, filename)
            data = load_yaml(path)
            if data:
                matches.append((filename, data))
    return matches


def parse_match(match_dict: Dict[str, Any]) -> pd.DataFrame:
    """Parse Cricsheet match dictionary into delivery-level DataFrame"""
    deliveries = []
    innings = match_dict.get("innings", [])

    for inning in innings:
        for inning_name, inning_data in inning.items():
            batting_team = inning_data.get("team", "Unknown")
            for delivery in inning_data.get("deliveries", []):
                for ball_number, ball_info in delivery.items():
                    row = {
                        "inning": inning_name,
                        "batting_team": batting_team,
                        "ball": ball_number,
                        "batsman": ball_info.get("batsman"),
                        "bowler": ball_info.get("bowler"),
                        "runs_total": ball_info.get("runs", {}).get("total", 0),
                        "runs_batter": ball_info.get("runs", {}).get("batsman", 0),
                        "runs_extras": ball_info.get("runs", {}).get("extras", 0),
                        "extras_type": (
                            list(ball_info.get("extras", {}).keys())[0]
                            if ball_info.get("extras")
                            else None
                        ),
                        "dismissal": ball_info.get("wicket", {}).get("kind"),
                        "fielder": (
                            ", ".join(ball_info["wicket"].get("fielders", []))
                            if "fielders" in ball_info.get("wicket", {})
                            else ball_info.get("wicket", {}).get("fielder")
                        ),
                    }
                    deliveries.append(row)

    return pd.DataFrame(deliveries)


def parse_match_info(match_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Extract match-level metadata"""
    info = match_dict.get("info", {})

    return {
        "match_type": info.get("match_type"),
        "gender": info.get("gender"),
        "dates": info.get("dates", []),
        "city": info.get("city"),
        "venue": info.get("venue"),
        "teams": info.get("teams", []),
        "toss_winner": info.get("toss", {}).get("winner"),
        "toss_decision": info.get("toss", {}).get("decision"),
        "outcome_winner": info.get("outcome", {}).get("winner"),
        "outcome_by": info.get("outcome", {}).get("by", {}),
        "player_of_match": info.get("player_of_match", []),
    }


# Quick test
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        match_file = sys.argv[1]
        print(f"Testing with {match_file}")

        # Load
        data = load_yaml(match_file)
        print(f"✅ Loaded match data")

        # Parse
        df = parse_match(data)
        print(f"✅ Parsed {len(df)} deliveries")

        # Match info
        info = parse_match_info(data)
        print(f"✅ Match: {info['teams'][0]} vs {info['teams'][1]}")
        print(f"   Winner: {info['outcome_winner']}")
    else:
        print("Usage: python cricpy_loader.py <path_to_match.yaml>")
