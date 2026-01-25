"""
Player-Weighted ELO Rating System
Accounts for individual player strength in team ratings
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from collections import defaultdict


class PlayerWeightedELO:
    """
    Hybrid ELO system: Team ratings + Individual player ratings

    Team match rating = Average of 11 players' ELO ratings
    This accounts for squad changes, injuries, and form
    """

    def __init__(self, initial_rating=1500, k_factor=32):
        self.initial_rating = initial_rating
        self.k_factor = k_factor

        # Ratings
        self.team_elo = {}      # Base team ratings (fallback)
        self.player_elo = {}    # Individual player ratings

        # History
        self.match_history = []
        self.player_history = defaultdict(list)  # Track each player's rating over time

    def get_team_rating(self, team):
        """Get base team rating"""
        if team not in self.team_elo:
            self.team_elo[team] = self.initial_rating
        return self.team_elo[team]

    def get_player_rating(self, player):
        """Get individual player rating"""
        if player not in self.player_elo:
            self.player_elo[player] = self.initial_rating
        return self.player_elo[player]

    def get_match_rating(self, team, playing_xi=None):
        """
        Calculate team rating for a specific match

        Args:
            team: Team name
            playing_xi: List of 11 players in the lineup

        Returns:
            Match-specific team rating
        """
        if playing_xi is None or len(playing_xi) == 0:
            # No lineup data - use base team rating
            return self.get_team_rating(team)

        # Calculate average player rating
        player_ratings = [self.get_player_rating(p) for p in playing_xi]

        # Average of player ratings
        return sum(player_ratings) / len(player_ratings)

    def calculate_expected_score(self, rating_a, rating_b):
        """Calculate expected win probability for team A"""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def calculate_margin_multiplier(self, margin, margin_type='runs'):
        """Adjust K-factor based on victory margin"""
        if margin_type == 'runs':
            if margin < 10:
                return 1.0
            elif margin < 30:
                return 1.2
            else:
                return 1.5
        else:  # wickets
            if margin <= 2:
                return 1.0
            elif margin <= 5:
                return 1.2
            else:
                return 1.5

    def update_ratings(self, winner_team, loser_team,
                      winner_xi, loser_xi,
                      margin, margin_type='runs',
                      match_id=None, date=None, venue=None):
        """
        Update both team and player ratings after a match

        Args:
            winner_team: Winning team name
            loser_team: Losing team name
            winner_xi: List of 11 players in winning team
            loser_xi: List of 11 players in losing team
            margin: Victory margin
            margin_type: 'runs' or 'wickets'
            match_id: Match identifier
            date: Match date
            venue: Match venue
        """
        # Get match-specific ratings (player-weighted if lineup available)
        winner_rating = self.get_match_rating(winner_team, winner_xi)
        loser_rating = self.get_match_rating(loser_team, loser_xi)

        # Calculate expected outcome
        winner_expected = self.calculate_expected_score(winner_rating, loser_rating)
        loser_expected = 1 - winner_expected

        # Margin multiplier
        margin_mult = self.calculate_margin_multiplier(margin, margin_type)

        # Calculate rating change
        k = self.k_factor * margin_mult
        rating_change = k * (1 - winner_expected)

        # Update PLAYER ratings (distribute change equally among 11 players)
        player_change = rating_change / 11

        if winner_xi:
            for player in winner_xi:
                current = self.get_player_rating(player)
                new_rating = current + player_change
                self.player_elo[player] = new_rating

                # Track player history
                self.player_history[player].append({
                    'date': date,
                    'match_id': match_id,
                    'team': winner_team,
                    'result': 'won',
                    'rating_before': current,
                    'rating_after': new_rating,
                    'change': player_change
                })

        if loser_xi:
            for player in loser_xi:
                current = self.get_player_rating(player)
                new_rating = current - player_change
                self.player_elo[player] = new_rating

                # Track player history
                self.player_history[player].append({
                    'date': date,
                    'match_id': match_id,
                    'team': loser_team,
                    'result': 'lost',
                    'rating_before': current,
                    'rating_after': new_rating,
                    'change': -player_change
                })

        # Update BASE team ratings (for matches without lineup)
        team_winner_rating = self.get_team_rating(winner_team)
        team_loser_rating = self.get_team_rating(loser_team)

        self.team_elo[winner_team] = team_winner_rating + rating_change
        self.team_elo[loser_team] = team_loser_rating - rating_change

        # Record match history
        self.match_history.append({
            'match_id': match_id,
            'date': date,
            'venue': venue,
            'winner': winner_team,
            'loser': loser_team,
            'margin': margin,
            'margin_type': margin_type,
            'winner_rating': winner_rating,
            'loser_rating': loser_rating,
            'winner_expected': winner_expected,
            'rating_change': rating_change,
            'winner_xi_size': len(winner_xi) if winner_xi else 0,
            'loser_xi_size': len(loser_xi) if loser_xi else 0,
        })

        return winner_rating + rating_change, loser_rating - rating_change

    def get_team_rankings(self):
        """Get current team rankings"""
        rankings = pd.DataFrame([
            {'team': team, 'rating': rating}
            for team, rating in self.team_elo.items()
        ]).sort_values('rating', ascending=False).reset_index(drop=True)

        rankings['rank'] = range(1, len(rankings) + 1)
        return rankings[['rank', 'team', 'rating']]

    def get_player_rankings(self, min_matches=5):
        """
        Get current player rankings

        Args:
            min_matches: Minimum matches to be included
        """
        player_data = []

        for player, rating in self.player_elo.items():
            matches = len(self.player_history[player])

            if matches >= min_matches:
                player_data.append({
                    'player': player,
                    'rating': rating,
                    'matches': matches
                })

        rankings = pd.DataFrame(player_data).sort_values('rating', ascending=False).reset_index(drop=True)
        rankings['rank'] = range(1, len(rankings) + 1)

        return rankings[['rank', 'player', 'rating', 'matches']]

    def save(self, filepath):
        """Save rating system"""
        data = {
            'team_elo': self.team_elo,
            'player_elo': self.player_elo,
            'match_history': self.match_history,
            'player_history': dict(self.player_history),
            'initial_rating': self.initial_rating,
            'k_factor': self.k_factor,
        }

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        print(f"💾 Player-weighted ELO saved to {filepath}")

    def load(self, filepath):
        """Load rating system"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.team_elo = data['team_elo']
        self.player_elo = data['player_elo']
        self.match_history = data['match_history']
        self.player_history = defaultdict(list, data['player_history'])
        self.initial_rating = data['initial_rating']
        self.k_factor = data['k_factor']

        print(f"✅ Player-weighted ELO loaded from {filepath}")
        return self


def extract_playing_xi(deliveries_df, match_id, team):
    """
    Extract playing XI for a team in a match

    Args:
        deliveries_df: Ball-by-ball deliveries DataFrame
        match_id: Match identifier
        team: Team name

    Returns:
        List of player names (up to 11)
    """
    # Get all deliveries for this team batting
    batting = deliveries_df[
        (deliveries_df['match_id'] == match_id) &
        (deliveries_df['batting_team'] == team)
    ]

    # Get all deliveries where this team was bowling
    bowling = deliveries_df[
        (deliveries_df['match_id'] == match_id) &
        (deliveries_df['batting_team'] != team)
    ]

    # Batters = all unique batsmen
    batters = batting['batsman'].unique().tolist()

    # Bowlers = all unique bowlers when this team bowled
    bowlers = bowling['bowler'].unique().tolist()

    # Combine (some overlap for all-rounders)
    playing_xi = list(set(batters + bowlers))

    return playing_xi


def process_all_matches_with_players(
    deliveries_path="data/processed/all_deliveries.csv",
    summaries_path="data/processed/match_summaries.csv"
):
    """
    Process all matches with player-aware ratings

    Args:
        deliveries_path: Path to ball-by-ball data
        summaries_path: Path to match summaries

    Returns:
        PlayerWeightedELO system with calculated ratings
    """
    print("="*80)
    print("PLAYER-WEIGHTED ELO RATING SYSTEM")
    print("="*80)

    # Load data
    print("\n📊 Loading data...")
    deliveries = pd.read_csv(deliveries_path)
    summaries = pd.read_csv(summaries_path)

    # Sort summaries chronologically
    summaries['match_date'] = pd.to_datetime(summaries['match_date'], errors='coerce')
    summaries = summaries.sort_values('match_date').reset_index(drop=True)

    print(f"✅ Loaded {len(summaries)} matches")
    print(f"✅ Loaded {len(deliveries):,} deliveries")

    # Initialize rating system
    rating_system = PlayerWeightedELO(initial_rating=1500, k_factor=32)

    # Process matches
    print("\n🔄 Processing matches with player lineups...")

    processed = 0
    skipped = 0
    missing_lineups = 0

    for idx, match in summaries.iterrows():
        # Get winner
        winner = match.get('outcome_winner')

        if pd.isna(winner) or winner == '':
            skipped += 1
            continue

        # Get teams
        teams = eval(match.get('teams', '[]')) if isinstance(match.get('teams'), str) else match.get('teams', [])

        if len(teams) != 2:
            skipped += 1
            continue

        team1, team2 = teams[0], teams[1]
        loser = team2 if winner == team1 else team1

        # Get margin
        outcome_by = match.get('outcome_by', '{}')
        if isinstance(outcome_by, str):
            outcome_by = eval(outcome_by)

        if 'runs' in outcome_by:
            margin_type = 'runs'
            margin = outcome_by['runs']
        elif 'wickets' in outcome_by:
            margin_type = 'wickets'
            margin = outcome_by['wickets']
        else:
            margin_type = 'runs'
            margin = 1

        if pd.isna(margin) or margin == 0:
            margin = 1

        # Extract playing XIs
        match_id = match.get('match_id')

        try:
            winner_xi = extract_playing_xi(deliveries, match_id, winner)
            loser_xi = extract_playing_xi(deliveries, match_id, loser)

            if len(winner_xi) == 0 or len(loser_xi) == 0:
                missing_lineups += 1
                winner_xi = None
                loser_xi = None
        except:
            missing_lineups += 1
            winner_xi = None
            loser_xi = None

        # Update ratings
        rating_system.update_ratings(
            winner_team=winner,
            loser_team=loser,
            winner_xi=winner_xi,
            loser_xi=loser_xi,
            margin=margin,
            margin_type=margin_type,
            match_id=match_id,
            date=match.get('match_date'),
            venue=match.get('venue')
        )

        processed += 1

        if processed % 20 == 0:
            print(f"   Processed {processed}/{len(summaries)} matches...")

    print(f"\n✅ Processed {processed} matches")
    print(f"   ({skipped} skipped - no result)")
    print(f"   ({missing_lineups} missing lineups - used team ratings)")

    # Display rankings
    print("\n" + "="*80)
    print("TEAM RANKINGS (Player-Weighted)")
    print("="*80)

    team_rankings = rating_system.get_team_rankings()
    print(team_rankings.head(10).to_string(index=False))

    print("\n" + "="*80)
    print("TOP 20 PLAYER RATINGS (Min 5 matches)")
    print("="*80)

    player_rankings = rating_system.get_player_rankings(min_matches=5)
    print(player_rankings.head(20).to_string(index=False))

    # Analysis
    print("\n" + "="*80)
    print("PLAYER INSIGHTS")
    print("="*80)

    print(f"\n📊 Total unique players rated: {len(rating_system.player_elo)}")
    print(f"📊 Players with 5+ matches: {len(player_rankings)}")

    # Top gainers
    player_changes = []
    for player, history in rating_system.player_history.items():
        if len(history) >= 5:
            initial = history[0]['rating_before']
            final = history[-1]['rating_after']
            player_changes.append({
                'player': player,
                'initial': initial,
                'final': final,
                'change': final - initial,
                'matches': len(history)
            })

    changes_df = pd.DataFrame(player_changes).sort_values('change', ascending=False)

    print("\n🚀 Biggest Rating Gains:")
    print(changes_df.head(10)[['player', 'initial', 'final', 'change', 'matches']].to_string(index=False))

    print("\n📉 Biggest Rating Declines:")
    print(changes_df.tail(10)[['player', 'initial', 'final', 'change', 'matches']].to_string(index=False))

    return rating_system


def compare_systems(team_only_path, player_weighted_path):
    """Compare team-only vs player-weighted ELO predictions"""
    print("\n" + "="*80)
    print("COMPARISON: Team-Only vs Player-Weighted ELO")
    print("="*80)

    # Load both systems
    with open(team_only_path, 'rb') as f:
        team_only = pickle.load(f)

    with open(player_weighted_path, 'rb') as f:
        pw_data = pickle.load(f)

    # Compare top teams
    print("\nTeam Ratings Comparison (Top 10):")
    print(f"{'Team':<20} {'Team-Only':<12} {'Player-Weighted':<18} {'Difference'}")
    print("-" * 70)

    for team in sorted(team_only['ratings'].keys(),
                       key=lambda t: team_only['ratings'][t],
                       reverse=True)[:10]:
        team_rating = team_only['ratings'].get(team, 1500)
        pw_rating = pw_data['team_elo'].get(team, 1500)
        diff = pw_rating - team_rating

        print(f"{team:<20} {team_rating:>8.0f}     {pw_rating:>10.0f}       {diff:+7.0f}")


def main():
    """Build player-weighted ELO system"""

    # Build ratings
    rating_system = process_all_matches_with_players()

    # Save system
    rating_system.save("scripts/ml/models/player_weighted_elo.pkl")

    # Save rankings
    team_rankings = rating_system.get_team_rankings()
    team_rankings.to_csv("scripts/ml/models/player_team_rankings.csv", index=False)

    player_rankings = rating_system.get_player_rankings(min_matches=5)
    player_rankings.to_csv("scripts/ml/models/player_rankings.csv", index=False)

    # Save match history
    match_history = pd.DataFrame(rating_system.match_history)
    match_history.to_csv("scripts/ml/models/player_match_history.csv", index=False)

    print(f"\n💾 Saved to scripts/ml/models/")

    # Compare with team-only
    print("\n" + "="*80)
    print("Comparing with team-only ELO...")
    compare_systems(
        "scripts/ml/models/team_ratings.pkl",
        "scripts/ml/models/player_weighted_elo.pkl"
    )

    print("\n" + "="*80)
    print("✅ PLAYER-WEIGHTED ELO SYSTEM COMPLETE")
    print("="*80)

    return rating_system


if __name__ == "__main__":
    rating_system = main()
