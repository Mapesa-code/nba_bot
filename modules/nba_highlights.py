import requests
from datetime import datetime, timedelta
import os # <-- Import the os module

def get_youtube_highlights(max_results=5):
    # Retrieve the API key from environment variables
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    # Check if the API key exists
    if not YOUTUBE_API_KEY:
        print("Error: YOUTUBE_API_KEY environment variable not set!")
        # raise ValueError("YOUTUBE_API_KEY environment variable not set!")
        return [] # Return empty list to prevent crash

    YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"

    published_after = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ')

    search_url = f"{YOUTUBE_API_BASE_URL}/search"
    params = {
        'key': YOUTUBE_API_KEY,
        'part': 'snippet',
        'q': 'NBA highlights',
        'type': 'video',
        'order': 'date',
        'maxResults': max_results,
        'publishedAfter': published_after
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get('items', []):
            videos.append({
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            })
        return videos
    except Exception as e:
        print(f"Error fetching from YouTube: {e}")
        return []
