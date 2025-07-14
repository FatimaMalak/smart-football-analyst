import streamlit as st
import pandas as pd
import plotly.express as px
from apis.football_data import get_team_performance_and_save, LEAGUES, get_teams_by_competition

def plot_performance(df: pd.DataFrame):
    """
    Function to plot summarized performance graphs per season
    """
    # تجميع البيانات حسب الموسم
    df_summary = df.groupby("season", as_index=False).agg({
        "points": "sum",
        "goalsFor": "sum",
        "goalsAgainst": "sum"
    })
    df_summary["goal_difference"] = df_summary["goalsFor"] - df_summary["goalsAgainst"]

    # رسم الأهداف المسجلة والمستقبلة
    fig_goals = px.bar(df_summary, x='season', y=['goalsFor', 'goalsAgainst'],
                       labels={'goalsFor': 'Goals Scored', 'goalsAgainst': 'Goals Conceded'},
                       title="Goals Scored vs Goals Conceded")
    st.plotly_chart(fig_goals)

#Purpose: Generates performance charts for a team.
#How it works:
#Aggregates data by season using groupby.
#Calculates the goal difference.
#Creates a bar chart comparing goals scored and conceded.
#Displays the chart using Streamlit.

def app():
    st.title("📂 Historical Trends")
    st.markdown("🎯 *Explore your favorite team’s journey throughout the 2023 and 2024 seasons with stats and summaries!*")

    # Select League
    league_name = st.selectbox("🌍 Select a League", list(LEAGUES.keys()))
    competition_code = LEAGUES[league_name]

    # Update the season selection to include both 2023 and 2024
    selected_season = st.selectbox("📅 Select Base Season", [2023, 2024], help="Select the season you want to explore.")

    with st.spinner(f"🔍 Fetching teams from {league_name}..."):
        teams = get_teams_by_competition(competition_code, selected_season)

    if teams:
        team_names = [team["name"] for team in teams]
        selected_team_name = st.selectbox("⚽ Select a Team", team_names)
        team_id = next(team["id"] for team in teams if team["name"] == selected_team_name)

        refresh = st.checkbox("🔄 Force refresh from API")

        with st.spinner(f"📈 Loading performance data for **{selected_team_name}**..."):
            df = get_team_performance_and_save(team_id, selected_team_name, competition_code, [selected_season], force_refresh=refresh)

        if not df.empty:
            st.subheader(f"📊 {selected_team_name} – Season {selected_season} Performance")
            st.dataframe(df)

            # Display performance graphs
            plot_performance(df)

            # Metrics Summary
            with st.expander("📌 Summary Stats"):
                latest = df.iloc[-1]
                st.metric("🏆 Position", latest["position"])
                st.metric("🎯 Points", latest["points"])
                st.metric("🥅 Goals For", latest["goalsFor"])
                st.metric("🛡️ Goals Against", latest["goalsAgainst"])
                st.metric("📈 Goal Difference", latest["goalsFor"] - latest["goalsAgainst"])

        else:
            st.warning("❌ No data available for the selected team and season.")
    else:
        st.warning("⚠️ No teams found for the selected league.")


#Purpose: Main function to render the Streamlit app.
#How it works:
#Sets up the Streamlit page title and description.
#Allows users to select a league, season, and team.
#Fetches team performance data using get_team_performance_and_save().
#Displays the data in a table, chart, and summary metrics.
#Handles cases where no data is available.