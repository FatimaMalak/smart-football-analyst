# ⚽ Smart Football Analyst

**Smart Football Analyst** is an AI-powered football data analytics dashboard that allows users to view, analyze, and summarize football matches from Europe's top leagues. It includes interactive visualizations, match summaries, and player/team insights using Streamlit and Plotly.

---

## 🚀 Features

- 📅 View fixtures by date
- 📊 Analyze team and match performance
- 📈 Interactive data visualizations with Plotly
- 🤖 AI-generated match summaries and player insights (via Ollama Mistral)
- 🔍 Search by team, league, or date
- 🔄 Refresh and update match data from local CSV or APIs

---

## 🛠️ Technologies Used

- Python 3.x
- [Streamlit](https://streamlit.io/) — UI/dashboard
- [Plotly](https://plotly.com/) — Visualizations
- SQLite — Lightweight local database
- Pandas & NumPy — Data handling
- aiohttp — API requests
- Ollama Mistral — AI processing and summarization (local model)

---

## 📁 Project Structure

smart-football-analyst/
│
├── app/ # Streamlit app files
├── data/ # Local datasets (CSV files)
│ ├── matches.csv
│ ├── teams.csv
│ └── standings.csv
├── notebooks/ # (Optional) Jupyter notebooks for analysis
├── backend/ # FastAPI backend (if used)
├── requirements.txt # Python dependencies
└── README.md