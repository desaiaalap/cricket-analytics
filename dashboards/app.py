"""
Cricket Analytics Dashboard - Streamlit Application
Main entry point for the T20 cricket analytics dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from etl.data_loader import CricketDataLoader
from etl.data_processor import DataProcessor
from modeling.match_predictor import MatchPredictor

# Page configuration
st.set_page_config(
    page_title="Cricket Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main dashboard function."""

    # Header
    st.markdown('<h1 class="main-header">🏏 Cricket Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Data-Driven T20 Cricket Analysis")

    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=Cricket", width=150)
        st.title("Navigation")

        page = st.radio(
            "Select Page",
            ["Home", "Match Analysis", "Player Stats", "Predictions", "Team Comparison", "About"]
        )

        st.markdown("---")
        st.subheader("Filters")

        # Tournament filter
        tournament = st.selectbox(
            "Tournament",
            ["All", "IPL", "BBL", "CPL", "PSL", "T20 World Cup"]
        )

        # Season filter
        season = st.selectbox(
            "Season",
            ["2024", "2023", "2022", "2021", "2020"]
        )

    # Route to appropriate page
    if page == "Home":
        show_home()
    elif page == "Match Analysis":
        show_match_analysis()
    elif page == "Player Stats":
        show_player_stats()
    elif page == "Predictions":
        show_predictions()
    elif page == "Team Comparison":
        show_team_comparison()
    elif page == "About":
        show_about()


def show_home():
    """Display home page with overview statistics."""
    st.header("Dashboard Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Matches",
            value="1,234",
            delta="+56 from last season"
        )

    with col2:
        st.metric(
            label="Teams Tracked",
            value="24",
            delta="+2"
        )

    with col3:
        st.metric(
            label="Players Analyzed",
            value="456",
            delta="+89"
        )

    with col4:
        st.metric(
            label="Prediction Accuracy",
            value="78.5%",
            delta="+2.3%"
        )

    st.markdown("---")

    # Two columns for charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Match Outcomes Distribution")
        # Sample data
        outcomes = pd.DataFrame({
            'Result': ['Home Win', 'Away Win', 'No Result'],
            'Count': [450, 420, 30]
        })
        fig = px.pie(outcomes, values='Count', names='Result',
                    color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Scores by Tournament")
        # Sample data
        avg_scores = pd.DataFrame({
            'Tournament': ['IPL', 'BBL', 'CPL', 'PSL', 'T20 WC'],
            'Avg Score': [175, 165, 158, 160, 168]
        })
        fig = px.bar(avg_scores, x='Tournament', y='Avg Score',
                    color='Avg Score', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Recent matches
    st.subheader("Recent Matches")
    st.info("⚠️ Connect CricPy API to display real match data")

    # Sample recent matches data
    recent_matches = pd.DataFrame({
        'Date': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12'],
        'Team 1': ['Mumbai', 'Chennai', 'Bangalore', 'Delhi'],
        'Score 1': ['185/6', '178/8', '195/4', '160/9'],
        'Team 2': ['Delhi', 'Punjab', 'Kolkata', 'Hyderabad'],
        'Score 2': ['182/7', '180/5', '190/7', '165/6'],
        'Winner': ['Mumbai', 'Punjab', 'Bangalore', 'Hyderabad']
    })
    st.dataframe(recent_matches, use_container_width=True)


def show_match_analysis():
    """Display match analysis page."""
    st.header("Match Analysis")

    st.subheader("Select Match")
    col1, col2 = st.columns(2)

    with col1:
        match_id = st.text_input("Match ID", "M12345")

    with col2:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Scoring Patterns", "Wicket Analysis", "Partnership Analysis", "Phase Analysis"]
        )

    if st.button("Analyze Match"):
        st.info("⚠️ Connect CricPy API to load match data")

        # Sample visualization
        st.subheader("Runs by Over")
        overs = list(range(1, 21))
        runs = np.random.randint(4, 18, 20)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=overs, y=runs, mode='lines+markers',
                                name='Runs per Over', line=dict(color='blue', width=3)))
        fig.update_layout(xaxis_title="Over", yaxis_title="Runs",
                         title="Scoring Rate by Over")
        st.plotly_chart(fig, use_container_width=True)


def show_player_stats():
    """Display player statistics page."""
    st.header("Player Statistics")

    col1, col2 = st.columns(2)

    with col1:
        player_name = st.text_input("Player Name", "V. Kohli")

    with col2:
        stat_type = st.selectbox(
            "Stat Type",
            ["Batting", "Bowling", "Fielding", "Overall"]
        )

    if st.button("Get Stats"):
        st.info("⚠️ Connect CricPy API to load player data")

        # Sample player stats
        st.subheader(f"Statistics for {player_name}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Matches", "234")
            st.metric("Runs", "8,456")
        with col2:
            st.metric("Average", "52.4")
            st.metric("Strike Rate", "138.5")
        with col3:
            st.metric("Hundreds", "12")
            st.metric("Fifties", "45")


def show_predictions():
    """Display match prediction page."""
    st.header("Match Outcome Prediction")

    st.subheader("Input Match Details")

    col1, col2 = st.columns(2)

    with col1:
        team1 = st.text_input("Team 1", "Mumbai Indians")
        team1_form = st.slider("Team 1 Recent Form (wins in last 5)", 0, 5, 3)

    with col2:
        team2 = st.text_input("Team 2", "Chennai Super Kings")
        team2_form = st.slider("Team 2 Recent Form (wins in last 5)", 0, 5, 3)

    venue = st.text_input("Venue", "Wankhede Stadium")
    toss_winner = st.selectbox("Toss Winner", [team1, team2])
    toss_decision = st.selectbox("Toss Decision", ["Bat First", "Bowl First"])

    if st.button("Predict Match Outcome"):
        st.info("⚠️ Load trained model to make predictions")

        # Placeholder prediction
        with st.spinner("Running prediction models..."):
            import time
            time.sleep(1)

            st.success("Prediction Complete!")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Predicted Winner")
                st.markdown(f"### 🏆 {team1}")
                st.markdown("**Win Probability: 68.5%**")

            with col2:
                st.subheader("Confidence Breakdown")
                model_scores = pd.DataFrame({
                    'Model': ['Random Forest', 'XGBoost', 'LightGBM', 'Neural Net'],
                    'Confidence': [72, 68, 65, 69]
                })
                fig = px.bar(model_scores, x='Model', y='Confidence',
                           color='Confidence', color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)


def show_team_comparison():
    """Display team comparison page."""
    st.header("Team Comparison")

    col1, col2 = st.columns(2)

    with col1:
        team_a = st.selectbox("Team A", ["Mumbai", "Chennai", "Bangalore", "Delhi"])

    with col2:
        team_b = st.selectbox("Team B", ["Chennai", "Mumbai", "Kolkata", "Punjab"])

    if st.button("Compare Teams"):
        st.subheader(f"{team_a} vs {team_b}")

        # Sample comparison data
        comparison = pd.DataFrame({
            'Metric': ['Matches Played', 'Wins', 'Avg Score', 'Win %', 'H2H Wins'],
            team_a: [150, 95, 175, 63.3, 12],
            team_b: [148, 88, 168, 59.5, 10]
        })

        st.dataframe(comparison, use_container_width=True)

        # Radar chart
        categories = ['Batting', 'Bowling', 'Fielding', 'Consistency', 'Recent Form']

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[85, 78, 82, 75, 88],
            theta=categories,
            fill='toself',
            name=team_a
        ))

        fig.add_trace(go.Scatterpolar(
            r=[80, 85, 75, 80, 72],
            theta=categories,
            fill='toself',
            name=team_b
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)


def show_about():
    """Display about page."""
    st.header("About This Dashboard")

    st.markdown("""
    ## Cricket Analytics Dashboard

    This dashboard provides comprehensive T20 cricket analytics including:

    - **Match Analysis**: Deep dive into individual match statistics
    - **Player Performance**: Detailed player statistics and trends
    - **Predictive Models**: ML-powered match outcome predictions
    - **Team Comparison**: Head-to-head team analysis

    ### Technology Stack
    - **Frontend**: Streamlit
    - **Data Processing**: Pandas, NumPy
    - **Visualization**: Plotly, Matplotlib, Seaborn
    - **Machine Learning**: Scikit-learn, XGBoost, LightGBM, TensorFlow, PyTorch
    - **Computer Vision**: OpenCV

    ### Data Sources
    - CricPy API (Integration pending)
    - Cricsheet data

    ### Models Implemented
    1. Logistic Regression
    2. Random Forest
    3. Gradient Boosting
    4. XGBoost
    5. LightGBM
    6. CatBoost
    7. Neural Networks (TensorFlow & PyTorch)

    ### Version
    **v0.1.0** - Initial Release

    ---

    **Note**: This dashboard is ready for data integration. Connect your CricPy API to enable all features.
    """)


if __name__ == "__main__":
    main()
