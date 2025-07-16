import requests
from datetime import datetime, timedelta
from config import SPORTSDATA_API_KEY

NBA_BASE_URL = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDate"

def fetch_scores_for_date(date_str):
    url = f"{NBA_BASE_URL}/{date_str}"
    params = {"key": SPORTSDATA_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {date_str}: {response.status_code}")
        return []

def get_last_n_days_dates(n=30):
    today = datetime.utcnow()
    return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(n)]

def fetch_last_n_days_scores(n=30):
    all_games = []
    for date_str in get_last_n_days_dates(n):
        games = fetch_scores_for_date(date_str)
        if games:
            all_games.extend(games)
    return all_games
