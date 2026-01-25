"""
Team Strength Rankings Dashboard
Visualize ELO ratings and team power rankings
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import pickle

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(page_title="Team Rankings", page_icon="🏆", layout="wide")

st.title("🏆 Team Strength Rankings")
st.markdown("**ELO-based power ratings for T20 cricket teams**")

# Load rating system
@st.cache_resource
def load_ratings():
    """Load team ratings from pickle"""
    rating_path = Path(__file__).parent.parent / "scripts/ml/models/team_ratings.pkl"

    if not rating_path.exists():
        return None

    with open(rating_path, 'rb') as f:
        data = pickle.load(f)

    return data

@st.cache_data
def load_rankings():
    """Load current rankings CSV"""
    rankings_path = Path(__file__).parent.parent / "scripts/ml/models/team_rankings.csv"
    return pd.read_csv(rankings_path)

@st.cache_data
def load_history():
    """Load rating history CSV"""
    history_path = Path(__file__).parent.parent / "scripts/ml/models/team_rating_history.csv"
    return pd.read_csv(history_path)

# Load data
rating_data = load_ratings()

if rating_data is None:
    st.error("⚠️ Ratings not found. Run `python scripts/ml/team_ratings.py` first.")
    st.stop()

rankings = load_rankings()
history = load_history()
history['date'] = pd.to_datetime(history['date'])

st.success(f"✅ Loaded ratings for {len(rankings)} teams across {len(history)} matches")

# Current Rankings
st.header("📊 Current Team Rankings")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🥇 Top Team",
        rankings.iloc[0]['team'],
        f"{rankings.iloc[0]['rating']:.0f} ELO"
    )

with col2:
    avg_rating = rankings['rating'].mean()
    st.metric(
        "📊 Average Rating",
        f"{avg_rating:.0f}",
        f"{len(rankings)} teams"
    )

with col3:
    rating_range = rankings['rating'].max() - rankings['rating'].min()
    st.metric(
        "📏 Rating Spread",
        f"{rating_range:.0f} points",
        f"Max-Min difference"
    )

# Rankings table with conditional formatting
st.subheader("🏅 Full Rankings")

# Color code by rating
def color_rating(rating):
    if rating >= 1600:
        return '🟢'  # Elite
    elif rating >= 1500:
        return '🟡'  # Strong
    elif rating >= 1450:
        return '🟠'  # Average
    else:
        return '🔴'  # Weak

rankings['tier'] = rankings['rating'].apply(color_rating)
rankings['rating'] = rankings['rating'].round(0).astype(int)

st.dataframe(
    rankings[['rank', 'tier', 'team', 'rating']],
    use_container_width=True,
    hide_index=True,
    height=600
)

st.caption("""
**Rating Tiers:** 🟢 Elite (1600+) | 🟡 Strong (1500-1600) | 🟠 Average (1450-1500) | 🔴 Developing (<1450)
""")

# Horizontal bar chart
st.subheader("📊 Rating Comparison")

fig = px.bar(
    rankings.head(15),
    y='team',
    x='rating',
    orientation='h',
    title='Top 15 Teams by ELO Rating',
    color='rating',
    color_continuous_scale='RdYlGn',
    text='rating'
)

fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig.update_layout(
    height=600,
    showlegend=False,
    xaxis_title="ELO Rating",
    yaxis_title="",
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(fig, use_container_width=True)

# Rating Evolution Over Time
st.header("📈 Rating Evolution")

# Let user select teams to track
all_teams = sorted(rankings['team'].unique())
default_teams = rankings.head(5)['team'].tolist()

selected_teams = st.multiselect(
    "Select teams to track:",
    all_teams,
    default=default_teams
)

if selected_teams:
    # Build time series for each team
    team_timeseries = {}

    for team in selected_teams:
        # Get all rating updates for this team
        winner_data = history[history['winner'] == team][['date', 'winner_rating_after']].copy()
        winner_data.columns = ['date', 'rating']

        loser_data = history[history['loser'] == team][['date', 'loser_rating_after']].copy()
        loser_data.columns = ['date', 'rating']

        # Combine and sort
        team_data = pd.concat([winner_data, loser_data]).sort_values('date')
        team_timeseries[team] = team_data

    # Plot
    fig = go.Figure()

    for team, data in team_timeseries.items():
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['rating'],
            name=team,
            mode='lines',
            line=dict(width=2)
        ))

    fig.add_hline(y=1500, line_dash="dash", line_color="gray",
                  annotation_text="Initial Rating (1500)")

    fig.update_layout(
        title='Team Rating Evolution Over Time',
        xaxis_title='Date',
        yaxis_title='ELO Rating',
        hovermode='x unified',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

# Match Predictor
st.header("🔮 Match Outcome Predictor")

st.markdown("Predict match outcome based on current ELO ratings")

col1, col2 = st.columns(2)

with col1:
    team_a = st.selectbox("Team A", all_teams, index=0)

with col2:
    team_b = st.selectbox("Team B", all_teams, index=1)

if team_a != team_b:
    # Get ratings
    rating_a = rankings[rankings['team'] == team_a]['rating'].values[0]
    rating_b = rankings[rankings['team'] == team_b]['rating'].values[0]

    # Calculate win probabilities
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    expected_b = 1 - expected_a

    st.subheader("🎯 Prediction")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.metric(
            team_a,
            f"{rating_a:.0f} ELO",
            f"{expected_a*100:.1f}% win chance"
        )

    with col2:
        st.markdown("### VS")

    with col3:
        st.metric(
            team_b,
            f"{rating_b:.0f} ELO",
            f"{expected_b*100:.1f}% win chance"
        )

    # Probability visualization
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[expected_a * 100, expected_b * 100],
        y=[team_a, team_b],
        orientation='h',
        marker_color=['#2ecc71' if expected_a > expected_b else '#e74c3c',
                      '#2ecc71' if expected_b > expected_a else '#e74c3c'],
        text=[f"{expected_a*100:.1f}%", f"{expected_b*100:.1f}%"],
        textposition='auto'
    ))

    fig.update_layout(
        title='Win Probability',
        xaxis_title='Probability (%)',
        xaxis_range=[0, 100],
        yaxis_title='',
        showlegend=False,
        height=250
    )

    st.plotly_chart(fig, use_container_width=True)

    # Favorite/underdog
    favorite = team_a if expected_a > expected_b else team_b
    underdog = team_b if expected_a > expected_b else team_a
    prob_diff = abs(expected_a - expected_b) * 100

    if prob_diff > 30:
        st.info(f"**Strong Favorite:** {favorite} is heavily favored ({prob_diff:.1f}% advantage)")
    elif prob_diff > 15:
        st.info(f"**Favorite:** {favorite} has the edge ({prob_diff:.1f}% advantage)")
    else:
        st.success(f"**Evenly Matched:** This should be a close contest! ({prob_diff:.1f}% difference)")

# Historical Insights
st.header("📜 Historical Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Biggest Rating Gains")

    biggest_gains = history.nlargest(10, 'winner_change')[
        ['date', 'winner', 'loser', 'margin', 'margin_type', 'winner_change']
    ]
    biggest_gains['winner_change'] = biggest_gains['winner_change'].round(1)
    biggest_gains['date'] = pd.to_datetime(biggest_gains['date']).dt.strftime('%Y-%m-%d')

    st.dataframe(
        biggest_gains,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("😱 Biggest Upsets")

    upsets = history[history['winner_expected'] < 0.4].nsmallest(10, 'winner_expected')[
        ['date', 'winner', 'loser', 'winner_expected', 'winner_change']
    ]
    upsets['win_prob'] = (upsets['winner_expected'] * 100).round(1).astype(str) + '%'
    upsets['rating_gain'] = upsets['winner_change'].round(1)
    upsets['date'] = pd.to_datetime(upsets['date']).dt.strftime('%Y-%m-%d')

    st.dataframe(
        upsets[['date', 'winner', 'loser', 'win_prob', 'rating_gain']],
        use_container_width=True,
        hide_index=True
    )

# System Information
st.divider()
st.subheader("ℹ️ About ELO Rating System")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **How ELO Works:**
    - Teams start at 1500 rating
    - Win = gain points
    - Loss = lose points
    - Bigger wins = more points
    """)

with col2:
    st.markdown("""
    **Victory Margin Impact:**
    - Close (1-9 runs): 1.0x
    - Comfortable (10-29 runs): 1.2x
    - Dominant (30+ runs): 1.5x
    """)

with col3:
    st.markdown("""
    **System Stats:**
    - K-factor: 32
    - Matches processed: {0}
    - Teams rated: {1}
    - Date range: 2014-2024
    """.format(len(history), len(rankings)))

st.caption("🏏 ELO ratings update after every match based on result and margin of victory")

st.markdown("---")
st.caption("🏆 Team Strength Rankings | Powered by ELO Rating System")
