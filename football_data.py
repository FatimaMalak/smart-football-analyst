import requests
import pandas as pd
import os

API_KEY = "1cb6d2d1e93e4fcd9929cb091d20e76a"
BASE_URL = "https://api.football-data.org/v4"
headers = {
        "X-Auth-Token": API_KEY
}

DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

# تعريف البطولات
LEAGUES = {
    "Premier League": "PL",
    "La Liga": "PD",      # بدلاً من ES1
    "Serie A": "SA",      # بدلاً من IT1
    "Bundesliga": "BL1",  # بدلاً من DE1
    "Ligue 1": "FL1",     # بدلاً من FR1
   
}

'''
Purpose: Configuration and setup.
Explanation:
Imports required libraries.
Sets up API credentials and base URL.
Creates a data directory if it doesn't exist.
Defines a dictionary mapping league names to their codes.
'''

# دالة جلب الفرق
def get_teams_by_competition(competition_code="ES1", season=2023):
    url = f"{BASE_URL}/competitions/{competition_code}/teams?season={season}"
    response = requests.get(url, headers=headers)
     # Add debugging information
    print(f"API Response for {competition_code} {season}: {response.text}")
    if response.status_code != 200:
        print(f"⚠️ Error fetching teams: {response.text}")
        return []
    try:
        data = response.json()
        teams = [{"id": team["id"], "name": team["name"]} for team in data.get("teams", [])]
    except Exception as e:
        print(f"⚠️ Error parsing response: {e}")
    
        return []
    # حفظ الفرق في ملف CSV
    df = pd.DataFrame(teams)
    teams_filename = os.path.join(DATA_DIR, f"{competition_code}_teams_{season}.csv")
    df.to_csv(teams_filename, index=False)
    print(f"✅ Teams saved to {teams_filename}")
    return teams

'''
Purpose: Fetches teams in a competition for a specific season.
How it works:
Constructs the API URL with the provided competition_code and season.
Sends a GET request to the API.
Checks if the response status code is 200 (success).
Extracts team data from the JSON response.
Saves team data to a CSV file.
Returns a list of team dictionaries.
Handles errors by printing messages and returning empty lists.
'''

# جلب أداء الفريق وحفظه إلى ملف CSV
def get_team_performance_and_save(team_id, team_name, competition_code="PL", seasons=[  2023 ,2024], force_refresh=False):
    filename = os.path.join(DATA_DIR, f"{team_name.replace(' ', '_')}_{competition_code}_performance.csv")
    
    if os.path.exists(filename) and not force_refresh:
        print(f"✅ File already exists: {filename}")
        return pd.read_csv(filename)

    results = []
    for season in seasons:
        url = f"{BASE_URL}/competitions/{competition_code}/standings?season={season}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"⚠️ Error in season {season}: {response.text}")
            continue
        data = response.json()
        try:
            for team_entry in data["standings"][0]["table"]:
                if team_entry["team"]["id"] == team_id:
                    results.append({
                        "season": season,
                        "position": team_entry["position"],
                        "points": team_entry["points"],
                        "playedGames": team_entry["playedGames"],
                        "won": team_entry["won"],
                        "draw": team_entry["draw"],
                        "lost": team_entry["lost"],
                        "goalsFor": team_entry["goalsFor"],
                        "goalsAgainst": team_entry["goalsAgainst"]
                    })
        except Exception as e:
            print(f"⚠️ Parsing error for season {season}: {e}")
            continue

    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"✅ Performance data saved to {filename}")
    return df

'''
Purpose: Fetches historical performance data for a team.
How it works:
Constructs the file path for saving team performance data.
Checks if the file already exists and returns it if force_refresh is False.
For each season in the provided list:
Constructs the API URL for fetching standings.
Sends a GET request to the API.
Checks if the response status code is 200 (success).
Extracts performance data for the specified team.
Saves the collected data to a CSV file.
Returns a DataFrame of the performance data.
Handles errors during the process.
'''

def fetch_all_teams_for_all_leagues(seasons=[2023]):
    for season in seasons:
        for league_name, code in LEAGUES.items():
            print(f"\n📥 Fetching teams for {league_name} ({code}) - {season}")
            get_teams_by_competition(code, season)

'''
Purpose: Fetches teams for all predefined leagues and seasons.
How it works:
Iterates over each season in the provided list.
For each season, iterates over the predefined leagues in LEAGUES.
Calls get_teams_by_competition() for each league-season combination.
Prints status messages during the process.
'''

# نفّذ السحب لكل البطولات والمواسم
fetch_all_teams_for_all_leagues(seasons=[2023])

# دالة لاستدعاء ترتيب الدوري
def get_league_standings(league_id):
    url = f"{BASE_URL}/competitions/{league_id}/standings"
    response = requests.get(url, headers=headers)
    data = response.json()

    print("📦 API Response:", data)
    print("🔎 League ID used:", league_id)

    if 'standings' not in data:
        print("⚠️ المفتاح 'standings' غير موجود. قد يكون ID غير صالح أو البطولة غير نشطة.")
        return []  # أو return None

    # استخراج بيانات الترتيب
    standings = []
    for entry in data['standings'][0]['table']:
        standings.append({
            "position": entry["position"],
            "team": entry["team"]["name"],
            "points": entry["points"],
            "goals_for": entry["goalsFor"],
            "goals_against": entry["goalsAgainst"],
            "goal_difference": entry["goalDifference"]
        })

    return standings

'''
Purpose: Fetches the current league standings.
How it works:
Constructs the API URL with the provided league_id.
Sends a GET request to the API.
Checks if the response contains the 'standings' key.
Extracts standings data from the JSON response.
Returns a list of dictionaries containing team standings.
Handles cases where the 'standings' key is missing.
'''

# دالة للحصول على إحصائيات الفريق
def get_team_stats(team_id):
    url = f"{BASE_URL}teams/{team_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
'''
Purpose: Fetches detailed statistics for a team.
How it works:
Constructs the API URL with the provided team_id.
Sends a GET request to the API.
Returns the JSON response containing team statistics.

'''
# دالة للحصول على بيانات التواجه المباشر بين فريقين
def get_team_head_to_head(team_a, team_b):
    url = f"{BASE_URL}matches?homeTeam={team_a}&awayTeam={team_b}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
'''
Purpose: Fetches head-to-head match history between two teams.
How it works:
Constructs the API URL with the provided team IDs.
Sends a GET request to the API.
Returns the JSON response containing match history.

'''
# دالة للحصول على إحصائيات اللاعبين
def get_player_stats(player_name):
    url = f"https://api.football-data.org/v2/players?search={player_name}" 
    response = requests.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")       # ✅ لتتبع حالة الاستجابة
    print(f"Response Text: {response.text[:500]}")      # ✅ طباعة أول 500 حرف من الرد

    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError:
            print("❌ Error: JSON decode failed.")
            return None
    else:
        print("❌ Error: Bad response from API.")
        return None
'''
Purpose: Searches for a player by name.
How it works:
Constructs the API URL with the provided player_name.
Sends a GET request to the API.
Checks if the response status code is 200 (success).
Returns the JSON response containing player data.
Handles errors related to JSON decoding and bad responses.
'''
# دالة للحصول على البيانات التاريخية
def get_historical_trends(team_id):
    url = f"{BASE_URL}teams/{team_id}/matches?season=2022"
    params = {
        "team": team_id,
        "season": 2023,
        "league": 39
    }

    response = requests.get(url, headers=headers, params=params)

    print("🔍 DEBUG URL:", response.url)
    print("🔍 DEBUG Status Code:", response.status_code)
    print("🔍 DEBUG Response Text:", response.text[:500])  # نطبع أول 500 حرف فقط

    try:
        return response.json()
    except ValueError:
        print("❌ JSONDecodeError: الرد ليس JSON. الرد الكامل:\n", response.text)
        return None
'''
Purpose: Fetches historical match data for a team.
How it works:
Constructs the API URL with the provided team_id.
Sets up parameters for the API request.
Sends a GET request to the API.
Prints debug information about the request and response.
Returns the JSON response containing historical match data.
Handles cases where the response is not valid JSON.
'''
# دالة للحصول على إحصائيات متقدمة (مثل xG)
def get_advanced_stats(team_id):
    # Assuming Football-Data.org supports advanced stats in the API
    url = f"{BASE_URL}teams/{team_id}/statistics"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
'''
Purpose: Fetches advanced statistics for a team.
How it works:
Constructs the API URL with the provided team_id.
Sends a GET request to the API.
Returns the JSON response containing advanced statistics.

'''
# دالة للحصول على الفرق من الدوري
def get_teams_for_league(competition_code):
    url = f"{BASE_URL}/competitions/{competition_code}/teams"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"⚠️ Error fetching teams: {response.text}")
        return []
    
    teams_data = response.json()
    teams = []
    for team in teams_data['teams']:
        teams.append({
            "id": team["id"],
            "name": team["name"]
        })
    
    return teams
'''
Purpose: Fetches teams in a specific league.
How it works:
Constructs the API URL with the provided competition_code.
Sends a GET request to the API.
Checks if the response status code is 200 (success).
Extracts team data from the JSON response.
Returns a list of team dictionaries.
Handles errors by printing messages and returning empty lists.
'''
# استخدام الدوال لجلب الفرق من الدوري وإنشاء ملفات CSV
get_teams_by_competition("PL", 2023)
get_team_performance_and_save(65, "Liverpool", competition_code="PL", seasons=[2020, 2021, 2022, 2023])

