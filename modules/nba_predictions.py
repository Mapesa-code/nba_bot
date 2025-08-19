import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os # <-- Import the os module

def get_nba_predictions():
    # Retrieve the API key from environment variables
    API_KEY = os.getenv("SPORTS_API_KEY")
    
    # Check if the API key exists
    if not API_KEY:
        print("Error: SPORTS_API_KEY environment variable not set!")
        # You could also raise an exception here to stop the app
        # raise ValueError("SPORTS_API_KEY environment variable not set!")
        return [] # Return empty list to prevent crash

    BASE_URL = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/"
    HEADERS = {"Ocp-Apim-Subscription-Key": API_KEY}

    # We'll train on the last 30 days and predict for today
    today = datetime.now()
    all_games_data = []

    for i in range(30):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"{BASE_URL}{date}"
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            games = response.json()
            if games:
                all_games_data.extend(games)
        except Exception as e:
            print(f"Error fetching data for {date}: {e}")
            continue

    if not all_games_data:
        return []

    df = pd.DataFrame(all_games_data)
    # Ensure score columns are not null before comparison
    df = df[df['HomeTeamScore'].notna() & df['AwayTeamScore'].notna()]
    if df.empty:
        return []
        
    df['HomeTeamWon'] = (df['HomeTeamScore'] > df['AwayTeamScore']).astype(int)
    
    features = ['PointSpread', 'OverUnder', 'HomeTeamMoneyLine', 'AwayTeamMoneyLine']
    target = 'HomeTeamWon'

    # Filter out rows where essential features might be missing
    df_train = df.dropna(subset=features)
    if df_train.empty or len(df_train['HomeTeamWon'].unique()) < 2:
         print("Not enough data to train the model after cleaning.")
         return []

    X = df_train[features]
    y = df_train[target]

    # Use stratify only if there are at least 2 classes
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)

    # Now, let's get today's games to predict
    today_str = today.strftime("%Y-%m-%d")
    url_today = f"{BASE_URL}{today_str}"
    try:
        response_today = requests.get(url_today, headers=HEADERS)
        response_today.raise_for_status()
        today_games = response_today.json()
    except Exception:
        today_games = []

    if not today_games:
        return []

    predict_df = pd.DataFrame(today_games)
    # Check if prediction data is valid
    if predict_df.empty or not all(f in predict_df.columns for f in features):
        return []
        
    X_predict = predict_df[features].fillna(predict_df[features].mean())
    X_predict_scaled = scaler.transform(X_predict)
    
    predictions = model.predict(X_predict_scaled)
    
    # Add predictions to the game data
    for i, game in enumerate(today_games):
        game['prediction'] = 'Home Team' if predictions[i] == 1 else 'Away Team'
        
    return today_games
