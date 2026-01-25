"""
Team Strength Rating System
ELO-based power rankings for cricket teams
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import pickle


class TeamRatingSystem:
    """ELO-based rating system for cricket teams"""

    def __init__(self, initial_rating=1500, k_factor=32):
        self.initial_rating = initial_rating
        self.k_factor = k_factor
        self.ratings = {}  # {team: current_rating}
        self.rating_history = []  # List of rating snapshots over time

    def get_rating(self, team):
        """Get current rating for a team"""
        if team not in self.ratings:
            self.ratings[team] = self.initial_rating
        return self.ratings[team]

    def calculate_expected_score(self, rating_a, rating_b):
        """Calculate expected win probability for team A"""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def calculate_margin_multiplier(self, margin, margin_type='runs'):
        """
        Adjust K-factor based on victory margin

        Args:
            margin: Runs or wickets margin
            margin_type: 'runs' or 'wickets'

        Returns:
            Multiplier (1.0 to 1.5)
        """
        if margin_type == 'runs':
            if margin < 10:
                return 1.0  # Close match
            elif margin < 30:
                return 1.2  # Comfortable win
            else:
                return 1.5  # Dominant win
        else:  # wickets
            if margin <= 2:
                return 1.0  # Close match
            elif margin <= 5:
                return 1.2  # Comfortable win
            else:
                return 1.5  # Dominant win

    def update_ratings(self, winner, loser, margin, margin_type='runs',
                      match_id=None, date=None, venue=None):
        """
        Update ELO ratings after a match

        Args:
            winner: Winning team name
            loser: Losing team name
            margin: Victory margin (runs or wickets)
            margin_type: 'runs' or 'wickets'
            match_id: Match identifier (for tracking)
            date: Match date
            venue: Match venue
        """
        # Get current ratings
        winner_rating = self.get_rating(winner)
        loser_rating = self.get_rating(loser)

        # Calculate expected scores
        winner_expected = self.calculate_expected_score(winner_rating, loser_rating)
        loser_expected = 1 - winner_expected

        # Margin multiplier
        margin_mult = self.calculate_margin_multiplier(margin, margin_type)

        # Calculate rating changes
        k = self.k_factor * margin_mult
        winner_change = k * (1 - winner_expected)
        loser_change = k * (0 - loser_expected)

        # Update ratings
        new_winner_rating = winner_rating + winner_change
        new_loser_rating = loser_rating + loser_change

        self.ratings[winner] = new_winner_rating
        self.ratings[loser] = new_loser_rating

        # Record history
        self.rating_history.append({
            'match_id': match_id,
            'date': date,
            'venue': venue,
            'winner': winner,
            'loser': loser,
            'margin': margin,
            'margin_type': margin_type,
            'winner_rating_before': winner_rating,
            'winner_rating_after': new_winner_rating,
            'winner_change': winner_change,
            'loser_rating_before': loser_rating,
            'loser_rating_after': new_loser_rating,
            'loser_change': loser_change,
            'winner_expected': winner_expected,
        })

        return new_winner_rating, new_loser_rating

    def get_current_rankings(self):
        """Get current team rankings sorted by rating"""
        rankings = pd.DataFrame([
            {'team': team, 'rating': rating}
            for team, rating in self.ratings.items()
        ]).sort_values('rating', ascending=False).reset_index(drop=True)

        rankings['rank'] = range(1, len(rankings) + 1)
        return rankings[['rank', 'team', 'rating']]

    def get_rating_history(self):
        """Get full rating history as DataFrame"""
        return pd.DataFrame(self.rating_history)

    def predict_match_winner(self, team_a, team_b):
        """
        Predict match outcome based on current ratings

        Returns:
            dict with win probabilities
        """
        rating_a = self.get_rating(team_a)
        rating_b = self.get_rating(team_b)

        prob_a = self.calculate_expected_score(rating_a, rating_b)
        prob_b = 1 - prob_a

        return {
            'team_a': team_a,
            'team_b': team_b,
            'rating_a': rating_a,
            'rating_b': rating_b,
            'prob_a_wins': prob_a,
            'prob_b_wins': prob_b,
            'favorite': team_a if prob_a > 0.5 else team_b,
            'underdog': team_b if prob_a > 0.5 else team_a,
        }

    def save(self, filepath):
        """Save rating system to disk"""
        data = {
            'ratings': self.ratings,
            'rating_history': self.rating_history,
            'initial_rating': self.initial_rating,
            'k_factor': self.k_factor,
        }

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        print(f"💾 Rating system saved to {filepath}")

    def load(self, filepath):
        """Load rating system from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.ratings = data['ratings']
        self.rating_history = data['rating_history']
        self.initial_rating = data['initial_rating']
        self.k_factor = data['k_factor']

        print(f"✅ Rating system loaded from {filepath}")
        return self


def process_all_matches(data_path="data/processed/match_summaries.csv"):
    """
    Process all matches chronologically and build team ratings

    Args:
        data_path: Path to match summaries CSV

    Returns:
        TeamRatingSystem with ratings calculated
    """
    print("="*80)
    print("TEAM STRENGTH RATING SYSTEM")
    print("="*80)

    # Load match data
    print("\n📊 Loading match data...")
    df = pd.read_csv(data_path)

    # Parse dates for chronological processing
    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')

    # Sort by date (chronological order is critical!)
    df = df.sort_values('match_date').reset_index(drop=True)

    print(f"✅ Loaded {len(df)} matches")
    print(f"   Date range: {df['match_date'].min()} to {df['match_date'].max()}")

    # Initialize rating system
    rating_system = TeamRatingSystem(initial_rating=1500, k_factor=32)

    # Process each match
    print("\n🔄 Processing matches chronologically...")

    processed = 0
    skipped = 0

    for idx, match in df.iterrows():
        # Determine winner
        winner = match.get('outcome_winner')

        # Skip matches without a winner (no result, tie, etc.)
        if pd.isna(winner) or winner == '':
            skipped += 1
            continue

        # Get teams from 'teams' column (list of two teams)
        teams = eval(match.get('teams', '[]')) if isinstance(match.get('teams'), str) else match.get('teams', [])

        if len(teams) != 2:
            skipped += 1
            continue

        team1, team2 = teams[0], teams[1]

        # Determine loser
        loser = team2 if winner == team1 else team1

        # Parse outcome_by (e.g., {'runs': 21} or {'wickets': 5})
        outcome_by = match.get('outcome_by', '{}')
        if isinstance(outcome_by, str):
            outcome_by = eval(outcome_by)

        # Get margin type and value
        if 'runs' in outcome_by:
            margin_type = 'runs'
            margin = outcome_by['runs']
        elif 'wickets' in outcome_by:
            margin_type = 'wickets'
            margin = outcome_by['wickets']
        else:
            margin_type = 'runs'
            margin = 1  # Default for unknown margin

        # Handle missing margin (assume close match)
        if pd.isna(margin) or margin == 0:
            margin = 1

        # Update ratings
        rating_system.update_ratings(
            winner=winner,
            loser=loser,
            margin=margin,
            margin_type=margin_type,
            match_id=match.get('match_id'),
            date=match.get('match_date'),
            venue=match.get('venue')
        )

        processed += 1

        # Progress indicator
        if processed % 20 == 0:
            print(f"   Processed {processed}/{len(df)} matches...")

    print(f"\n✅ Processed {processed} matches ({skipped} skipped - no result)")

    # Display final rankings
    print("\n" + "="*80)
    print("FINAL TEAM RANKINGS")
    print("="*80)

    rankings = rating_system.get_current_rankings()
    print(rankings.to_string(index=False))

    # Show rating changes
    history = rating_system.get_rating_history()

    if len(history) > 0:
        print("\n" + "="*80)
        print("BIGGEST RATING GAINS")
        print("="*80)

        biggest_gains = history.nlargest(5, 'winner_change')[
            ['date', 'winner', 'loser', 'margin', 'winner_change']
        ]
        print(biggest_gains.to_string(index=False))

        print("\n" + "="*80)
        print("BIGGEST UPSETS (Lower-rated team won)")
        print("="*80)

        upsets = history[history['winner_expected'] < 0.3].nsmallest(5, 'winner_expected')[
            ['date', 'winner', 'loser', 'winner_expected', 'winner_change']
        ]
        print(upsets.to_string(index=False))

    return rating_system


def analyze_rating_trends(rating_system):
    """Analyze how team ratings evolved over time"""
    history = rating_system.get_rating_history()

    if len(history) == 0:
        print("No rating history available")
        return

    print("\n" + "="*80)
    print("RATING TRENDS ANALYSIS")
    print("="*80)

    # Get all teams
    teams = set(history['winner'].unique()) | set(history['loser'].unique())

    # Track each team's rating over time
    team_trends = {}

    for team in teams:
        team_history = []

        # Get all matches for this team
        for _, match in history.iterrows():
            if match['winner'] == team:
                team_history.append({
                    'date': match['date'],
                    'rating': match['winner_rating_after'],
                    'change': match['winner_change']
                })
            elif match['loser'] == team:
                team_history.append({
                    'date': match['date'],
                    'rating': match['loser_rating_after'],
                    'change': match['loser_change']
                })

        if team_history:
            team_df = pd.DataFrame(team_history)
            team_trends[team] = {
                'matches': len(team_history),
                'min_rating': team_df['rating'].min(),
                'max_rating': team_df['rating'].max(),
                'final_rating': team_df['rating'].iloc[-1],
                'total_change': team_df['rating'].iloc[-1] - 1500,
                'volatility': team_df['change'].abs().mean(),
            }

    # Convert to DataFrame
    trends_df = pd.DataFrame(team_trends).T
    trends_df = trends_df.sort_values('final_rating', ascending=False)

    print("\n📈 Most Improved Teams (total rating gain):")
    print(trends_df.nlargest(5, 'total_change')[['matches', 'final_rating', 'total_change']].to_string())

    print("\n📉 Biggest Declines (total rating loss):")
    print(trends_df.nsmallest(5, 'total_change')[['matches', 'final_rating', 'total_change']].to_string())

    print("\n🎢 Most Volatile Teams (biggest rating swings):")
    print(trends_df.nlargest(5, 'volatility')[['matches', 'final_rating', 'volatility']].to_string())

    print("\n⭐ Peak Ratings (highest ever achieved):")
    print(trends_df.nlargest(5, 'max_rating')[['max_rating', 'final_rating']].to_string())


def main():
    """Build and analyze team rating system"""

    # Build ratings from match data
    rating_system = process_all_matches()

    # Analyze trends
    analyze_rating_trends(rating_system)

    # Save rating system
    rating_system.save("scripts/ml/models/team_ratings.pkl")

    # Save rankings to CSV
    rankings = rating_system.get_current_rankings()
    rankings.to_csv("scripts/ml/models/team_rankings.csv", index=False)
    print(f"\n💾 Rankings saved to scripts/ml/models/team_rankings.csv")

    # Save full history
    history = rating_system.get_rating_history()
    history.to_csv("scripts/ml/models/team_rating_history.csv", index=False)
    print(f"💾 Rating history saved to scripts/ml/models/team_rating_history.csv")

    print("\n" + "="*80)
    print("✅ TEAM RATING SYSTEM COMPLETE")
    print("="*80)

    return rating_system


if __name__ == "__main__":
    rating_system = main()
