import requests
from datetime import datetime, timedelta

def get_youtube_highlights(max_results=5):
    YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your YouTube Data API v3 key
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
