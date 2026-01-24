"""
Cricket Analytics - Home Dashboard
Main entry point with overview and links to specialized dashboards

Run: streamlit run dashboard/home.py
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
    page_title="Cricket Analytics Home",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 1rem 2rem;
    }
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
    }
    .dashboard-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    .dashboard-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .card-description {
        color: #64748b;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
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


def render_hero():
    """Render hero section"""
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-title">🏏 Cricket Analytics Platform</div>
            <div class="hero-subtitle">
                Comprehensive T20 World Cup Analysis • Interactive Visualizations • Data-Driven Insights
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_stats(batting, bowling, deliveries, matches):
    """Render quick statistics"""
    st.markdown("## 📊 At a Glance")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{len(matches)}</div>
                <div class="stat-label">Matches</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{len(deliveries):,}</div>
                <div class="stat-label">Deliveries</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        total_runs = deliveries["runs_total"].sum()
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{total_runs:,}</div>
                <div class="stat-label">Total Runs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{len(batting)}</div>
                <div class="stat-label">Batsmen</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{len(bowling)}</div>
                <div class="stat-label">Bowlers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_dashboard_links():
    """Render links to specialized dashboards"""
    st.markdown("## 🎯 Explore Dashboards")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-title">📖 Storytelling Dashboard</div>
                <div class="card-description">
                    Experience the data as a narrative journey through T20 cricket.
                    Explore chapters covering legends, battles, partnerships, and winning factors.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Run:** `streamlit run dashboard/storytelling_app.py`")

        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-title">🎬 Match Viewer</div>
                <div class="card-description">
                    Replay matches ball-by-ball with momentum charts, Manhattan graphs,
                    worm charts, and phase analysis. Relive the action!
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Run:** `streamlit run dashboard/match_viewer.py`")

    with col2:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-title">🎮 Player Explorer</div>
                <div class="card-description">
                    Deep dive into individual player stats, performance trends,
                    and head-to-head comparisons. Analyze batting and bowling in detail.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Run:** `streamlit run dashboard/player_explorer.py`")

        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-title">📊 Classic Dashboard</div>
                <div class="card-description">
                    Traditional analytics dashboard with batting analysis, bowling stats,
                    match insights, and comprehensive player comparisons.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Run:** `streamlit run dashboard/app.py`")


def render_top_performers(batting, bowling):
    """Render top performers section"""
    st.markdown("## 🏆 Top Performers")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏏 Leading Run Scorers")

        top_batsmen = batting.nlargest(10, "runs")[["player", "runs", "average", "strike_rate"]]

        fig = px.bar(
            top_batsmen,
            x="runs",
            y="player",
            orientation="h",
            color="strike_rate",
            color_continuous_scale="Viridis",
            text="runs",
            title="Top 10 Run Scorers",
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white", height=450, showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⚾ Leading Wicket Takers")

        top_bowlers = bowling.nlargest(10, "wickets")[["player", "wickets", "economy", "average"]]

        fig = px.bar(
            top_bowlers,
            x="wickets",
            y="player",
            orientation="h",
            color="economy",
            color_continuous_scale="RdYlGn_r",
            text="wickets",
            title="Top 10 Wicket Takers",
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white", height=450, showlegend=False)

        st.plotly_chart(fig, use_container_width=True)


def render_features():
    """Render features section"""
    st.markdown("## ✨ Platform Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 📊 Advanced Analytics
            - Phase-wise analysis (Powerplay, Middle, Death)
            - Partnership tracking
            - Player form trends
            - Match momentum calculation
            """
        )

    with col2:
        st.markdown(
            """
            ### 📈 Interactive Visualizations
            - Plotly-powered charts
            - Real-time filtering
            - Multi-dimensional comparisons
            - Responsive design
            """
        )

    with col3:
        st.markdown(
            """
            ### 🚀 Production Ready
            - Automated data pipeline
            - Docker containerization
            - 37+ automated tests
            - CI/CD with GitHub Actions
            """
        )


def main():
    """Main app"""
    # Load data
    batting, bowling, deliveries, matches = load_data()

    if batting is None:
        st.error(
            """
            ❌ **No data found!**

            Please run the E2E pipeline first:
            ```
            docker-compose up --build
            ```

            Or manually:
            ```
            python scripts/init_pipeline.py
            ```
            """
        )
        return

    # Render sections
    render_hero()
    render_quick_stats(batting, bowling, deliveries, matches)
    render_dashboard_links()
    render_top_performers(batting, bowling)
    render_features()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; margin-top: 2rem;">
            <p>📊 Data from Cricsheet.org • Built with Streamlit & Plotly</p>
            <p>🏏 Cricket Analytics Platform by Aalap Desai</p>
            <p>⚡ Fully automated E2E pipeline • From data acquisition to visualization</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
