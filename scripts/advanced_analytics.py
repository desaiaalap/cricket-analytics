"""
Advanced Cricket Analytics
Provides deeper insights: partnerships, phase analysis, player forms, match momentum
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple


class AdvancedAnalytics:
    """Advanced cricket analytics for deeper insights"""

    def __init__(self, deliveries_df, matches_df, batting_df, bowling_df):
        self.deliveries = deliveries_df
        self.matches = matches_df
        self.batting = batting_df
        self.bowling = bowling_df

    def analyze_partnerships(self, min_runs=30) -> pd.DataFrame:
        """
        Analyze batting partnerships

        Args:
            min_runs: Minimum runs for partnership to be included

        Returns:
            DataFrame with partnership details
        """
        partnerships = []

        for match_id in self.deliveries["match_id"].unique():
            match_balls = self.deliveries[self.deliveries["match_id"] == match_id]

            for inning in match_balls["inning"].unique():
                inning_balls = match_balls[match_balls["inning"] == inning]

                # Track partnerships (wicket to wicket)
                current_partnership = {"runs": 0, "balls": 0, "batsmen": set()}

                for _, ball in inning_balls.iterrows():
                    current_partnership["runs"] += ball.get("runs_batter", 0)
                    current_partnership["balls"] += 1
                    current_partnership["batsmen"].add(ball.get("batter", "Unknown"))

                    # If wicket, record partnership
                    if pd.notna(ball.get("wicket_kind")):
                        if current_partnership["runs"] >= min_runs:
                            partnerships.append(
                                {
                                    "match_id": match_id,
                                    "inning": inning,
                                    "runs": current_partnership["runs"],
                                    "balls": current_partnership["balls"],
                                    "batsmen": ", ".join(
                                        sorted(current_partnership["batsmen"])
                                    ),
                                    "run_rate": (
                                        current_partnership["runs"]
                                        / current_partnership["balls"]
                                        * 6
                                        if current_partnership["balls"] > 0
                                        else 0
                                    ),
                                }
                            )
                        # Reset
                        current_partnership = {"runs": 0, "balls": 0, "batsmen": set()}

        return pd.DataFrame(partnerships).sort_values("runs", ascending=False)

    def analyze_match_phases(self) -> pd.DataFrame:
        """
        Analyze performance in different match phases
        Powerplay (1-6), Middle (7-15), Death (16-20)

        Returns:
            DataFrame with phase-wise statistics
        """
        phase_stats = []

        for match_id in self.deliveries["match_id"].unique():
            match_balls = self.deliveries[self.deliveries["match_id"] == match_id]

            for inning in match_balls["inning"].unique():
                inning_balls = match_balls[match_balls["inning"] == inning].copy()

                # Add phase column
                inning_balls["phase"] = inning_balls["over"].apply(self._get_phase)

                # Calculate stats per phase
                for phase in ["Powerplay", "Middle", "Death"]:
                    phase_balls = inning_balls[inning_balls["phase"] == phase]

                    if len(phase_balls) > 0:
                        phase_stats.append(
                            {
                                "match_id": match_id,
                                "inning": inning,
                                "phase": phase,
                                "runs": phase_balls["runs_total"].sum(),
                                "wickets": phase_balls["wicket_kind"].notna().sum(),
                                "balls": len(phase_balls),
                                "run_rate": (
                                    phase_balls["runs_total"].sum() / len(phase_balls) * 6
                                ),
                                "boundary_pct": (
                                    len(
                                        phase_balls[
                                            phase_balls["runs_batter"].isin([4, 6])
                                        ]
                                    )
                                    / len(phase_balls)
                                    * 100
                                ),
                            }
                        )

        return pd.DataFrame(phase_stats)

    def _get_phase(self, over: float) -> str:
        """Determine match phase based on over number"""
        if over < 6:
            return "Powerplay"
        elif over < 16:
            return "Middle"
        else:
            return "Death"

    def analyze_player_form(self, player_name: str, is_batsman: bool = True) -> Dict:
        """
        Analyze player's form across matches

        Args:
            player_name: Name of the player
            is_batsman: True for batting stats, False for bowling

        Returns:
            Dictionary with form analysis
        """
        if is_batsman:
            # Batting form
            player_balls = self.deliveries[self.deliveries["batter"] == player_name]

            # Group by match
            match_stats = []
            for match_id in player_balls["match_id"].unique():
                match_balls = player_balls[player_balls["match_id"] == match_id]

                match_stats.append(
                    {
                        "match_id": match_id,
                        "runs": match_balls["runs_batter"].sum(),
                        "balls": len(match_balls),
                        "fours": len(match_balls[match_balls["runs_batter"] == 4]),
                        "sixes": len(match_balls[match_balls["runs_batter"] == 6]),
                        "strike_rate": (
                            match_balls["runs_batter"].sum() / len(match_balls) * 100
                            if len(match_balls) > 0
                            else 0
                        ),
                    }
                )

            form_df = pd.DataFrame(match_stats)

            return {
                "player": player_name,
                "type": "batting",
                "matches": len(form_df),
                "avg_runs": form_df["runs"].mean(),
                "best_score": form_df["runs"].max(),
                "consistency": form_df["runs"].std(),
                "recent_form": form_df.tail(5)["runs"].mean(),
                "match_stats": form_df,
            }

        else:
            # Bowling form
            player_balls = self.deliveries[self.deliveries["bowler"] == player_name]

            match_stats = []
            for match_id in player_balls["match_id"].unique():
                match_balls = player_balls[player_balls["match_id"] == match_id]

                match_stats.append(
                    {
                        "match_id": match_id,
                        "wickets": match_balls["wicket_kind"].notna().sum(),
                        "runs": match_balls["runs_total"].sum(),
                        "balls": len(match_balls),
                        "economy": (
                            match_balls["runs_total"].sum() / len(match_balls) * 6
                            if len(match_balls) > 0
                            else 0
                        ),
                    }
                )

            form_df = pd.DataFrame(match_stats)

            return {
                "player": player_name,
                "type": "bowling",
                "matches": len(form_df),
                "avg_wickets": form_df["wickets"].mean(),
                "best_figures": form_df["wickets"].max(),
                "avg_economy": form_df["economy"].mean(),
                "recent_form": form_df.tail(5)["wickets"].mean(),
                "match_stats": form_df,
            }

    def get_match_momentum(self, match_id: str) -> pd.DataFrame:
        """
        Calculate match momentum over by over

        Args:
            match_id: Match identifier

        Returns:
            DataFrame with over-by-over momentum
        """
        match_balls = self.deliveries[self.deliveries["match_id"] == match_id]

        momentum = []

        for inning in match_balls["inning"].unique():
            inning_balls = match_balls[match_balls["inning"] == inning]

            # Group by over
            for over in sorted(inning_balls["over"].unique()):
                over_balls = inning_balls[inning_balls["over"] == over]

                momentum.append(
                    {
                        "inning": inning,
                        "over": over,
                        "runs": over_balls["runs_total"].sum(),
                        "wickets": over_balls["wicket_kind"].notna().sum(),
                        "cumulative_runs": inning_balls[
                            inning_balls["over"] <= over
                        ]["runs_total"].sum(),
                        "cumulative_wickets": inning_balls[
                            inning_balls["over"] <= over
                        ]["wicket_kind"]
                        .notna()
                        .sum(),
                        "run_rate": over_balls["runs_total"].sum(),
                    }
                )

        return pd.DataFrame(momentum)

    def head_to_head_batting(self, player1: str, player2: str) -> Dict:
        """
        Compare two batsmen head-to-head

        Args:
            player1: First player name
            player2: Second player name

        Returns:
            Dictionary with comparison stats
        """
        p1_stats = self.batting[self.batting["player"] == player1].iloc[0].to_dict()
        p2_stats = self.batting[self.batting["player"] == player2].iloc[0].to_dict()

        return {
            "player1": {"name": player1, **p1_stats},
            "player2": {"name": player2, **p2_stats},
            "winner": {
                "runs": player1 if p1_stats["runs"] > p2_stats["runs"] else player2,
                "average": (
                    player1 if p1_stats["average"] > p2_stats["average"] else player2
                ),
                "strike_rate": (
                    player1
                    if p1_stats["strike_rate"] > p2_stats["strike_rate"]
                    else player2
                ),
                "boundaries": (
                    player1
                    if (p1_stats["fours"] + p1_stats["sixes"])
                    > (p2_stats["fours"] + p2_stats["sixes"])
                    else player2
                ),
            },
        }

    def get_key_insights(self) -> List[Dict]:
        """
        Extract key insights and stories from the data

        Returns:
            List of insight dictionaries
        """
        insights = []

        # Top partnership
        partnerships = self.analyze_partnerships(min_runs=50)
        if len(partnerships) > 0:
            top_partnership = partnerships.iloc[0]
            insights.append(
                {
                    "type": "partnership",
                    "title": "Biggest Partnership",
                    "description": f"{top_partnership['batsmen']} put on {top_partnership['runs']} runs in {top_partnership['balls']} balls",
                    "value": int(top_partnership["runs"]),
                    "metric": "runs",
                }
            )

        # Death overs specialist
        phase_stats = self.analyze_match_phases()
        death_stats = phase_stats[phase_stats["phase"] == "Death"]
        if len(death_stats) > 0:
            avg_death_rr = death_stats["run_rate"].mean()
            insights.append(
                {
                    "type": "phase",
                    "title": "Death Overs Intensity",
                    "description": f"Average run rate in death overs (16-20): {avg_death_rr:.2f}",
                    "value": round(avg_death_rr, 2),
                    "metric": "run_rate",
                }
            )

        # Most consistent batsman (low std deviation)
        if "average" in self.batting.columns:
            high_scorers = self.batting[self.batting["runs"] > 200]
            if len(high_scorers) > 0:
                # Calculate consistency (runs per match)
                consistent = high_scorers.nsmallest(1, "average")
                if len(consistent) > 0:
                    player = consistent.iloc[0]
                    insights.append(
                        {
                            "type": "player",
                            "title": "Consistent Performer",
                            "description": f"{player['player']} averaged {player['average']:.1f} runs across {player['matches']} matches",
                            "value": round(player["average"], 1),
                            "metric": "average",
                        }
                    )

        # Best economy in death overs
        if len(death_stats) > 0 and "run_rate" in death_stats.columns:
            best_death = death_stats.nsmallest(5, "run_rate")
            if len(best_death) > 0:
                avg_best = best_death["run_rate"].mean()
                insights.append(
                    {
                        "type": "bowling",
                        "title": "Death Bowling Excellence",
                        "description": f"Best death overs economy: {avg_best:.2f} runs per over",
                        "value": round(avg_best, 2),
                        "metric": "economy",
                    }
                )

        # Powerplay domination
        pp_stats = phase_stats[phase_stats["phase"] == "Powerplay"]
        if len(pp_stats) > 0:
            avg_pp_rr = pp_stats["run_rate"].mean()
            avg_pp_wickets = pp_stats["wickets"].mean()
            insights.append(
                {
                    "type": "phase",
                    "title": "Powerplay Stats",
                    "description": f"Average RR: {avg_pp_rr:.2f}, Wickets/innings: {avg_pp_wickets:.2f}",
                    "value": round(avg_pp_rr, 2),
                    "metric": "run_rate",
                }
            )

        return insights


def load_analytics_data(data_dir: str = "data/processed"):
    """
    Load data and create AdvancedAnalytics instance

    Args:
        data_dir: Directory containing processed data

    Returns:
        AdvancedAnalytics instance or None if data not found
    """
    data_path = Path(data_dir)

    try:
        deliveries = pd.read_csv(data_path / "all_deliveries.csv")
        matches = pd.read_csv(data_path / "match_summaries.csv")
        batting = pd.read_csv(data_path / "player_batting_stats.csv")
        bowling = pd.read_csv(data_path / "player_bowling_stats.csv")

        return AdvancedAnalytics(deliveries, matches, batting, bowling)

    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print("Make sure you've run the data processing pipeline first.")
        return None


if __name__ == "__main__":
    # Example usage
    analytics = load_analytics_data()

    if analytics:
        print("🏏 Advanced Cricket Analytics\n")

        # Partnerships
        print("=" * 60)
        print("TOP PARTNERSHIPS")
        print("=" * 60)
        partnerships = analytics.analyze_partnerships(min_runs=50)
        print(partnerships.head(10))

        # Phase analysis
        print("\n" + "=" * 60)
        print("PHASE ANALYSIS")
        print("=" * 60)
        phase_stats = analytics.analyze_match_phases()
        print(phase_stats.groupby("phase").agg({"runs": "mean", "run_rate": "mean"}))

        # Key insights
        print("\n" + "=" * 60)
        print("KEY INSIGHTS")
        print("=" * 60)
        insights = analytics.get_key_insights()
        for insight in insights:
            print(f"\n{insight['title']}")
            print(f"  → {insight['description']}")
