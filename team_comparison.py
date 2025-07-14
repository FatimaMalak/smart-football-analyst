import streamlit as st
import pandas as pd

# Load datasets
matches_df = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/matches.csv")
standings_df = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/standings.csv")
teams_df = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/teams.csv")

# Helper to get team name by ID
def get_team_name(team_id):
    name = teams_df.loc[teams_df['team_id'] == team_id, 'name']
    return name.values[0] if not name.empty else str(team_id)

# Helper to get latest common season
def get_latest_common_season(t1_id, t2_id):
    t1_seasons = standings_df[standings_df["team_id"] == t1_id]["season_id"].unique()
    t2_seasons = standings_df[standings_df["team_id"] == t2_id]["season_id"].unique()
    common = set(t1_seasons).intersection(set(t2_seasons))
    return max(common) if common else None

# Display season stats
def show_team_stats(stats, name):
    if not stats.empty:
        stats = stats.iloc[0]
        st.metric(f"{name} - Position", stats['position'])
        st.metric(f"{name} - Points", stats['points'])
        st.metric(f"{name} - Wins", stats['won'])
        st.metric(f"{name} - Goal Diff", stats['goal_difference'])
    else:
        st.warning(f"No season stats found for {name}.")

#get_team_name(team_id): Fetches a team's name by ID.
#get_latest_common_season(t1_id, t2_id): Finds the most recent season where both teams played.
#show_team_stats(stats, name): Displays seasonal statistics for a team.

# Main Streamlit page
def render_team_comparison():
    st.title("⚽ Team Comparison & Head-to-Head Analysis")

    # Team selection
    team_names = teams_df["name"].sort_values().tolist()
    team1_name = st.selectbox("Select Team 1", team_names)
    team2_name = st.selectbox("Select Team 2", team_names)

    if team1_name == team2_name:
        st.warning("Please select two different teams.")
        return

    # Get team IDs
    team1_id = teams_df[teams_df["name"] == team1_name]["team_id"].values[0]
    team2_id = teams_df[teams_df["name"] == team2_name]["team_id"].values[0]

    # Head-to-head matches
    st.subheader("🔁 Head-to-Head Matches")
    h2h_matches = matches_df[
        ((matches_df["home_team_id"] == team1_id) & (matches_df["away_team_id"] == team2_id)) |
        ((matches_df["home_team_id"] == team2_id) & (matches_df["away_team_id"] == team1_id))
    ]

    if not h2h_matches.empty:
        h2h_matches["home_team"] = h2h_matches["home_team_id"].apply(get_team_name)
        h2h_matches["away_team"] = h2h_matches["away_team_id"].apply(get_team_name)
        st.dataframe(h2h_matches[["utc_date", "home_team", "away_team", "winner"]].sort_values("utc_date", ascending=False))
    else:
        st.info("No head-to-head matches found.")

    # Season performance
    season_id = get_latest_common_season(team1_id, team2_id)
    if season_id:
        st.subheader("📊 Season Performance")
        st.write(f"📅 Using Season ID: `{season_id}`")

        t1_stats = standings_df[(standings_df["team_id"] == team1_id) & (standings_df["season_id"] == season_id)]
        t2_stats = standings_df[(standings_df["team_id"] == team2_id) & (standings_df["season_id"] == season_id)]

        col1, col2 = st.columns(2)
        with col1:
            show_team_stats(t1_stats, team1_name)
        with col2:
            show_team_stats(t2_stats, team2_name)
    else:
        st.warning("No common season data available for both teams.")

#Purpose: Main function to render the Streamlit app.
#How it works:
#Allows users to select two teams.
#Fetches head-to-head match history between the selected teams.
#Displays the match history in a table.
#Fetches seasonal performance data for both teams.
#Displays the performance metrics in a formatted way.
#Handles cases where no data is available.

# Entry point
def app():
    render_team_comparison()
#Purpose: Entry point for the Streamlit app.
#How it works: Calls render_team_comparison() to render the app.

