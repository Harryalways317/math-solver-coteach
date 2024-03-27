import asyncio
from functools import wraps

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
import diskcache as dc
from crew.math_analysis_crew import MathQuestionSearchCrew
from tools.vision_search import vision_api_request
from utils.cache_utils import cache_response

load_dotenv()
app = FastAPI()

cache = dc.Cache('./.cache')


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

@cache_response()
def generate_search_query(math_question: str):
    math_search_crew = MathQuestionSearchCrew(math_question)
    search_query = math_search_crew.run()
    return search_query
@cache_response()
def find_youtube_videos(math_question: str):
    math_search_crew = MathQuestionSearchCrew(math_question)
    search_query = math_search_crew.run()
    youtube_links = fetch_youtube_data(search_query)
    videos = extract_video_details(youtube_links)
    return videos
@cache_response()
def find_videos_to_the_question(math_question: str):
    youtube_links_for_question = fetch_youtube_data(math_question)
    videos = extract_video_details(youtube_links_for_question)
    return videos

class MathQuestion(BaseModel):
    question: str = ''
    image_url:str = ''

@app.post("/search_youtube/")
async def search_youtube_for_math_videos(math_question: MathQuestion):
    try:
        if math_question.image_url:
            math_question.question = vision_api_request(math_question.image_url)
            print(f'vision api question {math_question.question}')

        query = generate_search_query(math_question.question)
        print(f'Query {query}')
        videos = find_videos_to_the_question(query)
        videos_for_question = find_videos_to_the_question(math_question.question)
        if not videos and not videos_for_question:
            raise HTTPException(status_code=404, detail="No videos found")
        return {"videos": videos,'question_videos':videos_for_question,'query':query,'question':math_question.question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
