import streamlit as st
import pandas as pd
import datetime

def app():
   
    # تحميل البيانات
    matches = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/matches.csv", parse_dates=["utc_date"])
    scores = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/scores.csv")
    stadiums = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/stadiums.csv")
    teams = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/teams.csv")
    leagues = pd.read_csv("data/european-top-5-leagues/kaggle_dataset/leagues.csv")

    # تجهيز البيانات
    matches = matches.merge(teams[['team_id', 'name', 'stadium_id']], left_on='home_team_id', right_on='team_id', how='left')
    matches = matches.rename(columns={'name': 'home_team', 'stadium_id': 'home_stadium_id'})
    matches = matches.merge(teams[['team_id', 'name']], left_on='away_team_id', right_on='team_id', how='left')
    matches = matches.rename(columns={'name': 'away_team'})
    matches = matches.merge(stadiums[['stadium_id', 'name']], left_on='home_stadium_id', right_on='stadium_id', how='left')
    matches = matches.rename(columns={'name': 'stadium_name'})
    matches = matches.merge(leagues[['league_id', 'name']], on='league_id', how='left')
    matches = matches.rename(columns={'name': 'league_name'})
    matches = matches.merge(scores, on='match_id', how='left')

    # 📅 اختيار التاريخ
    
    # Get first and last available dates from your data
    first_date = matches["utc_date"].min().date()
    last_date = matches["utc_date"].max().date()

    # Define the range you want
    min_allowed = datetime.date(2023, 1, 1)
    max_allowed = datetime.date(2024, 6, 2)

# Choose a default date within the allowed range
    if first_date < min_allowed:
       default_date = min_allowed
    elif first_date > max_allowed:
       default_date = max_allowed
    else:
        default_date = first_date

    # Use st.date_input with all values correctly bounded
    selected_date = st.date_input(
    "📅 اختر تاريخ المباراة",
    value=default_date,
    min_value=min_allowed,
    max_value=max_allowed
)
 
    # 🏆 اختيار الدوري
    league_options = ["All"] + sorted(matches['league_name'].dropna().unique().tolist())
    selected_league = st.selectbox("🏆 choose a league", league_options)

    # 🏟 اختيار الفريق المضيف أو الضيف (اختياري)
    team_options = ["All"] + sorted(matches['home_team'].dropna().unique().tolist())
    selected_home_team = st.selectbox("🏠 home team", team_options)
    selected_away_team = st.selectbox("🚩 away team", team_options)

    # 🎯 التصفية
    filtered = matches[matches['utc_date'].dt.date == selected_date]

    if selected_league != "All":
        filtered = filtered[filtered['league_name'] == selected_league]

    if selected_home_team != "All":
        filtered = filtered[filtered['home_team'] == selected_home_team]

    if selected_away_team != "All":
        filtered = filtered[filtered['away_team'] == selected_away_team]

    # 📝 عرض التفاصيل
    if not filtered.empty:
        st.subheader("📊 Match details:")
        for _, match in filtered.iterrows():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### ⚽ {match['home_team']} vs {match['away_team']}")
                st.write(f"🏆league: {match['league_name']}")
                st.write(f"📅 date: {match['utc_date'].strftime('%Y-%m-%d')}")
                st.write(f"🏟 stadium: {match['stadium_name'] if pd.notna(match['stadium_name']) else 'غير متوفر'}")
            with col2:
                st.metric("🔢 final result", f"{match['full_time_home']} - {match['full_time_away']}")
                st.metric("⏱ first half time result", f"{match['half_time_home']} - {match['half_time_away']}")
            st.markdown("---")
    else:
        st.warning("❌ No matches found.")


#purpose: Main function to render the Streamlit app.
#How it works:
#Loads match data from CSV files.
#Merges data from different CSV files to enrich match details.
#Allows users to filter matches by date, league, and team.
#Displays match details in a formatted way.
#Handles cases where no matches are found.
