import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def fetch_reddit_posts(query, limit=10):
    url = f"https://api.pushshift.io/reddit/search/submission/?q={query}&size={limit}&sort=desc"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print("Failed to fetch Reddit posts.")
        return []

def analyze_sentiments(posts):
    analyzer = SentimentIntensityAnalyzer()
    results = []
    for post in posts:
        title = post.get('title', '[No Title]')
        sentiment = analyzer.polarity_scores(title)
        results.append({'title': title, 'score': sentiment['compound']})
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    summary = "positive" if avg_score > 0 else "negative" if avg_score < 0 else "neutral"
    return results, summary
