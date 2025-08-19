from flask import Flask, render_template
from modules.nba_predictions import get_nba_predictions
from modules.lakers_social import get_lakers_posts_and_sentiment
from modules.nba_highlights import get_youtube_highlights

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predictions')
def predictions():
    games = get_nba_predictions()
    return render_template('predictions.html', games=games)

@app.route('/lakers')
def lakers_feed():
    posts, summary = get_lakers_posts_and_sentiment()
    return render_template('lakers_feed.html', posts=posts, summary=summary)

@app.route('/highlights')
def highlights():
    videos = get_youtube_highlights()
    return render_template('highlights.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
