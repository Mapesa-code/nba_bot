import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from nba_fetch import fetch_last_n_days_scores
from reddit_sentiment import fetch_reddit_posts, analyze_sentiments
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your NBA analytics bot.")

async def fetch_scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        games = fetch_last_n_days_scores()
        await update.message.reply_text(f"Fetched {len(games)} games from the last 30 days.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def fetch_reddit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posts = fetch_reddit_posts("Oklahoma City Thunder")
    results, sentiment = analyze_sentiments(posts)
    msg = "\n".join([f"{r['title']} (score={r['score']:.2f})" for r in results])
    msg += f"\n\nAggregate sentiment: {sentiment}"
    await update.message.reply_text(msg[:4096])  # Telegram's message limit

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fetch_scores", fetch_scores))
    app.add_handler(CommandHandler("fetch_reddit", fetch_reddit))
    app.run_polling()

if __name__ == "__main__":
    main()
