from telegram import Update
from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_BOT_TOKEN
from scores import fetch_last_30_days_scores, save_to_csv
from reddit import fetch_reddit_posts, analyze_sentiments
from youtube import get_youtube_videos
from ai_summary import summarize_posts_with_gpt

def start(update: Update, ctx):
    update.message.reply_text("NBA Bot: /scores | /reddit | /yt")

def scores(update, ctx):
    games = fetch_last_30_days_scores()
    save_to_csv(games)
    update.message.reply_text(f"Fetched {len(games)} games.")

def reddit_cmd(update, ctx):
    posts = fetch_reddit_posts()
    results, summary = analyze_sentiments(posts)
    msg = "\n".join(f"{r['title']} ({r['score']:+.2f})" for r in results)
    msg += f"\n\nOverall sentiment: {summary}"
    update.message.reply_text(msg[:4096])

def yt_cmd(update, ctx):
    vids = get_youtube_videos()
    msg = "\n".join(f"{v['title']} — https://youtu.be/{v['video_id']}" for v in vids)
    update.message.reply_text(msg)

def ai_cmd(update, ctx):
    posts = fetch_reddit_posts()
    summary = summarize_posts_with_gpt(posts)
    update.message.reply_text(summary[:4096])

def main():
    up = Updater(TELEGRAM_BOT_TOKEN)
    dp = up.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("scores", scores))
    dp.add_handler(CommandHandler("reddit", reddit_cmd))
    dp.add_handler(CommandHandler("yt", yt_cmd))
    dp.add_handler(CommandHandler("ai", ai_cmd))
    up.start_polling()
    up.idle()

if __name__ == "__main__":
    main()
