"""
Cricket Analytics - Storytelling Dashboard
Interactive data-driven narratives about T20 cricket

Run: streamlit run dashboard/storytelling_app.py
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

# Page configuration
st.set_page_config(
    page_title="Cricket Stories - T20 Analytics",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for storytelling feel
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&family=Inter:wght@300;400;600&display=swap');

    .main {
        padding: 2rem 3rem;
        background-color: #fafafa;
    }
    .story-title {
        font-family: 'Merriweather', serif;
        font-size: 3rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    .story-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: #64748b;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .insight-number {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
    }
    .insight-label {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .narrative-text {
        font-family: 'Merriweather', serif;
        font-size: 1.15rem;
        line-height: 1.8;
        color: #334155;
        margin: 1.5rem 0;
    }
    .quote-box {
        border-left: 4px solid #667eea;
        padding-left: 1.5rem;
        margin: 2rem 0;
        font-style: italic;
        color: #475569;
    }
    .stat-highlight {
        display: inline-block;
        background-color: #fef3c7;
        padding: 0.2rem 0.6rem;
        border-radius: 0.3rem;
        font-weight: 600;
        color: #92400e;
    }
    .chapter-divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #cbd5e1, transparent);
        margin: 3rem 0;
    }
    .stMetric {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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


@st.cache_resource
def get_analytics(_batting, _bowling, _deliveries, _matches):
    """Create analytics instance"""
    return AdvancedAnalytics(_deliveries, _matches, _batting, _bowling)


def render_story_header():
    """Render the main header"""
    st.markdown(
        """
        <div class="story-title">
            📖 The Story of T20 Cricket
        </div>
        <div class="story-subtitle">
            A data-driven journey through the most explosive format of cricket
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_card(value, label, icon="📊"):
    """Render an insight card"""
    st.markdown(
        f"""
        <div class="insight-box">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div class="insight-number">{value}</div>
            <div class="insight-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def story_chapter_1(batting, bowling, deliveries, matches, analytics):
    """Chapter 1: The Numbers That Define T20"""
    st.markdown('<div class="chapter-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        ## Chapter 1: By The Numbers
        ### The Statistical Landscape of T20 Cricket
        """,
        unsafe_allow_html=False,
    )

    # Create insight cards
    col1, col2, col3 = st.columns(3)

    with col1:
        total_runs = deliveries["runs_total"].sum()
        render_insight_card(f"{total_runs:,}", "Total Runs Scored", "🏏")

    with col2:
        total_wickets = bowling["wickets"].sum()
        render_insight_card(f"{total_wickets:,}", "Wickets Fallen", "🎯")

    with col3:
        total_balls = len(deliveries)
        render_insight_card(f"{total_balls:,}", "Balls Bowled", "⚾")

    st.markdown(
        f"""
        <div class="narrative-text">
        In the high-octane world of T20 cricket, every ball tells a story. Across {len(matches)}
        matches spanning multiple World Cups, we've witnessed <span class="stat-highlight">{total_runs:,} runs</span>
        scored at an average of <span class="stat-highlight">{total_runs/len(matches):.0f} runs per match</span>.

        The format demands aggression, and the numbers don't lie—batsmen have smashed boundaries at will while
        bowlers have fought back with {total_wickets:,} wickets, making every delivery a battle of wits and skill.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Runs distribution over time
    st.subheader("📈 The Evolution of Scoring")

    match_runs = deliveries.groupby("match_id")["runs_total"].sum().reset_index()
    match_runs["match_num"] = range(1, len(match_runs) + 1)

    fig = px.scatter(
        match_runs,
        x="match_num",
        y="runs_total",
        trendline="lowess",
        title="Match Scores Across Tournaments",
        labels={"match_num": "Match Number", "runs_total": "Total Runs"},
        template="plotly_white",
    )
    fig.update_traces(marker=dict(size=8, color="#667eea", opacity=0.6))
    st.plotly_chart(fig, use_container_width=True)


def story_chapter_2(batting, bowling, deliveries, matches, analytics):
    """Chapter 2: Legends of the Game"""
    st.markdown('<div class="chapter-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
        ## Chapter 2: The Legends
        ### Players Who Defined an Era
        """)

    # Top batsmen
    top_batsmen = batting.nlargest(10, "runs")

    st.markdown(
        """
        <div class="narrative-text">
        Behind every great tournament are the players who rise to the occasion. These are the batsmen
        who have turned matches on their head, whose names echo in cricket stadiums worldwide.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Interactive batsman chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=top_batsmen["player"],
            y=top_batsmen["runs"],
            name="Total Runs",
            marker_color="#667eea",
            text=top_batsmen["runs"],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Top Run Scorers - The Heavyweights",
        xaxis_title="Player",
        yaxis_title="Runs",
        template="plotly_white",
        height=500,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Spotlight on top scorer
    if len(top_batsmen) > 0:
        champion = top_batsmen.iloc[0]

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(
                f"""
                <div class="insight-box">
                    <div style="font-size: 1.5rem; margin-bottom: 1rem;">👑 Leading Run Scorer</div>
                    <div class="insight-number">{champion['player']}</div>
                    <div class="insight-label">{int(champion['runs'])} runs across {int(champion['matches'])} matches</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="narrative-text">
                <strong>{champion['player']}</strong> stands tall as the tournament's run machine.
                With an average of <span class="stat-highlight">{champion['average']:.2f}</span> and
                a strike rate of <span class="stat-highlight">{champion['strike_rate']:.2f}</span>,
                this player has been the cornerstone of their team's batting lineup.

                Across {int(champion['matches'])} matches, they've smashed
                <span class="stat-highlight">{int(champion['fours'])} fours</span> and
                <span class="stat-highlight">{int(champion['sixes'])} sixes</span>,
                entertaining millions with their aggressive yet calculated approach.
                </div>
                """,
                unsafe_allow_html=True,
            )


def story_chapter_3(batting, bowling, deliveries, matches, analytics):
    """Chapter 3: The Battle: Bat vs Ball"""
    st.markdown('<div class="chapter-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
        ## Chapter 3: The Eternal Battle
        ### Bat vs Ball: Who Wins in T20?
        """)

    # Get phase analysis
    phase_stats = analytics.analyze_match_phases()
    phase_summary = phase_stats.groupby("phase").agg(
        {
            "runs": "mean",
            "wickets": "mean",
            "run_rate": "mean",
            "boundary_pct": "mean",
        }
    )

    st.markdown(
        """
        <div class="narrative-text">
        T20 cricket is a game of phases. From the explosive powerplay to the calculated middle overs,
        and finally the death overs chaos—each phase has its own narrative.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Phase comparison chart
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Run Rate by Phase", "Wickets by Phase", "Runs by Phase", "Boundary %"),
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]],
    )

    phases_order = ["Powerplay", "Middle", "Death"]

    # Run rate
    fig.add_trace(
        go.Bar(
            x=phases_order,
            y=[phase_summary.loc[p, "run_rate"] for p in phases_order],
            marker_color=["#22c55e", "#eab308", "#ef4444"],
            name="Run Rate",
        ),
        row=1,
        col=1,
    )

    # Wickets
    fig.add_trace(
        go.Bar(
            x=phases_order,
            y=[phase_summary.loc[p, "wickets"] for p in phases_order],
            marker_color=["#22c55e", "#eab308", "#ef4444"],
            name="Wickets",
        ),
        row=1,
        col=2,
    )

    # Runs
    fig.add_trace(
        go.Bar(
            x=phases_order,
            y=[phase_summary.loc[p, "runs"] for p in phases_order],
            marker_color=["#22c55e", "#eab308", "#ef4444"],
            name="Runs",
        ),
        row=2,
        col=1,
    )

    # Boundary %
    fig.add_trace(
        go.Bar(
            x=phases_order,
            y=[phase_summary.loc[p, "boundary_pct"] for p in phases_order],
            marker_color=["#22c55e", "#eab308", "#ef4444"],
            name="Boundary %",
        ),
        row=2,
        col=2,
    )

    fig.update_layout(height=700, showlegend=False, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # Insights from phases
    pp_rr = phase_summary.loc["Powerplay", "run_rate"]
    death_rr = phase_summary.loc["Death", "run_rate"]

    st.markdown(
        f"""
        <div class="quote-box">
        "The powerplay sets the tone at <strong>{pp_rr:.2f} runs per over</strong>, but it's the
        death overs where matches are won and lost, with the run rate skyrocketing to
        <strong>{death_rr:.2f} runs per over</strong>—a difference that can change the course of history."
        </div>
        """,
        unsafe_allow_html=True,
    )


def story_chapter_4(batting, bowling, deliveries, matches, analytics):
    """Chapter 4: Partnerships That Made History"""
    st.markdown('<div class="chapter-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
        ## Chapter 4: Partnerships
        ### When Two Become Greater Than the Sum
        """)

    # Get partnerships
    partnerships = analytics.analyze_partnerships(min_runs=40)

    if len(partnerships) > 0:
        st.markdown(
            """
            <div class="narrative-text">
            Cricket is not an individual sport. While stars shine, it's the partnerships that build
            match-winning totals. Here are the stands that left spectators in awe.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Top 10 partnerships
        top_partnerships = partnerships.head(10)

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=top_partnerships["batsmen"],
                x=top_partnerships["runs"],
                orientation="h",
                marker=dict(
                    color=top_partnerships["run_rate"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Run Rate"),
                ),
                text=top_partnerships["runs"],
                textposition="outside",
            )
        )

        fig.update_layout(
            title="Biggest Partnerships - Building Blocks of Victory",
            xaxis_title="Partnership Runs",
            yaxis_title="",
            template="plotly_white",
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Highlight top partnership
        top = partnerships.iloc[0]
        st.markdown(
            f"""
            <div class="insight-box">
                <div style="font-size: 1.3rem; margin-bottom: 1rem;">🤝 Biggest Partnership</div>
                <div class="insight-number">{int(top['runs'])} runs</div>
                <div class="insight-label">{top['batsmen']}</div>
                <div class="insight-label" style="margin-top: 1rem;">
                    {int(top['balls'])} balls • Run rate: {top['run_rate']:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def story_chapter_5(batting, bowling, deliveries, matches, analytics):
    """Chapter 5: The Deciding Factors"""
    st.markdown('<div class="chapter-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
        ## Chapter 5: What Wins Matches?
        ### Dissecting the Anatomy of Victory
        """)

    # Toss analysis
    matches_clean = matches[matches["outcome_winner"].notna()]
    toss_wins = matches_clean[matches_clean["toss_winner"] == matches_clean["outcome_winner"]]
    toss_pct = len(toss_wins) / len(matches_clean) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        render_insight_card(f"{toss_pct:.1f}%", "Toss Winners Who Won", "🪙")

    with col2:
        bat_first = matches_clean[matches_clean["toss_decision"] == "bat"]
        bat_first_wins = bat_first[bat_first["toss_winner"] == bat_first["outcome_winner"]]
        bat_first_pct = len(bat_first_wins) / len(bat_first) * 100 if len(bat_first) > 0 else 0
        render_insight_card(f"{bat_first_pct:.1f}%", "Bat First Win %", "🏏")

    with col3:
        field_first = matches_clean[matches_clean["toss_decision"] == "field"]
        field_first_wins = field_first[field_first["toss_winner"] == field_first["outcome_winner"]]
        field_first_pct = (
            len(field_first_wins) / len(field_first) * 100 if len(field_first) > 0 else 0
        )
        render_insight_card(f"{field_first_pct:.1f}%", "Field First Win %", "⚾")

    st.markdown(
        f"""
        <div class="narrative-text">
        The toss—a simple coin flip that can change everything. In T20 cricket, winning the toss
        translates to a <span class="stat-highlight">{toss_pct:.1f}%</span> chance of winning the match.

        But what do teams choose? The data reveals fascinating insights: teams prefer to
        field first, believing in the power of chasing targets. The pressure of setting a score
        versus the clarity of chasing one—each strategy with its own merits.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Toss decision distribution
    toss_decision_counts = matches_clean["toss_decision"].value_counts()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=toss_decision_counts.index,
                values=toss_decision_counts.values,
                hole=0.4,
                marker_colors=["#667eea", "#764ba2"],
            )
        ]
    )

    fig.update_layout(
        title="Toss Decision: What Do Captains Choose?",
        template="plotly_white",
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main app"""
    # Load data
    batting, bowling, deliveries, matches = load_data()

    if batting is None:
        st.error("""
            ❌ **No data found!**

            Please run the E2E pipeline first:
            ```
            docker-compose up --build
            ```

            Or manually:
            ```
            python scripts/init_pipeline.py
            ```
            """)
        return

    # Create analytics
    analytics = get_analytics(batting, bowling, deliveries, matches)

    # Render header
    render_story_header()

    # Sidebar navigation
    st.sidebar.title("📚 Chapters")
    chapter = st.sidebar.radio(
        "Navigate the story:",
        [
            "All Chapters",
            "Chapter 1: By The Numbers",
            "Chapter 2: The Legends",
            "Chapter 3: The Battle",
            "Chapter 4: Partnerships",
            "Chapter 5: What Wins?",
        ],
    )

    # Render chapters
    if chapter == "All Chapters" or chapter == "Chapter 1: By The Numbers":
        story_chapter_1(batting, bowling, deliveries, matches, analytics)

    if chapter == "All Chapters" or chapter == "Chapter 2: The Legends":
        story_chapter_2(batting, bowling, deliveries, matches, analytics)

    if chapter == "All Chapters" or chapter == "Chapter 3: The Battle":
        story_chapter_3(batting, bowling, deliveries, matches, analytics)

    if chapter == "All Chapters" or chapter == "Chapter 4: Partnerships":
        story_chapter_4(batting, bowling, deliveries, matches, analytics)

    if chapter == "All Chapters" or chapter == "Chapter 5: What Wins?":
        story_chapter_5(batting, bowling, deliveries, matches, analytics)

    # Footer
    st.markdown('<div class="chapter-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; margin-top: 3rem;">
            <p>📊 Data from Cricsheet.org • Built with Streamlit & Plotly</p>
            <p>🏏 Cricket Analytics Project by Aalap Desai</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
