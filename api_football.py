import requests
import csv
import pandas as pd
import os

# === إعدادات عامة ===
API_KEY = "e6943610c6msha0020215e423899p12ce63jsn8a7d971f9e27"
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}        

'''
Purpose: These are configuration variables.
Explanation:
requests, csv, pandas, and os are imported for HTTP requests, CSV handling, data manipulation, and file operations respectively.
API_KEY and BASE_URL store credentials and the base URL for API requests.
headers include authentication headers required for API access.
'''

# === 1. جلب المواسم المتوفرة لدوري معين ===
def get_league_seasons(league_id):
    url = f"{BASE_URL}/leagues?id={league_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("response", [])
        if not data:
            print("⚠️ لا توجد بيانات لهذا الدوري.")
            return []
        return [season["year"] for season in data[0].get("seasons", [])]
    else:
        print(f"❌ فشل في جلب المواسم: {response.status_code}")
        return []

'''
Purpose: Fetches available seasons for a specific league.
How it works:
Constructs the API URL with the provided league_id.
Sends a GET request to the API.
Checks if the response status code is 200 (success).
Extracts the list of seasons from the JSON response.
Returns a list of season years (e.g., [2020, 2021]).
Handles errors by printing messages and returning empty lists.
'''

# === 2. جلب الفرق لدوري وموسم معين ===
def get_teams_by_league(league_id, season=2024): 
    url = f"{BASE_URL}/teams"
    params = {"league": league_id, "season": season}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get("response", [])
        if not data:
            print(f"⚠️ لا توجد فرق للدوري {league_id} في الموسم {season}")
        else:
            print(f"✅ تم جلب {len(data)} فريق للدوري {league_id} - الموسم {season}")
        return [team["team"] for team in data]
    else:
        print(f"❌ فشل في جلب الفرق: {response.status_code}")
        return []

#Saves team data to a CSV file.
def save_teams_to_csv(league_id, season=2024, filename="teams.csv"):
    teams = get_teams_by_league(league_id, season)
    if teams:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "country", "logo"])
            writer.writeheader()
            for team in teams:
                writer.writerow({
                    "id": team["id"],
                    "name": team["name"],
                    "country": team.get("country", ""),
                    "logo": team.get("logo", "")
                })
        print(f"✅ تم حفظ بيانات الفرق في {filename}")
    else:
        print("❌ لم يتم العثور على فرق.")

"""
How it works:
Calls get_teams_by_league() to fetch team data.
If teams are found:
Creates/overwrites a CSV file.
Writes team details (ID, name, country, logo) to the CSV.
Prints confirmation messages based on success/failure.

"""
# === 3. جلب بيانات اللاعبين لفريق معين ===
def get_players_with_data(team_id, season=2024, save_csv=True):
    url = f"{BASE_URL}/players"
    params = {"team": team_id, "season": season}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ فشل في جلب اللاعبين للفريق {team_id}")
        return []

    data = response.json().get("response", [])
    players_data = []

    for item in data:
        player = item["player"]
        stats = item["statistics"][0] if item["statistics"] else {}

        games = stats.get("games", {}) if stats else {}
        goals = stats.get("goals", {}) if stats else {}

        players_data.append({
            "id": player.get("id"),
            "name": player.get("name"),
            "age": player.get("age"),
            "nationality": player.get("nationality"),
            "team_id": team_id,
            "position": games.get("position"),
            # تصحيح مفتاح appearances مع دعم كلا الاحتمالين
            "appearances": games.get("appearences") or games.get("appearances"),
            "minutes": games.get("minutes"),
            "goals": goals.get("total"),
            "assists": goals.get("assists")
        })

    if save_csv:
        os.makedirs("data", exist_ok=True)
        path = f"data/players_team_{team_id}_{season}.csv"
        df = pd.DataFrame(players_data)
        if not df.empty:
            df.to_csv(path, index=False)
            print(f"✅ تم حفظ بيانات اللاعبين في {path}")
        else:
            print(f"⚠️ لا توجد بيانات لاعبين لحفظها للفريق {team_id}")

    return players_data

'''
Purpose: Fetches player data for a specific team and season.
How it works:
Constructs the API URL for fetching players.
Sends a GET request with parameters team_id and season.
Checks if the response status code is 200 (success).
Extracts player data and their statistics from the JSON response.
Processes statistics to handle potential missing keys.
Saves player data to a CSV file if save_csv is True.
Returns a list of player dictionaries.
'''

# === 4. جلب إحصاءات لاعب معين ===
def get_player_stats(player_id, season=2024, save_csv=True):
    url = f"{BASE_URL}/players"
    params = {"id": player_id, "season": season}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ فشل في جلب الإحصاءات للاعب {player_id}")
        return {}

    data = response.json().get("response", [])
    if not data:
        print(f"⚠️ لا توجد إحصاءات للاعب {player_id}")
        return {}

    stats = data[0]["statistics"][0]

    games = stats.get("games", {}) if stats else {}
    goals = stats.get("goals", {}) if stats else {}
    cards = stats.get("cards", {}) if stats else {}
    team_info = stats.get("team", {}) if stats else {}
    league_info = stats.get("league", {}) if stats else {}

    stat_data = {
        "player_id": player_id,
        "season": season,
        "team": team_info.get("name"),
        "league": league_info.get("name"),
        "position": games.get("position"),
        "appearances": games.get("appearences") or games.get("appearances"),
        "minutes": games.get("minutes"),
        "rating": games.get("rating"),
        "goals": goals.get("total"),
        "assists": goals.get("assists"),
        "yellow_cards": cards.get("yellow"),
        "red_cards": cards.get("red")
    }

    if save_csv:
        os.makedirs("data", exist_ok=True)
        path = f"data/player_stats_{player_id}_{season}.csv"
        df = pd.DataFrame([stat_data])
        if not df.empty:
            df.to_csv(path, index=False)
            print(f"✅ تم حفظ إحصاءات اللاعب في {path}")
        else:
            print(f"⚠️ لا توجد بيانات لحفظها للاعب {player_id}")

    return stat_data

'''
Purpose: Fetches detailed statistics for a specific player.
How it works:
Constructs the API URL for fetching player statistics.
Sends a GET request with parameters player_id and season.
Checks if the response status code is 200 (success).
Extracts player statistics from the JSON response.
Processes different aspects of the statistics (games, goals, cards, team, league).
Combines all statistics into a dictionary.
Saves the statistics to a CSV file if save_csv is True.
Returns the statistics dictionary.
'''

# === 5. جلب إحصاءات مباراة ===
def get_match_stats(fixture_id):
    url = f"{BASE_URL}/fixtures/statistics"
    params = {"fixture": fixture_id}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print(f"❌ فشل في جلب إحصاءات المباراة: {response.status_code}")
        return []

'''
Purpose: Fetches statistics for a specific match.
How it works:
Constructs the API URL for fetching match statistics.
Sends a GET request with the fixture_id parameter.
Checks if the response status code is 200 (success).
Returns the statistics from the JSON response.
Handles errors by printing messages and returning empty lists.
'''

# === 6. جلب جميع البيانات لدوري معين ===
def fetch_league_full_data(league_id, season=2024, save_csv=True):
    print(f"📥 جاري تحميل الفرق لدوري {league_id} - موسم {season}")
    teams = get_teams_by_league(league_id, season)
    if not teams:
        print("❌ لم يتم العثور على فرق، إيقاف العملية.")
        return

    all_stats = []

    for team in teams:
        print(f"\n🏃 تحميل لاعبي الفريق: {team['name']} ({team['id']})")
        players = get_players_with_data(team["id"], season, save_csv=False)

        if not players:
            print(f"⚠️ لا توجد بيانات لاعبين للفريق {team['name']}")
            continue

        for player in players:
            player_id = player["id"]
            if player_id:
                print(f"📊 إحصاءات اللاعب: {player['name']} ({player_id})")
                try:
                    stats = get_player_stats(player_id, season, save_csv=False)
                    if stats:
                        combined = {**player, **stats}
                        all_stats.append(combined)
                        print(f"✔️ تم دمج إحصاءات اللاعب {player['name']}")
                    else:
                        print(f"⚠️ لا توجد إحصاءات إضافية للاعب {player['name']}")
                except Exception as e:
                    print(f"⚠️ خطأ أثناء معالجة اللاعب {player['name']} ({player_id}): {e}")

    if save_csv:
        os.makedirs("data", exist_ok=True)
        path = f"data/league_{league_id}_{season}_full_players_stats.csv"
        df = pd.DataFrame(all_stats)
        if not df.empty:
            df.to_csv(path, index=False)
            print(f"\n✅ تم حفظ بيانات اللاعبين الكاملة في {path}")
        else:
            print("⚠️ لا توجد بيانات كافية لحفظها في CSV.")

'''
Purpose: Fetches comprehensive data for all teams and players in a league.
How it works:
Fetches teams for the specified league and season using get_teams_by_league().
For each team:
Fetches player data using get_players_with_data().
For each player:
Fetches detailed statistics using get_player_stats().
Combines player data with their statistics.
Adds the combined data to a list.
Saves all collected data to a CSV file if save_csv is True.
Handles errors and edge cases with try-except blocks and conditional checks.
'''

# === تشغيل الملف الرئيسي ===
if __name__ == "__main__":
    # غيّر الرقم حسب الدوري والموسم المطلوب
    fetch_league_full_data(league_id=39, season=2024, save_csv=True)
