"""
Batting statistics and analysis functions.
"""

import pandas as pd
from typing import Optional


def calculate_batting_stats(deliveries_df: pd.DataFrame, group_by: Optional[str] = 'batsman') -> pd.DataFrame:
    """
    Calculate comprehensive batting statistics from delivery-level data.

    Args:
        deliveries_df: DataFrame with delivery-level data from parse_match()
        group_by: Column to group by ('batsman' for individual stats, 'batting_team' for team stats)

    Returns:
        DataFrame with batting statistics including runs, balls, average, strike rate, etc.

    Example:
        >>> df = parse_match(match_data)
        >>> batting_stats = calculate_batting_stats(df)
        >>> print(batting_stats.head())
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Filter out wides (batsman doesn't face these)
    legal_deliveries = deliveries_df[deliveries_df['extras_type'] != 'wides'].copy()

    # Group by specified column
    stats = legal_deliveries.groupby(group_by).agg({
        'runs_batter': 'sum',          # Total runs scored
        'ball': 'count',                # Balls faced
        'dismissal': lambda x: x.notna().sum()  # Times dismissed
    }).reset_index()

    stats.columns = [group_by, 'runs', 'balls_faced', 'dismissals']

    # Calculate derived metrics
    stats['average'] = stats.apply(
        lambda row: row['runs'] / row['dismissals'] if row['dismissals'] > 0 else row['runs'],
        axis=1
    ).round(2)

    stats['strike_rate'] = (stats['runs'] / stats['balls_faced'] * 100).round(2)

    # Count boundaries
    boundaries = legal_deliveries.groupby(group_by).apply(
        lambda x: pd.Series({
            'fours': (x['runs_batter'] == 4).sum(),
            'sixes': (x['runs_batter'] == 6).sum()
        })
    ).reset_index()

    stats = stats.merge(boundaries, on=group_by, how='left')

    # Calculate dots (0 runs scored by batsman)
    dots = legal_deliveries[legal_deliveries['runs_batter'] == 0].groupby(group_by).size().reset_index(name='dots')
    stats = stats.merge(dots, on=group_by, how='left')
    stats['dots'] = stats['dots'].fillna(0).astype(int)

    # Sort by runs scored
    stats = stats.sort_values('runs', ascending=False).reset_index(drop=True)

    return stats


def get_partnerships(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate partnerships between batting pairs.

    Args:
        deliveries_df: DataFrame with delivery-level data

    Returns:
        DataFrame with partnership details (batsmen, runs, balls, wicket_number)

    Example:
        >>> df = parse_match(match_data)
        >>> partnerships = get_partnerships(df)
        >>> print(partnerships)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    partnerships = []

    # Process each innings separately
    for inning in deliveries_df['inning'].unique():
        inning_df = deliveries_df[deliveries_df['inning'] == inning].copy()

        # Get unique batsmen in order of appearance
        batsmen = inning_df['batsman'].unique()

        wicket_number = 0
        current_partnership = {
            'batsman1': None,
            'batsman2': None,
            'runs': 0,
            'balls': 0
        }

        for idx, row in inning_df.iterrows():
            batsman = row['batsman']

            # Initialize partnership
            if current_partnership['batsman1'] is None:
                current_partnership['batsman1'] = batsman
            elif current_partnership['batsman2'] is None and batsman != current_partnership['batsman1']:
                current_partnership['batsman2'] = batsman

            # Add runs to partnership (exclude extras from partner's end)
            if row['runs_batter'] > 0 or row['extras_type'] in ['legbyes', 'byes']:
                current_partnership['runs'] += row['runs_total']

            # Count balls (exclude wides)
            if row['extras_type'] != 'wides':
                current_partnership['balls'] += 1

            # Check for wicket
            if pd.notna(row['dismissal']):
                wicket_number += 1

                # Save partnership
                if current_partnership['batsman1'] and current_partnership['batsman2']:
                    partnerships.append({
                        'inning': inning,
                        'wicket': wicket_number,
                        'batsman1': current_partnership['batsman1'],
                        'batsman2': current_partnership['batsman2'],
                        'runs': current_partnership['runs'],
                        'balls': current_partnership['balls']
                    })

                # Reset partnership
                dismissed_batsman = batsman
                remaining_batsman = (current_partnership['batsman1']
                                     if dismissed_batsman == current_partnership['batsman2']
                                     else current_partnership['batsman2'])

                current_partnership = {
                    'batsman1': remaining_batsman,
                    'batsman2': None,
                    'runs': 0,
                    'balls': 0
                }

    return pd.DataFrame(partnerships)


def calculate_powerplay_stats(deliveries_df: pd.DataFrame, powerplay_overs: int = 6) -> pd.DataFrame:
    """
    Calculate batting statistics during powerplay overs.

    Args:
        deliveries_df: DataFrame with delivery-level data
        powerplay_overs: Number of overs in powerplay (default 6 for T20)

    Returns:
        DataFrame with powerplay batting statistics by team

    Example:
        >>> df = parse_match(match_data)
        >>> pp_stats = calculate_powerplay_stats(df, powerplay_overs=6)
        >>> print(pp_stats)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Filter powerplay deliveries
    powerplay_df = deliveries_df[deliveries_df['ball'] < powerplay_overs].copy()

    # Calculate stats by team
    stats = powerplay_df.groupby(['inning', 'batting_team']).agg({
        'runs_total': 'sum',
        'dismissal': lambda x: x.notna().sum(),
        'ball': 'count'
    }).reset_index()

    stats.columns = ['inning', 'team', 'runs', 'wickets', 'balls']

    # Calculate run rate
    stats['run_rate'] = (stats['runs'] / stats['balls'] * 6).round(2)

    # Count boundaries
    boundaries = powerplay_df.groupby(['inning', 'batting_team']).apply(
        lambda x: pd.Series({
            'fours': (x['runs_batter'] == 4).sum(),
            'sixes': (x['runs_batter'] == 6).sum()
        })
    ).reset_index()

    boundaries.columns = ['inning', 'team', 'fours', 'sixes']

    stats = stats.merge(boundaries, on=['inning', 'team'], how='left')

    return stats


def get_batting_milestones(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify batting milestones (50s, 100s, etc.).

    Args:
        deliveries_df: DataFrame with delivery-level data

    Returns:
        DataFrame with players who reached milestones

    Example:
        >>> df = parse_match(match_data)
        >>> milestones = get_batting_milestones(df)
        >>> print(milestones)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Calculate runs per batsman per innings
    batting = deliveries_df.groupby(['inning', 'batting_team', 'batsman']).agg({
        'runs_batter': 'sum'
    }).reset_index()

    batting.columns = ['inning', 'team', 'batsman', 'runs']

    # Identify milestones
    milestones = []
    for _, row in batting.iterrows():
        runs = row['runs']
        if runs >= 100:
            milestone = 'Century (100+)'
        elif runs >= 50:
            milestone = 'Half-century (50+)'
        else:
            continue

        milestones.append({
            'inning': row['inning'],
            'team': row['team'],
            'batsman': row['batsman'],
            'runs': runs,
            'milestone': milestone
        })

    return pd.DataFrame(milestones)
