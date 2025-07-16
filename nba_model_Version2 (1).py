import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def prepare_features(games_df):
    # Only games with valid scores
    games_df = games_df[(games_df['HomeTeamScore'].notnull()) & (games_df['AwayTeamScore'].notnull())]
    games_df['HomeWin'] = (games_df['HomeTeamScore'] > games_df['AwayTeamScore']).astype(int)
    # Example features
    games_df['ScoreDiff'] = games_df['HomeTeamScore'] - games_df['AwayTeamScore']
    features = ['HomeTeamScore', 'AwayTeamScore', 'ScoreDiff']
    return games_df, features

def train_logistic_regression(games_df, features):
    X = games_df[features]
    y = games_df['HomeWin']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return model, acc, report