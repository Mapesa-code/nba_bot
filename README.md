# NBA Analytics & Sentiment Bot

This project is a modular, secure Python application that:
- Fetches and analyzes NBA game data
- Trains predictive models on NBA results
- Performs sentiment analysis on Reddit posts
- Delivers results via a Telegram Bot

## Features

- **NBA Data Fetch**: Get last 30 days of NBA games and team stats from SportsData.io API.
- **Modeling**: Train a logistic regression to predict game outcomes.
- **Reddit Sentiment**: Analyze sentiment of recent Reddit posts about NBA teams.
- **Telegram Bot**: Interactive bot for fetching scores and Reddit sentiment.

## Setup

1. **Clone the repo**
2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set your API keys**

    Create a `.env` file in the root directory:

    ```
    SPORTSDATA_API_KEY=your_sportsdata_key
    OPENAI_API_KEY=your_openai_key
    TELEGRAM_BOT_TOKEN=your_telegram_token
    ```

4. **Run the Telegram bot**

    ```bash
    python telegram_bot.py
    ```

## Module Overview

- `config.py` — Loads API keys from environment.
- `nba_fetch.py` — Functions to fetch NBA games for a date range.
- `nba_team_stats.py` — Fetch and aggregate team stats.
- `nba_model.py` — Model training and evaluation helpers.
- `reddit_sentiment.py` — Reddit post fetching and sentiment analysis.
- `telegram_bot.py` — Telegram bot entry point.
- `requirements.txt` — All dependencies.

## Security Notes

- **Do not hard-code API keys.** Use environment variables or `.env` files (not committed to git).
- **Never share your `.env` or credentials.**
- **Rotate all keys if they have ever been exposed.**

## Extending

- Add more commands to the Telegram bot for advanced analytics.
- Integrate with other sports or data sources.
- Improve model features with rolling stats, player injuries, etc.

---

**Questions or suggestions? Open an Issue or Pull Request!**
