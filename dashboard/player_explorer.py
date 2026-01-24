"""
Player Explorer - Interactive Player Analysis Dashboard
Deep dive into individual player performance

Run: streamlit run dashboard/player_explorer.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from advanced_analytics import AdvancedAnalytics

st.set_page_config(
    page_title="Player Explorer",
    page_icon="🎮",
    layout="wide",
)

st.markdown(
    """
    <style>
    .player-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    .stat-item {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    </style>
    """,
    unsafe_allow_html=True,
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


def render_batsman_profile(player_name, batting, deliveries, analytics):
    """Render detailed batsman profile"""

    player_data = batting[batting["player"] == player_name].iloc[0]

    # Player card header
    st.markdown(
        f"""
        <div class="player-card">
            <h1 style="margin: 0;">🏏 {player_name}</h1>
            <h3 style="margin: 0.5rem 0; opacity: 0.9;">Batsman Profile</h3>

            <div class="stat-grid">
                <div class="stat-item">
                    <div class="stat-value">{int(player_data['runs'])}</div>
                    <div class="stat-label">Total Runs</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{player_data['average']:.1f}</div>
                    <div class="stat-label">Average</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{player_data['strike_rate']:.1f}</div>
                    <div class="stat-label">Strike Rate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{int(player_data['fours'] + player_data['sixes'])}</div>
                    <div class="stat-label">Boundaries</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{int(player_data['matches'])}</div>
                    <div class="stat-label">Matches</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Performance analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Scoring Pattern")

        # Boundaries breakdown
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=["Fours", "Sixes", "Singles/Twos"],
                y=[
                    player_data["fours"] * 4,
                    player_data["sixes"] * 6,
                    player_data["runs"] - (player_data["fours"] * 4 + player_data["sixes"] * 6),
                ],
                marker_color=["#22c55e", "#ef4444", "#3b82f6"],
            )
        )

        fig.update_layout(
            title="Runs Distribution",
            yaxis_title="Runs",
            template="plotly_white",
            height=350,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Efficiency Metrics")

        # Boundaries per match
        boundaries_per_match = (player_data["fours"] + player_data["sixes"]) / player_data[
            "matches"
        ]
        runs_per_match = player_data["runs"] / player_data["matches"]

        metrics_data = pd.DataFrame(
            {
                "Metric": ["Boundaries/Match", "Runs/Match", "Balls/Match"],
                "Value": [
                    boundaries_per_match,
                    runs_per_match,
                    player_data["balls"] / player_data["matches"],
                ],
            }
        )

        fig = px.bar(
            metrics_data,
            x="Metric",
            y="Value",
            text="Value",
            color="Value",
            color_continuous_scale="Viridis",
        )

        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig.update_layout(
            title="Per Match Averages", template="plotly_white", height=350, showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    # Match-by-match form
    player_balls = deliveries[deliveries["batter"] == player_name]

    if len(player_balls) > 0:
        st.subheader("📈 Match-by-Match Form")

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
        form_df["match_num"] = range(1, len(form_df) + 1)

        # Create dual axis chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                x=form_df["match_num"],
                y=form_df["runs"],
                name="Runs",
                marker_color="#667eea",
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=form_df["match_num"],
                y=form_df["strike_rate"],
                name="Strike Rate",
                marker_color="#ef4444",
                line=dict(width=3),
            ),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="Match Number")
        fig.update_yaxes(title_text="Runs", secondary_y=False)
        fig.update_yaxes(title_text="Strike Rate", secondary_y=True)

        fig.update_layout(title="Performance Across Matches", template="plotly_white", height=400)

        st.plotly_chart(fig, use_container_width=True)

        # Show detailed table
        with st.expander("📋 Detailed Match Statistics"):
            st.dataframe(
                form_df[["match_num", "runs", "balls", "fours", "sixes", "strike_rate"]],
                use_container_width=True,
            )


def render_bowler_profile(player_name, bowling, deliveries, analytics):
    """Render detailed bowler profile"""

    player_data = bowling[bowling["player"] == player_name].iloc[0]

    # Player card header
    st.markdown(
        f"""
        <div class="player-card">
            <h1 style="margin: 0;">⚾ {player_name}</h1>
            <h3 style="margin: 0.5rem 0; opacity: 0.9;">Bowler Profile</h3>

            <div class="stat-grid">
                <div class="stat-item">
                    <div class="stat-value">{int(player_data['wickets'])}</div>
                    <div class="stat-label">Wickets</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{player_data['economy']:.2f}</div>
                    <div class="stat-label">Economy</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{player_data['average']:.1f}</div>
                    <div class="stat-label">Average</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{player_data['strike_rate']:.1f}</div>
                    <div class="stat-label">Strike Rate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{int(player_data['matches'])}</div>
                    <div class="stat-label">Matches</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Bowling Efficiency")

        # Economy vs Wickets
        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=player_data["economy"],
                title={"text": "Economy Rate"},
                gauge={
                    "axis": {"range": [None, 12]},
                    "bar": {"color": "#667eea"},
                    "steps": [
                        {"range": [0, 6], "color": "#86efac"},
                        {"range": [6, 9], "color": "#fde047"},
                        {"range": [9, 12], "color": "#fca5a5"},
                    ],
                },
            )
        )

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📊 Performance Metrics")

        metrics = pd.DataFrame(
            {
                "Metric": ["Wickets", "Overs", "Runs Conceded"],
                "Value": [
                    player_data["wickets"],
                    player_data["overs"],
                    player_data["runs"],
                ],
            }
        )

        fig = px.bar(
            metrics, x="Metric", y="Value", text="Value", color="Metric", template="plotly_white"
        )

        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def player_comparison_tool(batting, bowling):
    """Interactive player comparison"""

    st.header("⚔️ Player Comparison Tool")

    comparison_type = st.radio("Compare:", ["Batsmen", "Bowlers"], horizontal=True)

    if comparison_type == "Batsmen":
        col1, col2 = st.columns(2)

        with col1:
            player1 = st.selectbox(
                "Select Player 1",
                batting.nlargest(50, "runs")["player"].tolist(),
                key="p1",
            )

        with col2:
            player2 = st.selectbox(
                "Select Player 2",
                batting.nlargest(50, "runs")["player"].tolist(),
                key="p2",
            )

        if player1 and player2 and player1 != player2:
            p1_data = batting[batting["player"] == player1].iloc[0]
            p2_data = batting[batting["player"] == player2].iloc[0]

            # Radar chart comparison
            categories = ["Runs", "Average", "Strike Rate", "Fours", "Sixes"]

            # Normalize values for radar chart
            max_runs = max(p1_data["runs"], p2_data["runs"])
            max_avg = max(p1_data["average"], p2_data["average"])
            max_sr = max(p1_data["strike_rate"], p2_data["strike_rate"])
            max_fours = max(p1_data["fours"], p2_data["sixes"])
            max_sixes = max(p1_data["fours"], p2_data["sixes"])

            fig = go.Figure()

            fig.add_trace(
                go.Scatterpolar(
                    r=[
                        p1_data["runs"] / max_runs * 100,
                        p1_data["average"] / max_avg * 100,
                        p1_data["strike_rate"] / max_sr * 100,
                        p1_data["fours"] / max_fours * 100,
                        p1_data["sixes"] / max_sixes * 100,
                    ],
                    theta=categories,
                    fill="toself",
                    name=player1,
                    line_color="#667eea",
                )
            )

            fig.add_trace(
                go.Scatterpolar(
                    r=[
                        p2_data["runs"] / max_runs * 100,
                        p2_data["average"] / max_avg * 100,
                        p2_data["strike_rate"] / max_sr * 100,
                        p2_data["fours"] / max_fours * 100,
                        p2_data["sixes"] / max_sixes * 100,
                    ],
                    theta=categories,
                    fill="toself",
                    name=player2,
                    line_color="#ef4444",
                )
            )

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title="Player Comparison (Normalized)",
                template="plotly_white",
            )

            st.plotly_chart(fig, use_container_width=True)

            # Side-by-side comparison
            comp_col1, comp_col2, comp_col3 = st.columns(3)

            with comp_col1:
                st.metric(player1, "")
                st.metric("Runs", f"{int(p1_data['runs'])}")
                st.metric("Average", f"{p1_data['average']:.1f}")
                st.metric("Strike Rate", f"{p1_data['strike_rate']:.1f}")
                st.metric("Boundaries", f"{int(p1_data['fours'] + p1_data['sixes'])}")

            with comp_col2:
                st.markdown("### VS")

            with comp_col3:
                st.metric(player2, "")
                st.metric("Runs", f"{int(p2_data['runs'])}")
                st.metric("Average", f"{p2_data['average']:.1f}")
                st.metric("Strike Rate", f"{p2_data['strike_rate']:.1f}")
                st.metric("Boundaries", f"{int(p2_data['fours'] + p2_data['sixes'])}")


def main():
    """Main app"""
    st.title("🎮 Player Explorer")
    st.markdown("Deep dive into individual player performance and comparisons")

    # Load data
    batting, bowling, deliveries, matches = load_data()

    if batting is None:
        st.error("Please run the data processing pipeline first!")
        return

    analytics = get_analytics(batting, bowling, deliveries, matches)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏏 Batsman Analysis", "⚾ Bowler Analysis", "⚔️ Compare Players"])

    with tab1:
        selected_batsman = st.selectbox(
            "Select a batsman to analyze:",
            batting.nlargest(100, "runs")["player"].tolist(),
        )

        if selected_batsman:
            render_batsman_profile(selected_batsman, batting, deliveries, analytics)

    with tab2:
        selected_bowler = st.selectbox(
            "Select a bowler to analyze:", bowling.nlargest(100, "wickets")["player"].tolist()
        )

        if selected_bowler:
            render_bowler_profile(selected_bowler, bowling, deliveries, analytics)

    with tab3:
        player_comparison_tool(batting, bowling)


if __name__ == "__main__":
    main()
