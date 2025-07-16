import requests
import pandas as pd
from config import SPORTSDATA_API_KEY

ALL_TEAMS_URL = "https://api.sportsdata.io/v3/nba/scores/json/AllTeams"
PLAYER_STATS_BASE_URL = "https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStatsByTeam"

def fetch_all_teams():
    params = {"key": SPORTSDATA_API_KEY}
    r = requests.get(ALL_TEAMS_URL, params=params)
    r.raise_for_status()
    return r.json()

def fetch_team_player_stats(season, team_abbr):
    url = f"{PLAYER_STATS_BASE_URL}/{season}/{team_abbr}"
    params = {"key": SPORTSDATA_API_KEY}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

def aggregate_team_stats(season, teams):
    stats = []
    for team in teams:
        abbr = team["Key"]
        try:
            players = fetch_team_player_stats(season, abbr)
            df = pd.DataFrame(players)
            agg = {
                "TeamAbbr": abbr,
                "AvgPoints": df["Points"].mean(),
                "AvgAssists": df["Assists"].mean(),
                "AvgRebounds": df["Rebounds"].mean(),
                "AvgSteals": df["Steals"].mean(),
                "AvgBlocks": df["Blocks"].mean(),
                "AvgTurnovers": df["Turnovers"].mean(),
            }
            stats.append(agg)
        except Exception as e:
            print(f"Error fetching stats for {abbr}: {e}")
    return pd.DataFrame(stats)
