"""
Match Viewer - Interactive Match Replay and Analysis
Visualize match momentum, partnerships, and key moments

Run: streamlit run dashboard/match_viewer.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from advanced_analytics import AdvancedAnalytics

st.set_page_config(
    page_title="Match Viewer",
    page_icon="🎬",
    layout="wide",
)


@st.cache_data
def load_data():
    """Load processed cricket data"""
    data_dir = Path("data/processed")

    try:
        batting = pd.read_csv(data_dir / "player_batting_stats.csv")
        bowling = pd.read_csv(data_dir / "player_bowling_stats.csv")
        deliveries = pd.read_csv(data_dir / "all_deliveries.csv")
        matches = pd.read_csv(data_dir / "match_summaries.csv")
        return batting, bowling, deliveries, matches
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None


@st.cache_resource
def get_analytics(_batting, _bowling, _deliveries, _matches):
    """Create analytics instance"""
    return AdvancedAnalytics(_deliveries, _matches, _batting, _bowling)


def render_momentum_chart(match_id, deliveries, matches):
    """Render match momentum chart"""

    match_balls = deliveries[deliveries["match_id"] == match_id]
    match_info = matches[matches["match_id"] == match_id].iloc[0]

    # Get teams
    teams = match_info["teams"] if isinstance(match_info["teams"], list) else []

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Runs Progression", "Wickets Lost"),
        vertical_spacing=0.15,
        row_heights=[0.7, 0.3],
    )

    colors = ["#667eea", "#ef4444"]

    for idx, inning in enumerate(sorted(match_balls["inning"].unique())):
        inning_balls = match_balls[match_balls["inning"] == inning]

        # Calculate cumulative runs and wickets
        runs_progression = []
        wickets_progression = []
        overs = []

        cumulative_runs = 0
        cumulative_wickets = 0

        for ball_num in range(len(inning_balls)):
            ball = inning_balls.iloc[ball_num]
            cumulative_runs += ball["runs_total"]

            if pd.notna(ball.get("wicket_kind")):
                cumulative_wickets += 1

            overs.append(ball["over"] + (ball["ball"] / 6))
            runs_progression.append(cumulative_runs)
            wickets_progression.append(cumulative_wickets)

        team_name = teams[idx] if idx < len(teams) else f"Innings {inning}"

        # Runs progression
        fig.add_trace(
            go.Scatter(
                x=overs,
                y=runs_progression,
                name=team_name,
                mode="lines",
                line=dict(color=colors[idx], width=3),
                fill="tozeroy",
                fillcolor=f"rgba({int(colors[idx][1:3], 16)}, {int(colors[idx][3:5], 16)}, {int(colors[idx][5:7], 16)}, 0.2)",
            ),
            row=1,
            col=1,
        )

        # Wickets
        fig.add_trace(
            go.Scatter(
                x=overs,
                y=wickets_progression,
                name=f"{team_name} Wickets",
                mode="lines+markers",
                line=dict(color=colors[idx], width=2, dash="dot"),
                marker=dict(size=6),
            ),
            row=2,
            col=1,
        )

    fig.update_xaxes(title_text="Overs", row=2, col=1)
    fig.update_yaxes(title_text="Runs", row=1, col=1)
    fig.update_yaxes(title_text="Wickets", row=2, col=1)

    fig.update_layout(height=700, template="plotly_white", showlegend=True, hovermode="x unified")

    return fig


def render_manhattan_chart(match_id, deliveries):
    """Render Manhattan chart (runs per over)"""

    match_balls = deliveries[deliveries["match_id"] == match_id]

    innings_data = []

    for inning in sorted(match_balls["inning"].unique()):
        inning_balls = match_balls[match_balls["inning"] == inning]

        over_runs = inning_balls.groupby("over")["runs_total"].sum().reset_index()

        innings_data.append(
            {
                "inning": inning,
                "data": over_runs,
            }
        )

    fig = go.Figure()

    colors = ["#667eea", "#ef4444"]

    for idx, inning_info in enumerate(innings_data):
        over_runs = inning_info["data"]

        fig.add_trace(
            go.Bar(
                x=over_runs["over"] + 1,  # Overs start from 1
                y=over_runs["runs_total"],
                name=f"Innings {inning_info['inning']}",
                marker_color=colors[idx],
                opacity=0.7 if idx == 0 else 0.9,
            )
        )

    fig.update_layout(
        title="Manhattan Chart - Runs Per Over",
        xaxis_title="Over Number",
        yaxis_title="Runs",
        template="plotly_white",
        barmode="group",
        height=400,
    )

    return fig


def render_worm_chart(match_id, deliveries):
    """Render worm chart (run rate comparison)"""

    match_balls = deliveries[deliveries["match_id"] == match_id]

    fig = go.Figure()
    colors = ["#667eea", "#ef4444"]

    for idx, inning in enumerate(sorted(match_balls["inning"].unique())):
        inning_balls = match_balls[match_balls["inning"] == inning]

        overs = []
        run_rates = []

        for over in sorted(inning_balls["over"].unique()):
            over_balls = inning_balls[inning_balls["over"] <= over]
            balls_faced = len(over_balls)
            runs = over_balls["runs_total"].sum()

            if balls_faced > 0:
                run_rate = (runs / balls_faced) * 6
                overs.append(over + 1)
                run_rates.append(run_rate)

        fig.add_trace(
            go.Scatter(
                x=overs,
                y=run_rates,
                name=f"Innings {inning}",
                mode="lines+markers",
                line=dict(color=colors[idx], width=3),
                marker=dict(size=6),
            )
        )

    fig.update_layout(
        title="Worm Chart - Run Rate Progression",
        xaxis_title="Overs",
        yaxis_title="Run Rate",
        template="plotly_white",
        height=400,
        hovermode="x unified",
    )

    return fig


def render_phase_comparison(match_id, deliveries):
    """Compare performance in different phases"""

    match_balls = deliveries[deliveries["match_id"] == match_id].copy()

    # Add phase
    def get_phase(over):
        if over < 6:
            return "Powerplay"
        elif over < 16:
            return "Middle"
        else:
            return "Death"

    match_balls["phase"] = match_balls["over"].apply(get_phase)

    phase_stats = []

    for inning in match_balls["inning"].unique():
        for phase in ["Powerplay", "Middle", "Death"]:
            phase_balls = match_balls[
                (match_balls["inning"] == inning) & (match_balls["phase"] == phase)
            ]

            if len(phase_balls) > 0:
                phase_stats.append(
                    {
                        "Innings": f"Innings {inning}",
                        "Phase": phase,
                        "Runs": phase_balls["runs_total"].sum(),
                        "Run Rate": phase_balls["runs_total"].sum() / len(phase_balls) * 6,
                        "Wickets": phase_balls["wicket_kind"].notna().sum(),
                    }
                )

    phase_df = pd.DataFrame(phase_stats)

    # Create subplots
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Runs by Phase", "Run Rate by Phase"),
    )

    for inning in phase_df["Innings"].unique():
        inning_data = phase_df[phase_df["Innings"] == inning]

        color = "#667eea" if "1" in inning else "#ef4444"

        fig.add_trace(
            go.Bar(
                x=inning_data["Phase"],
                y=inning_data["Runs"],
                name=inning,
                marker_color=color,
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=inning_data["Phase"],
                y=inning_data["Run Rate"],
                name=inning,
                mode="lines+markers",
                line=dict(color=color, width=3),
                marker=dict(size=10),
            ),
            row=1,
            col=2,
        )

    fig.update_layout(height=400, template="plotly_white", showlegend=True)

    return fig


def render_key_moments(match_id, deliveries):
    """Highlight key moments in the match"""

    match_balls = deliveries[deliveries["match_id"] == match_id]

    st.subheader("🔥 Key Moments")

    # Find sixes
    sixes = match_balls[match_balls["runs_batter"] == 6]

    # Find wickets
    wickets = match_balls[match_balls["wicket_kind"].notna()]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💥 Biggest Hits (Sixes)")
        if len(sixes) > 0:
            six_summary = sixes.groupby("batter").size().sort_values(ascending=False).head(5)

            for player, count in six_summary.items():
                st.markdown(f"- **{player}**: {count} sixes")
        else:
            st.info("No sixes in this match")

    with col2:
        st.markdown("### 🎯 Key Wickets")
        if len(wickets) > 0:
            wicket_summary = wickets.groupby("bowler").size().sort_values(ascending=False).head(5)

            for player, count in wicket_summary.items():
                st.markdown(f"- **{player}**: {count} wickets")
        else:
            st.info("No wickets recorded")

    # Highest scoring overs
    st.markdown("### 🚀 Highest Scoring Overs")

    high_overs = (
        match_balls.groupby(["inning", "over"])["runs_total"]
        .sum()
        .reset_index()
        .sort_values("runs_total", ascending=False)
        .head(5)
    )

    for _, over_data in high_overs.iterrows():
        st.markdown(
            f"- Innings {int(over_data['inning'])}, Over {int(over_data['over']) + 1}: **{int(over_data['runs_total'])} runs**"
        )


def main():
    """Main app"""
    st.title("🎬 Match Viewer & Analyzer")
    st.markdown("Replay matches ball-by-ball and analyze momentum shifts")

    # Load data
    batting, bowling, deliveries, matches = load_data()

    if batting is None:
        st.error("Please run the data processing pipeline first!")
        return

    analytics = get_analytics(batting, bowling, deliveries, matches)

    # Match selector
    match_options = []
    for _, match in matches.iterrows():
        teams = match["teams"] if isinstance(match["teams"], list) else ["Team A", "Team B"]
        match_label = f"{teams[0] if len(teams) > 0 else 'Team1'} vs {teams[1] if len(teams) > 1 else 'Team2'} - {match['city']}"
        match_options.append({"label": match_label, "id": match["match_id"]})

    selected_match_label = st.selectbox(
        "Select a match to analyze:",
        [m["label"] for m in match_options],
    )

    # Get match ID
    selected_match_id = next(
        (m["id"] for m in match_options if m["label"] == selected_match_label), None
    )

    if selected_match_id:
        match_info = matches[matches["match_id"] == selected_match_id].iloc[0]

        # Match header
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Venue", match_info["city"])

        with col2:
            st.metric("Toss Winner", match_info.get("toss_winner", "N/A"))

        with col3:
            winner = match_info.get("outcome_winner", "N/A")
            st.metric("Match Winner", winner if pd.notna(winner) else "N/A")

        st.markdown("---")

        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Momentum", "📈 Manhattan", "🐛 Worm", "🎯 Analysis"])

        with tab1:
            st.plotly_chart(
                render_momentum_chart(selected_match_id, deliveries, matches),
                use_container_width=True,
            )

        with tab2:
            st.plotly_chart(
                render_manhattan_chart(selected_match_id, deliveries),
                use_container_width=True,
            )

        with tab3:
            st.plotly_chart(
                render_worm_chart(selected_match_id, deliveries), use_container_width=True
            )

        with tab4:
            st.plotly_chart(
                render_phase_comparison(selected_match_id, deliveries),
                use_container_width=True,
            )

            render_key_moments(selected_match_id, deliveries)


if __name__ == "__main__":
    main()
