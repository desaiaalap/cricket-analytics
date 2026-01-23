"""
Bowling statistics and analysis functions.
"""

import pandas as pd
from typing import Optional


def calculate_bowling_stats(deliveries_df: pd.DataFrame, group_by: Optional[str] = 'bowler') -> pd.DataFrame:
    """
    Calculate comprehensive bowling statistics from delivery-level data.

    Args:
        deliveries_df: DataFrame with delivery-level data from parse_match()
        group_by: Column to group by ('bowler' for individual stats, 'batting_team' for team stats)

    Returns:
        DataFrame with bowling statistics including wickets, economy, average, etc.

    Example:
        >>> df = parse_match(match_data)
        >>> bowling_stats = calculate_bowling_stats(df)
        >>> print(bowling_stats.head())
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Calculate basic stats
    stats = deliveries_df.groupby(group_by).agg({
        'ball': 'count',                          # Total balls bowled
        'runs_total': 'sum',                      # Total runs conceded
        'dismissal': lambda x: x.notna().sum(),   # Wickets taken
        'extras_type': lambda x: (x == 'wides').sum() + (x == 'noballs').sum()  # Wides + No-balls
    }).reset_index()

    stats.columns = [group_by, 'balls_bowled', 'runs_conceded', 'wickets', 'wides_noballs']

    # Calculate overs bowled
    stats['overs'] = stats['balls_bowled'].apply(lambda x: f"{x // 6}.{x % 6}")

    # Calculate economy rate (runs per over)
    stats['economy'] = (stats['runs_conceded'] / stats['balls_bowled'] * 6).round(2)

    # Calculate bowling average (runs per wicket)
    stats['average'] = stats.apply(
        lambda row: (row['runs_conceded'] / row['wickets']).round(2) if row['wickets'] > 0 else float('inf'),
        axis=1
    )

    # Calculate strike rate (balls per wicket)
    stats['strike_rate'] = stats.apply(
        lambda row: (row['balls_bowled'] / row['wickets']).round(2) if row['wickets'] > 0 else float('inf'),
        axis=1
    )

    # Count dots bowled
    dots = deliveries_df[deliveries_df['runs_total'] == 0].groupby(group_by).size().reset_index(name='dots')
    stats = stats.merge(dots, on=group_by, how='left')
    stats['dots'] = stats['dots'].fillna(0).astype(int)

    # Calculate dot ball percentage
    stats['dot_percentage'] = (stats['dots'] / stats['balls_bowled'] * 100).round(2)

    # Count boundaries conceded
    boundaries = deliveries_df.groupby(group_by).apply(
        lambda x: pd.Series({
            'fours_conceded': (x['runs_batter'] == 4).sum(),
            'sixes_conceded': (x['runs_batter'] == 6).sum()
        })
    ).reset_index()

    stats = stats.merge(boundaries, on=group_by, how='left')

    # Sort by wickets taken
    stats = stats.sort_values('wickets', ascending=False).reset_index(drop=True)

    return stats


def calculate_over_by_over(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate over-by-over bowling analysis.

    Args:
        deliveries_df: DataFrame with delivery-level data

    Returns:
        DataFrame with over-by-over statistics

    Example:
        >>> df = parse_match(match_data)
        >>> over_analysis = calculate_over_by_over(df)
        >>> print(over_analysis)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Extract over number from ball (e.g., 5.3 -> 5)
    deliveries_df = deliveries_df.copy()
    deliveries_df['over'] = deliveries_df['ball'].apply(lambda x: int(x))

    # Group by innings, bowler, and over
    over_stats = deliveries_df.groupby(['inning', 'bowler', 'over']).agg({
        'runs_total': 'sum',
        'dismissal': lambda x: x.notna().sum(),
        'ball': 'count'
    }).reset_index()

    over_stats.columns = ['inning', 'bowler', 'over', 'runs', 'wickets', 'balls']

    # Identify maidens (0 runs in the over)
    over_stats['maiden'] = over_stats['runs'] == 0

    return over_stats


def get_bowling_spells(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract bowling spell information (consecutive overs by a bowler).

    Args:
        deliveries_df: DataFrame with delivery-level data

    Returns:
        DataFrame with bowling spell details

    Example:
        >>> df = parse_match(match_data)
        >>> spells = get_bowling_spells(df)
        >>> print(spells)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    deliveries_df = deliveries_df.copy()
    deliveries_df['over'] = deliveries_df['ball'].apply(lambda x: int(x))

    spells = []

    for inning in deliveries_df['inning'].unique():
        inning_df = deliveries_df[deliveries_df['inning'] == inning]

        for bowler in inning_df['bowler'].unique():
            bowler_df = inning_df[inning_df['bowler'] == bowler]

            # Get over numbers this bowler bowled
            overs = sorted(bowler_df['over'].unique())

            # Calculate spell stats
            spell_stats = {
                'inning': inning,
                'bowler': bowler,
                'overs_bowled': len(overs),
                'first_over': min(overs),
                'last_over': max(overs),
                'runs_conceded': bowler_df['runs_total'].sum(),
                'wickets': bowler_df['dismissal'].notna().sum(),
                'balls_bowled': len(bowler_df[bowler_df['extras_type'] != 'wides'])
            }

            # Calculate economy
            spell_stats['economy'] = (spell_stats['runs_conceded'] / spell_stats['balls_bowled'] * 6).round(2)

            spells.append(spell_stats)

    return pd.DataFrame(spells)


def get_wicket_details(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract detailed wicket information.

    Args:
        deliveries_df: DataFrame with delivery-level data

    Returns:
        DataFrame with wicket details (batsman, bowler, type, over, score)

    Example:
        >>> df = parse_match(match_data)
        >>> wickets = get_wicket_details(df)
        >>> print(wickets)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Filter only wicket deliveries
    wickets = deliveries_df[deliveries_df['dismissal'].notna()].copy()

    if wickets.empty:
        return pd.DataFrame()

    # Extract over number
    wickets['over'] = wickets['ball'].apply(lambda x: int(x))

    # Calculate running score at wicket
    wickets = wickets[['inning', 'batting_team', 'ball', 'over', 'batsman', 'bowler', 'dismissal', 'fielder']].copy()

    return wickets.reset_index(drop=True)


def calculate_powerplay_bowling(deliveries_df: pd.DataFrame, powerplay_overs: int = 6) -> pd.DataFrame:
    """
    Calculate bowling statistics during powerplay overs.

    Args:
        deliveries_df: DataFrame with delivery-level data
        powerplay_overs: Number of overs in powerplay (default 6 for T20)

    Returns:
        DataFrame with powerplay bowling statistics by bowler

    Example:
        >>> df = parse_match(match_data)
        >>> pp_bowling = calculate_powerplay_bowling(df, powerplay_overs=6)
        >>> print(pp_bowling)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Filter powerplay deliveries
    powerplay_df = deliveries_df[deliveries_df['ball'] < powerplay_overs].copy()

    # Use the main bowling stats function on powerplay data
    return calculate_bowling_stats(powerplay_df, group_by='bowler')


def get_bowling_milestones(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify bowling milestones (3-wicket hauls, 5-wicket hauls, etc.).

    Args:
        deliveries_df: DataFrame with delivery-level data

    Returns:
        DataFrame with bowlers who achieved milestones

    Example:
        >>> df = parse_match(match_data)
        >>> milestones = get_bowling_milestones(df)
        >>> print(milestones)
    """
    if deliveries_df.empty:
        return pd.DataFrame()

    # Calculate wickets per bowler per innings
    bowling = deliveries_df.groupby(['inning', 'bowler']).agg({
        'dismissal': lambda x: x.notna().sum(),
        'runs_total': 'sum'
    }).reset_index()

    bowling.columns = ['inning', 'bowler', 'wickets', 'runs']

    # Identify milestones
    milestones = []
    for _, row in bowling.iterrows():
        wickets = row['wickets']
        if wickets >= 5:
            milestone = '5-wicket haul'
        elif wickets >= 3:
            milestone = '3-wicket haul'
        else:
            continue

        milestones.append({
            'inning': row['inning'],
            'bowler': row['bowler'],
            'wickets': wickets,
            'runs': row['runs'],
            'figures': f"{wickets}/{row['runs']}",
            'milestone': milestone
        })

    return pd.DataFrame(milestones)
