import feedparser
import requests
from textblob import TextBlob
import statistics

def get_lakers_posts_and_sentiment(limit=5):
    posts = []
    subreddits = ['lakers', 'nba']
    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/search.rss?q=lakers&restrict_sr=on&sort=new&t=week"
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if len(posts) < limit:
                posts.append({
                    'title': entry.title,
                    'url': entry.link,
                    'source': f'r/{sub}'
                })
    
    if not posts:
        return [], {}

    # Sentiment Analysis
    sentiments = []
    for post in posts:
        blob = TextBlob(post['title'])
        post['sentiment'] = blob.sentiment.polarity
        sentiments.append(blob.sentiment.polarity)

    avg_sentiment = statistics.mean(sentiments)
    
    if avg_sentiment > 0.1:
        overall_sentiment = "Positive"
    elif avg_sentiment < -0.1:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    summary = {
        'average': f"{avg_sentiment:.2f}",
        'overall': overall_sentiment
    }
    
    return posts, summary
