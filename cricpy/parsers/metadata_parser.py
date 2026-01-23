"""
Metadata parser for extracting match-level information from Cricsheet YAML files.
"""

import pandas as pd
from typing import Dict, Any, Optional, List


def parse_match_info(match_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract match-level metadata from Cricsheet match dictionary.

    Args:
        match_dict: Dictionary containing match data from Cricsheet YAML

    Returns:
        Dictionary with match metadata including teams, venue, date, outcome, etc.

    Example:
        >>> match_data = load_yaml('match.yaml')
        >>> info = parse_match_info(match_data)
        >>> print(info['venue'])
        'Melbourne Cricket Ground'
    """
    info = match_dict.get('info', {})

    # Extract basic match information
    metadata = {
        # Match identifiers
        'match_type': info.get('match_type'),
        'match_type_number': info.get('match_type_number'),
        'gender': info.get('gender'),
        'season': info.get('season'),

        # Date and venue
        'dates': info.get('dates', []),
        'city': info.get('city'),
        'venue': info.get('venue'),

        # Teams
        'teams': info.get('teams', []),

        # Match format details
        'overs': info.get('overs'),
        'balls_per_over': info.get('balls_per_over', 6),

        # Toss
        'toss_winner': info.get('toss', {}).get('winner'),
        'toss_decision': info.get('toss', {}).get('decision'),

        # Outcome
        'outcome_winner': info.get('outcome', {}).get('winner'),
        'outcome_by': info.get('outcome', {}).get('by', {}),
        'outcome_result': info.get('outcome', {}).get('result'),
        'outcome_method': info.get('outcome', {}).get('method'),

        # Awards
        'player_of_match': info.get('player_of_match', []),

        # Officials
        'umpires': info.get('umpires', []),
        'referee': info.get('referee'),
        'reserve_umpire': info.get('reserve_umpire'),
        'tv_umpire': info.get('tv_umpire'),
    }

    return metadata


def parse_players(match_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract player information from match data.

    Args:
        match_dict: Dictionary containing match data from Cricsheet YAML

    Returns:
        DataFrame with columns: team, player_name, player_id

    Example:
        >>> match_data = load_yaml('match.yaml')
        >>> players_df = parse_players(match_data)
        >>> print(players_df.head())
    """
    info = match_dict.get('info', {})
    players = info.get('players', {})
    registry = info.get('registry', {}).get('people', {})

    rows = []
    for team, player_list in players.items():
        for player in player_list:
            rows.append({
                'team': team,
                'player_name': player,
                'player_id': registry.get(player)
            })

    return pd.DataFrame(rows)


def parse_innings_summary(match_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract innings-level summary information.

    Args:
        match_dict: Dictionary containing match data from Cricsheet YAML

    Returns:
        DataFrame with innings summary (team, runs, wickets, overs)

    Example:
        >>> match_data = load_yaml('match.yaml')
        >>> innings_df = parse_innings_summary(match_data)
        >>> print(innings_df)
    """
    innings = match_dict.get('innings', [])

    rows = []
    for inning in innings:
        for inning_name, inning_data in inning.items():
            team = inning_data.get('team', 'Unknown')

            # Calculate total runs and wickets from deliveries
            total_runs = 0
            total_wickets = 0
            balls_faced = 0

            for delivery in inning_data.get('deliveries', []):
                for ball_number, ball_info in delivery.items():
                    runs = ball_info.get('runs', {})
                    total_runs += runs.get('total', 0)

                    if ball_info.get('wicket'):
                        total_wickets += 1

                    # Count legal deliveries (not wides or no-balls that don't count)
                    extras = ball_info.get('extras', {})
                    if 'wides' not in extras and 'noballs' not in extras:
                        balls_faced += 1

            # Calculate overs
            overs = balls_faced // 6
            balls = balls_faced % 6
            overs_str = f"{overs}.{balls}"

            rows.append({
                'inning': inning_name,
                'team': team,
                'runs': total_runs,
                'wickets': total_wickets,
                'overs': overs_str,
                'balls_faced': balls_faced
            })

    return pd.DataFrame(rows)


def get_match_result_string(match_dict: Dict[str, Any]) -> str:
    """
    Generate a human-readable match result string.

    Args:
        match_dict: Dictionary containing match data from Cricsheet YAML

    Returns:
        Formatted result string (e.g., "India won by 5 wickets")

    Example:
        >>> match_data = load_yaml('match.yaml')
        >>> result = get_match_result_string(match_data)
        >>> print(result)
        'Australia won by 7 runs'
    """
    info = match_dict.get('info', {})
    outcome = info.get('outcome', {})

    winner = outcome.get('winner')
    result = outcome.get('result')
    by = outcome.get('by', {})
    method = outcome.get('method')

    if result:
        return result

    if not winner:
        return "No result"

    # Build result string
    result_parts = [f"{winner} won"]

    if 'runs' in by:
        result_parts.append(f"by {by['runs']} runs")
    elif 'wickets' in by:
        result_parts.append(f"by {by['wickets']} wickets")

    if method:
        result_parts.append(f"({method})")

    return " ".join(result_parts)


def parse_full_match_summary(match_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract complete match summary combining all metadata.

    Args:
        match_dict: Dictionary containing match data from Cricsheet YAML

    Returns:
        Dictionary with comprehensive match summary

    Example:
        >>> match_data = load_yaml('match.yaml')
        >>> summary = parse_full_match_summary(match_data)
        >>> print(summary['match_title'])
        'India vs Pakistan at Dubai'
    """
    info = parse_match_info(match_dict)
    innings_summary = parse_innings_summary(match_dict)

    # Create match title
    teams = info.get('teams', [])
    if len(teams) >= 2:
        match_title = f"{teams[0]} vs {teams[1]}"
        if info.get('city'):
            match_title += f" at {info['city']}"
    else:
        match_title = "Unknown Match"

    # Get result
    result = get_match_result_string(match_dict)

    return {
        'match_title': match_title,
        'match_info': info,
        'innings_summary': innings_summary.to_dict('records') if not innings_summary.empty else [],
        'result': result,
        'player_of_match': info.get('player_of_match', [])
    }
