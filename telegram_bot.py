import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from nba_fetch import fetch_last_n_days_scores
from reddit_sentiment import fetch_reddit_posts, analyze_sentiments
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your NBA analytics bot.")

def fetch_scores(update: Update, context: CallbackContext):
    try:
        games = fetch_last_n_days_scores()
        update.message.reply_text(f"Fetched {len(games)} games from the last 30 days.")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def fetch_reddit(update: Update, context: CallbackContext):
    posts = fetch_reddit_posts("Oklahoma City Thunder")
    results, sentiment = analyze_sentiments(posts)
    msg = "\n".join([f"{r['title']} (score={r['score']:.2f})" for r in results])
    msg += f"\n\nAggregate sentiment: {sentiment}"
    update.message.reply_text(msg[:4096])  # Telegram's message limit

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fetch_scores", fetch_scores))
    dp.add_handler(CommandHandler("fetch_reddit", fetch_reddit))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
