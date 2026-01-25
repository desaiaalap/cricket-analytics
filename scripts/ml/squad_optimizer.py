"""
Squad Optimization System
Select best possible playing XI based on player ELO ratings and role balance
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from itertools import combinations


class SquadOptimizer:
    """
    Optimize team selection based on player ELO ratings and role requirements
    """

    def __init__(self, player_elo_system_path="scripts/ml/models/player_weighted_elo.pkl"):
        """Load player ELO ratings"""
        with open(player_elo_system_path, 'rb') as f:
            data = pickle.load(f)

        self.player_elo = data['player_elo']
        self.player_history = data['player_history']

        # Load deliveries to determine player roles
        self.deliveries = pd.read_csv("data/processed/all_deliveries.csv")

        # Calculate player roles and stats
        self._calculate_player_roles()

    def _calculate_player_roles(self):
        """Determine each player's role (batter/bowler/all-rounder)"""
        print("📊 Analyzing player roles...")

        player_stats = []

        # Get unique players
        all_players = set(self.deliveries['batsman'].unique()) | set(self.deliveries['bowler'].unique())

        for player in all_players:
            # Batting stats
            batting = self.deliveries[self.deliveries['batsman'] == player]
            innings_batted = batting['match_id'].nunique()
            runs_scored = batting['runs_batter'].sum()
            balls_faced = len(batting)
            batting_avg = runs_scored / max(innings_batted, 1)
            strike_rate = (runs_scored / max(balls_faced, 1)) * 100 if balls_faced > 0 else 0

            # Bowling stats
            bowling = self.deliveries[self.deliveries['bowler'] == player]
            innings_bowled = bowling['match_id'].nunique()
            wickets = bowling['dismissal'].notna().sum()
            runs_conceded = bowling['runs_total'].sum()
            balls_bowled = len(bowling)
            bowling_avg = runs_conceded / max(wickets, 1) if wickets > 0 else 999
            economy = (runs_conceded / max(balls_bowled, 1)) * 6 if balls_bowled > 0 else 999

            # Determine role
            if innings_batted >= 5 and innings_bowled >= 5:
                # All-rounder: plays both
                if wickets >= 10 and runs_scored >= 100:
                    role = 'all-rounder'
                elif wickets >= wickets:
                    role = 'bowling-allrounder'
                else:
                    role = 'batting-allrounder'
            elif innings_batted >= innings_bowled and innings_batted >= 3:
                role = 'batter'
            elif innings_bowled >= innings_batted and innings_bowled >= 3:
                role = 'bowler'
            else:
                role = 'unknown'

            # Get ELO rating
            elo_rating = self.player_elo.get(player, 1500)

            player_stats.append({
                'player': player,
                'role': role,
                'elo': elo_rating,
                'matches': max(innings_batted, innings_bowled),
                'innings_batted': innings_batted,
                'innings_bowled': innings_bowled,
                'runs': runs_scored,
                'batting_avg': batting_avg,
                'strike_rate': strike_rate,
                'wickets': wickets,
                'bowling_avg': bowling_avg,
                'economy': economy,
            })

        self.player_stats = pd.DataFrame(player_stats)
        print(f"✅ Analyzed {len(self.player_stats)} players")

    def get_team_players(self, team_name, min_matches=5):
        """
        Get all players who played for a team

        Args:
            team_name: Team name (e.g., 'India')
            min_matches: Minimum matches to be considered

        Returns:
            DataFrame of players with stats
        """
        # Find players who played for this team
        team_players = set()

        # Check batting records
        team_batting = self.deliveries[self.deliveries['batting_team'] == team_name]
        team_players.update(team_batting['batsman'].unique())

        # Check bowling records (when team was fielding)
        team_bowling = self.deliveries[self.deliveries['batting_team'] != team_name]
        # This is tricky - we need match context to know which team the bowler belongs to

        # Simpler approach: use player history
        team_player_names = []
        for player, history in self.player_history.items():
            for match in history:
                if match['team'] == team_name:
                    team_player_names.append(player)
                    break

        # Get stats for team players
        team_stats = self.player_stats[
            self.player_stats['player'].isin(team_player_names) &
            (self.player_stats['matches'] >= min_matches)
        ].copy()

        return team_stats.sort_values('elo', ascending=False)

    def optimize_xi(self, available_players, requirements=None):
        """
        Select best XI from available players

        Args:
            available_players: DataFrame of players (from get_team_players)
            requirements: Dict with role requirements
                          e.g., {'batters': 6, 'bowlers': 4, 'all-rounders': 1}

        Returns:
            Best XI with maximum combined ELO
        """
        if requirements is None:
            # Default balanced XI
            requirements = {
                'batter': 5,
                'bowler': 4,
                'all-rounder': 1,
                'batting-allrounder': 1,
                'flexible': 0  # Fill remaining with best ELO
            }

        print(f"\n🎯 Optimizing XI from {len(available_players)} available players...")
        print(f"   Requirements: {requirements}")

        selected = []
        remaining = available_players.copy()

        # Step 1: Select required roles
        for role, count in requirements.items():
            if role == 'flexible':
                continue

            # Get top players for this role
            role_players = remaining[
                remaining['role'].str.contains(role, case=False, na=False)
            ].nlargest(count, 'elo')

            selected.append(role_players)
            # Remove selected players
            remaining = remaining[~remaining['player'].isin(role_players['player'])]

        # Step 2: Fill remaining slots with highest ELO
        selected_df = pd.concat(selected, ignore_index=True) if selected else pd.DataFrame()
        slots_remaining = 11 - len(selected_df)

        if slots_remaining > 0:
            # Fill with best remaining players
            best_remaining = remaining.nlargest(slots_remaining, 'elo')
            selected_df = pd.concat([selected_df, best_remaining], ignore_index=True)

        # Calculate team stats
        team_elo = selected_df['elo'].mean()
        total_runs = selected_df['runs'].sum()
        total_wickets = selected_df['wickets'].sum()

        print(f"\n✅ Selected XI:")
        print(f"   Team ELO: {team_elo:.0f}")
        print(f"   Total runs scored: {total_runs:,}")
        print(f"   Total wickets taken: {total_wickets}")

        return selected_df

    def compare_squads(self, team1_name, team2_name, min_matches=5):
        """
        Compare best possible XIs from two teams

        Args:
            team1_name: First team
            team2_name: Second team

        Returns:
            Comparison summary
        """
        print("="*80)
        print(f"SQUAD COMPARISON: {team1_name} vs {team2_name}")
        print("="*80)

        # Get players for each team
        team1_players = self.get_team_players(team1_name, min_matches)
        team2_players = self.get_team_players(team2_name, min_matches)

        print(f"\n{team1_name}: {len(team1_players)} available players")
        print(f"{team2_name}: {len(team2_players)} available players")

        # Optimize XIs
        print(f"\n{'='*80}")
        print(f"{team1_name} - BEST XI")
        print(f"{'='*80}")
        team1_xi = self.optimize_xi(team1_players)

        print(f"\n{'='*80}")
        print(f"{team2_name} - BEST XI")
        print(f"{'='*80}")
        team2_xi = self.optimize_xi(team2_players)

        # Comparison
        print(f"\n{'='*80}")
        print("COMPARISON")
        print(f"{'='*80}")

        team1_elo = team1_xi['elo'].mean()
        team2_elo = team2_xi['elo'].mean()

        print(f"\nTeam ELO:")
        print(f"  {team1_name}: {team1_elo:.0f}")
        print(f"  {team2_name}: {team2_elo:.0f}")
        print(f"  Advantage: {team1_name if team1_elo > team2_elo else team2_name} (+{abs(team1_elo - team2_elo):.0f})")

        # Predict match
        win_prob = 1 / (1 + 10**((team2_elo - team1_elo) / 400))

        print(f"\nPredicted Match Outcome:")
        print(f"  {team1_name}: {win_prob*100:.1f}% win chance")
        print(f"  {team2_name}: {(1-win_prob)*100:.1f}% win chance")

        return {
            'team1_xi': team1_xi,
            'team2_xi': team2_xi,
            'team1_elo': team1_elo,
            'team2_elo': team2_elo,
            'win_prob_team1': win_prob
        }

    def what_if_analysis(self, team_name, player_in, player_out):
        """
        What-if analysis: Replace player X with player Y

        Args:
            team_name: Team name
            player_in: Player to include
            player_out: Player to exclude

        Returns:
            Impact analysis
        """
        print(f"\n{'='*80}")
        print(f"WHAT-IF ANALYSIS: {team_name}")
        print(f"{'='*80}")
        print(f"Replace: {player_out}")
        print(f"With: {player_in}")

        # Get best XI
        available = self.get_team_players(team_name)
        best_xi = self.optimize_xi(available)

        # Calculate current ELO
        current_elo = best_xi['elo'].mean()

        # Force player_out to be excluded and player_in to be included
        modified = available[available['player'] != player_out].copy()

        # Ensure player_in is in the pool
        player_in_stats = self.player_stats[self.player_stats['player'] == player_in]

        if len(player_in_stats) == 0:
            print(f"❌ Player '{player_in}' not found in database")
            return None

        # Add to pool if not already
        if player_in not in modified['player'].values:
            modified = pd.concat([modified, player_in_stats], ignore_index=True)

        # Re-optimize
        new_xi = self.optimize_xi(modified)

        # Ensure player_in is in the XI (force selection)
        if player_in not in new_xi['player'].values:
            # Remove lowest ELO player and add player_in
            new_xi = new_xi.nlargest(10, 'elo')
            new_xi = pd.concat([new_xi, player_in_stats], ignore_index=True)

        new_elo = new_xi['elo'].mean()

        # Impact
        impact = new_elo - current_elo

        print(f"\nImpact:")
        print(f"  Original XI ELO: {current_elo:.0f}")
        print(f"  Modified XI ELO: {new_elo:.0f}")
        print(f"  Change: {impact:+.0f} points")

        if impact > 0:
            print(f"  ✅ IMPROVEMENT: Team gets stronger by {impact:.0f} points!")
        elif impact < 0:
            print(f"  ❌ DECLINE: Team gets weaker by {abs(impact):.0f} points")
        else:
            print(f"  ➖ NEUTRAL: No significant change")

        return {
            'original_xi': best_xi,
            'modified_xi': new_xi,
            'original_elo': current_elo,
            'modified_elo': new_elo,
            'impact': impact
        }

    def best_xi_all_time(self, min_matches=10):
        """
        Build the best XI of all time (regardless of team)

        Args:
            min_matches: Minimum matches to qualify

        Returns:
            Dream XI
        """
        print("="*80)
        print("BEST XI OF ALL TIME (Across all teams)")
        print("="*80)

        # Filter qualified players
        qualified = self.player_stats[self.player_stats['matches'] >= min_matches].copy()

        print(f"\n{len(qualified)} players qualified (min {min_matches} matches)")

        # Optimize XI
        dream_xi = self.optimize_xi(qualified)

        print(f"\n{'='*80}")
        print("DREAM XI LINEUP")
        print(f"{'='*80}")

        print(f"\n{'Player':<25} {'Role':<20} {'ELO':<8} {'Runs':<8} {'Wickets'}")
        print("-"*80)

        for _, player in dream_xi.iterrows():
            print(f"{player['player']:<25} {player['role']:<20} {player['elo']:<8.0f} "
                  f"{player['runs']:<8.0f} {player['wickets']:.0f}")

        print(f"\n{'='*80}")
        print(f"Team ELO: {dream_xi['elo'].mean():.0f}")
        print(f"{'='*80}")

        return dream_xi


def main():
    """Run squad optimization examples"""

    # Load optimizer
    optimizer = SquadOptimizer()

    # Example 1: Compare India vs Australia best XIs
    print("\n" + "="*80)
    print("EXAMPLE 1: Best Possible XIs")
    print("="*80)

    comparison = optimizer.compare_squads('India', 'Australia')

    print(f"\n\nIndia XI:")
    print(comparison['team1_xi'][['player', 'role', 'elo', 'runs', 'wickets']].to_string(index=False))

    print(f"\n\nAustralia XI:")
    print(comparison['team2_xi'][['player', 'role', 'elo', 'runs', 'wickets']].to_string(index=False))

    # Example 2: What-if analysis
    print("\n\n" + "="*80)
    print("EXAMPLE 2: What-If Analysis")
    print("="*80)

    india_players = optimizer.get_team_players('India')
    if len(india_players) >= 12:
        player_out = india_players.iloc[10]['player']  # 11th best player
        player_in = india_players.iloc[0]['player']    # Best player

        optimizer.what_if_analysis('India', player_in, player_out)

    # Example 3: Dream XI of all time
    print("\n\n" + "="*80)
    print("EXAMPLE 3: Dream XI (All Time)")
    print("="*80)

    dream_xi = optimizer.best_xi_all_time(min_matches=10)

    # Save results
    print("\n💾 Saving results...")

    comparison['team1_xi'].to_csv("scripts/ml/models/india_best_xi.csv", index=False)
    comparison['team2_xi'].to_csv("scripts/ml/models/australia_best_xi.csv", index=False)
    dream_xi.to_csv("scripts/ml/models/dream_xi_all_time.csv", index=False)

    print("✅ Saved to scripts/ml/models/")

    print("\n" + "="*80)
    print("✅ SQUAD OPTIMIZATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
