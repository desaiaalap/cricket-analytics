"""
Cricket Analytics - Interactive Dashboard
Built with Streamlit

Run: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Page configuration
st.set_page_config(
    page_title="Cricket Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    """Load processed cricket data"""
    data_dir = Path("data/processed")

    if not data_dir.exists():
        return None, None, None, None

    try:
        batting = pd.read_csv(data_dir / "player_batting_stats.csv")
        bowling = pd.read_csv(data_dir / "player_bowling_stats.csv")
        deliveries = pd.read_csv(data_dir / "all_deliveries.csv")
        matches = pd.read_csv(data_dir / "match_summaries.csv")

        return batting, bowling, deliveries, matches
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None


def show_overview(batting, bowling, deliveries, matches):
    """Display overview statistics"""
    st.header("📊 Tournament Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Matches", len(matches))
    with col2:
        st.metric("Total Deliveries", f"{len(deliveries):,}")
    with col3:
        st.metric("Unique Batsmen", len(batting))
    with col4:
        st.metric("Unique Bowlers", len(bowling))

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric("Total Runs", f"{batting['runs'].sum():,}")
    with col6:
        st.metric("Total Wickets", f"{bowling['wickets'].sum():,}")
    with col7:
        avg_runs = deliveries["runs_total"].sum() / len(matches)
        st.metric("Avg Runs/Match", f"{avg_runs:.0f}")
    with col8:
        # Toss impact
        matches_with_outcome = matches[matches["outcome_winner"].notna()]
        toss_win = matches_with_outcome[
            matches_with_outcome["toss_winner"] == matches_with_outcome["outcome_winner"]
        ]
        toss_pct = len(toss_win) / len(matches_with_outcome) * 100
        st.metric("Toss Win %", f"{toss_pct:.1f}%")


def show_batting_analysis(batting):
    """Display batting analysis"""
    st.header("🏏 Batting Analysis")

    # Top performers
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Run Scorers")
        top_scorers = batting.nlargest(10, "runs")[
            ["player", "runs", "average", "strike_rate", "matches"]
        ]
        st.dataframe(top_scorers, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Top Run Scorers (Chart)")
        fig = px.bar(
            top_scorers,
            x="runs",
            y="player",
            orientation="h",
            title="Top 10 Run Scorers",
            labels={"runs": "Runs", "player": "Player"},
            color="strike_rate",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Strike rate vs Average
    st.subheader("Strike Rate vs Average (Min 100 runs)")

    qualified = batting[batting["runs"] >= 100].copy()

    fig = px.scatter(
        qualified,
        x="average",
        y="strike_rate",
        size="runs",
        hover_data=["player", "matches"],
        title="Strike Rate vs Average for Qualified Batsmen",
        labels={"average": "Average", "strike_rate": "Strike Rate", "runs": "Total Runs"},
        color="runs",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_bowling_analysis(bowling):
    """Display bowling analysis"""
    st.header("⚾ Bowling Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Wicket Takers")
        top_bowlers = bowling.nlargest(10, "wickets")[
            ["player", "wickets", "economy", "average", "matches"]
        ]
        st.dataframe(top_bowlers, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Top Wicket Takers (Chart)")
        fig = px.bar(
            top_bowlers,
            x="wickets",
            y="player",
            orientation="h",
            title="Top 10 Wicket Takers",
            labels={"wickets": "Wickets", "player": "Player"},
            color="economy",
            color_continuous_scale="RdYlGn_r",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Economy vs Average
    st.subheader("Economy vs Average (Min 10 wickets)")

    qualified = bowling[bowling["wickets"] >= 10].copy()

    fig = px.scatter(
        qualified,
        x="average",
        y="economy",
        size="wickets",
        hover_data=["player", "matches"],
        title="Economy vs Average for Qualified Bowlers",
        labels={"average": "Average", "economy": "Economy", "wickets": "Wickets"},
        color="wickets",
        color_continuous_scale="Reds",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_match_insights(matches):
    """Display match insights"""
    st.header("🎯 Match Insights")

    # Toss decision analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Toss Decision Distribution")
        toss_decisions = matches["toss_decision"].value_counts()
        fig = px.pie(
            values=toss_decisions.values,
            names=toss_decisions.index,
            title="Bat vs Field First",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Toss Impact on Match Outcome")
        matches_with_outcome = matches[matches["outcome_winner"].notna()].copy()
        matches_with_outcome["toss_won_match"] = (
            matches_with_outcome["toss_winner"] == matches_with_outcome["outcome_winner"]
        )

        toss_impact = matches_with_outcome["toss_won_match"].value_counts()
        fig = px.pie(
            values=toss_impact.values,
            names=["Toss Winner Won", "Toss Loser Won"],
            title="Did Toss Winner Win Match?",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Matches by venue
    st.subheader("Matches by Venue")
    venue_counts = matches["venue"].value_counts().head(10)
    fig = px.bar(
        x=venue_counts.values,
        y=venue_counts.index,
        orientation="h",
        title="Top 10 Venues by Match Count",
        labels={"x": "Number of Matches", "y": "Venue"},
    )
    st.plotly_chart(fig, use_container_width=True)


def show_player_comparison(batting, bowling):
    """Show player comparison tool"""
    st.header("🔍 Player Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Compare Batsmen")
        selected_batsmen = st.multiselect(
            "Select batsmen (max 5)",
            options=batting.nlargest(50, "runs")["player"].tolist(),
            max_selections=5,
        )

        if selected_batsmen:
            comparison = batting[batting["player"].isin(selected_batsmen)][
                ["player", "runs", "average", "strike_rate", "fours", "sixes", "matches"]
            ]
            st.dataframe(comparison, use_container_width=True, hide_index=True)

            # Radar chart
            metrics = ["runs", "average", "strike_rate"]
            fig = go.Figure()

            for player in selected_batsmen:
                player_data = batting[batting["player"] == player].iloc[0]
                values = [
                    player_data["runs"] / batting["runs"].max(),
                    player_data["average"] / batting["average"].max(),
                    player_data["strike_rate"] / batting["strike_rate"].max(),
                ]
                fig.add_trace(
                    go.Scatterpolar(
                        r=values + [values[0]],
                        theta=metrics + [metrics[0]],
                        fill="toself",
                        name=player,
                    )
                )

            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Compare Bowlers")
        selected_bowlers = st.multiselect(
            "Select bowlers (max 5)",
            options=bowling.nlargest(50, "wickets")["player"].tolist(),
            max_selections=5,
        )

        if selected_bowlers:
            comparison = bowling[bowling["player"].isin(selected_bowlers)][
                ["player", "wickets", "economy", "average", "strike_rate", "matches"]
            ]
            st.dataframe(comparison, use_container_width=True, hide_index=True)


def main():
    """Main dashboard function"""

    # Title and description
    st.title("🏏 Cricket Analytics Dashboard")
    st.markdown("### T20 World Cup Analysis (2014-2024)")

    # Load data
    with st.spinner("Loading data..."):
        batting, bowling, deliveries, matches = load_data()

    if batting is None:
        st.error("""
            ⚠️ **Data not found!**

            Please run the data processing first:
            ```
            python scripts/process_all_matches.py
            ```

            Or if using Docker:
            ```
            docker-compose --profile process up processor
            ```
            """)
        st.stop()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Overview", "Batting Analysis", "Bowling Analysis", "Match Insights", "Player Comparison"],
    )

    # Filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filters")

    min_matches = st.sidebar.slider("Minimum Matches Played", 1, 30, 1)

    # Apply filters
    batting_filtered = batting[batting["matches"] >= min_matches].copy()
    bowling_filtered = bowling[bowling["matches"] >= min_matches].copy()

    # Show selected page
    if page == "Overview":
        show_overview(batting, bowling, deliveries, matches)
    elif page == "Batting Analysis":
        show_batting_analysis(batting_filtered)
    elif page == "Bowling Analysis":
        show_bowling_analysis(bowling_filtered)
    elif page == "Match Insights":
        show_match_insights(matches)
    elif page == "Player Comparison":
        show_player_comparison(batting, bowling)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
        **Cricket Analytics Dashboard**

        Data Source: [Cricsheet.org](https://cricsheet.org/)

        Built with Streamlit & Plotly
        """)


if __name__ == "__main__":
    main()
