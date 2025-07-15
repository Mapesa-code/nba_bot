import requests
import pandas as pd
from datetime import datetime, timedelta
from config import API_KEY

BASE_URL = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDateFinal"

def fetch_scores_for_date(date_str):
    resp = requests.get(f"{BASE_URL}/{date_str}", params={"key": API_KEY})
    return resp.json() if resp.status_code == 200 else []

def get_last_30_days_dates():
    return [(datetime.utcnow() - timedelta(days=i)).strftime("%Y-%b-%d").upper() for i in range(30)]

def fetch_last_30_days_scores():
    all_games = []
    for date in get_last_30_days_dates():
        all_games.extend(fetch_scores_for_date(date))
    return all_games

def save_to_csv(games, filename="nba_scores_last_30_days.csv"):
    pd.DataFrame(games).to_csv(filename, index=False)
