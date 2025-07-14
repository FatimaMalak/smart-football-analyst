# main.py

import streamlit as st

# إعداد صفحة ستريملت
st.set_page_config(page_title="Smart Football Analyst", layout="wide")

from app import  league_overview, team_comparison, match_insights, historical_trends

# إعداد تبويبات الموقع
PAGES = {
    
    "🌍 League Overview": league_overview,
    "📊 Team Comparison": team_comparison,
    "📈 Match Insights": match_insights,
    "📂 Historical Trends": historical_trends,
   
    
}

# الشريط الجانبي للتنقل
st.sidebar.title("⚽ Smart Football Analyst")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# تشغيل الصفحة المختارة
page = PAGES[selection]
page.app()

'''
Purpose: Initializes the Streamlit app with multiple pages.
How it works:
Sets up page configuration.
Defines a dictionary mapping page names to their respective modules.
Uses a sidebar to let users navigate between pages.
Renders the selected page using its app() function.

'''