import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool

from utils.cache_utils import cache_response

load_dotenv()

class YouTubeSearchTools():
    @staticmethod
    @cache_response()
    def fetch_youtube_data(search_query: str):
        api_key = os.getenv("YOUTUBE_API_KEY")
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'maxResults': 5,
            'q': search_query,
            'type': 'video',
            'key': api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data", "statusCode": response.status_code, "message": response.text}

    @staticmethod
    @cache_response()
    def extract_video_details(data):
        videos = []
        for item in data.get('items', []):
            video_id = item.get('id', {}).get('videoId', '')
            title = item.get('snippet', {}).get('title', '')
            description = item.get('snippet', {}).get('description', '')
            channel_title = item.get('snippet', {}).get('channelTitle', '')
            thumbnail_url = item.get('snippet', {}).get('thumbnails', {}).get('high', {}).get('url', '')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                'url': video_url,
                'thumbnail': thumbnail_url,
                'title': title,
                'description': description,
                'author': channel_title
            })
        return videos

    @staticmethod
    @tool("Fetch YouTube Videos")
    def search_youtube(search_query):
        """Useful to search YouTube for videos related to a given topic and return relevant results"""
        data = YouTubeSearchTools.fetch_youtube_data(search_query)
        if "error" in data:
            return f"Error fetching YouTube data: {data['message']}"
        videos = YouTubeSearchTools.extract_video_details(data)
        return videos
