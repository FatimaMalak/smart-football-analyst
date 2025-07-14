import streamlit as st
import pandas as pd
from apis.football_data import get_league_standings

def app():
    st.title("🏆 League Overview")

    league_choice = st.selectbox(
        "Select a League",
        ["Premier League", "Serie A", "Bundesliga", "La Liga", "Ligue 1"]
    )

    league_ids = {
        "Premier League": "PL",
        "Serie A": "SA",
        "Bundesliga": "BL1",
        "La Liga": "PD",
        "Ligue 1": "FL1",
      
    }

    league_id = league_ids.get(league_choice)

    if league_id:
        standings = get_league_standings(league_id)

        if standings:  # التأكد من وجود البيانات
            st.subheader(f"Standings for {league_choice} - 2024 Season")
            standings_df = pd.DataFrame(standings)
            st.table(standings_df)
        else:
            st.warning("⚠️ No standings data available. The competition may not have started or there was an API error.")
    else:
        st.error("❌ Invalid league selection.")


#Purpose: Main function to render the Streamlit app.
#How it works:
#Sets up the Streamlit page title.
#Allows users to select a league.
#Fetches league standings using get_league_standings().
#Displays the standings in a table.
#Handles cases where standings data is unavailable or the league selection is invalid.
