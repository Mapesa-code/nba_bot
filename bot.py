import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from scores import fetch_last_30_days_scores, save_to_csv
from reddit import fetch_reddit_posts, analyze_sentiments
from youtube import get_youtube_videos
from ai_summary import summarize_posts_with_gpt

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NBA Bot: /scores | /reddit | /yt | /ai")

async def scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games = fetch_last_30_days_scores()
    save_to_csv(games)
    await update.message.reply_text(f"Fetched {len(games)} games.")

async def reddit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posts = fetch_reddit_posts()
    results, summary = analyze_sentiments(posts)
    msg = "\n".join(f"{r['title']} ({r['score']:+.2f})" for r in results)
    msg += f"\n\nOverall sentiment: {summary}"
    await update.message.reply_text(msg[:4096])

async def yt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vids = get_youtube_videos()
    msg = "\n".join(f"{v['title']} — https://youtu.be/{v['video_id']}" for v in vids)
    await update.message.reply_text(msg)

async def ai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posts = fetch_reddit_posts()
    summary = summarize_posts_with_gpt(posts)
    await update.message.reply_text(summary[:4096])

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scores", scores))
    app.add_handler(CommandHandler("reddit", reddit_cmd))
    app.add_handler(CommandHandler("yt", yt_cmd))
    app.add_handler(CommandHandler("ai", ai_cmd))

    app.run_polling()

if __name__ == "__main__":
    main()
