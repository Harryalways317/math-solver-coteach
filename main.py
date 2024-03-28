import asyncio
from functools import wraps
from typing import List, Dict, Any


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
import diskcache as dc

from agents.math_analysis_agent import YouTubeSearchAgent
from crew.math_analysis_crew import MathQuestionSearchCrew, YouTubeSearchCrew
from tools.vision_search import vision_api_request
from utils.cache_utils import cache_response
from openai import OpenAI


load_dotenv()
app = FastAPI()

cache = dc.Cache('./.cache')
client = OpenAI()


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
def fetch_yt_data(search_query: str,question:str):
    yt_crew = YouTubeSearchCrew(search_query,question)
    data = yt_crew.run()
    print(f'yt data {data}')
    return data
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
    chat_id:str = ''


def update_chat_history(chat_id: str, user_input: str = '', assistant_response: str = ''):
    if not chat_id:
        return None

    history = cache.get(chat_id, [])

    if user_input:
        history.append({"user": user_input})
    if assistant_response:
        history.append({"assistant": assistant_response})

    cache.set(chat_id, history)
    return history

async def generate_llm_response(context: str,history:str,videos:List) -> str:
    print(history)
    gpt_history = []
    for entry in history:
        if 'user' in entry:
            gpt_history.append({"role": "user", "content": entry['user']})
        if 'assistant' in entry:
            gpt_history.append({"role": "assistant", "content": entry['assistant']})
    print([
            {"role": "system", "content": "You are a helpful math assistant."},
            {"role": "user", "content": "I am struggling with an algebra question."},
            {"role": "assistant", "content": """
            Sure, what would you like me to help you with?
            Here are some basic algebra videos that you consider watching to get better at it:

            1. [Algebra Basics: What Is Algebra? - Math Antics](https://www.youtube.com/watch?v=NybHckSEQBI)
            2. [Evaluate Expressions with Variables | Find the Value of an Expression](https://www.youtube.com/watch?v=DOKiZfX9ePk&list=PLiT3pCvK_cfVYLO03dJFgyv3D6-EhXEAU)
            """},
            *gpt_history,
            {"role": "user", "content": f"{context}"},
            {"role": "user", "content": f"These are the relevant videos {videos} regarding my question you can include in prompt"}
        ])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful math assistant who returns relevant videos regarding the question in the order of most relavent first, but dont solve it.if you get an exact match then prioritize it first, if its a conversation question then handle accordingly"},
            {"role": "user", "content": "I am struggling with an algebra question."},
            {"role": "assistant", "content": """
            Sure, what would you like me to help you with?
            Here are some basic algebra videos that you consider watching to get better at it:

            1. [Algebra Basics: What Is Algebra? - Math Antics](https://www.youtube.com/watch?v=NybHckSEQBI)
            2. [Evaluate Expressions with Variables | Find the Value of an Expression](https://www.youtube.com/watch?v=DOKiZfX9ePk&list=PLiT3pCvK_cfVYLO03dJFgyv3D6-EhXEAU)
            """},
            {"role": "user", "content": "thanks for helping me with the videos"},
            {"role": "assistant", "content": "You're welcome! Let me know if you have any other questions."},
            *gpt_history,
            {"role": "user", "content": f"{context}"},
            {"role": "user", "content": f"These are the relevant videos  regarding my question you can include in prompt {videos}"}
        ]
    )
    print(f'response {response}')

    print(response.choices[0].message)
    return response.choices[0].message.content


async def handle_conversation(session_id,user_input,video_data):
    history = update_chat_history(session_id, user_input=user_input)

    prompt = f"{user_input}"

    # Generate the model's response
    llm_response = await generate_llm_response(prompt,history,video_data)
    print(f'LLM response {llm_response}')

    # Update the chat history with the model's response
    history = update_chat_history(session_id, assistant_response=llm_response)

    return llm_response,history


@app.post("/search_youtube/")
async def search_youtube_for_math_videos(math_question: MathQuestion):
    try:
        if math_question.image_url:
            math_question.question = vision_api_request(math_question.image_url)
            print(f'vision api question {math_question.question}')

        query_response = generate_search_query(math_question.question)
        query = query_response.get('question', '')
        is_math_question = query_response.get('is_question', False)
        print(f'Query {query}')
        videos = find_videos_to_the_question(query)
        videos_for_question = find_videos_to_the_question(math_question.question)
        if not videos and not videos_for_question:
            raise HTTPException(status_code=404, detail="No videos found")
        return {"videos": videos,'question_videos':videos_for_question,'query':query,'question':math_question.question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search_youtube_chat/")
async def search_youtube_for_math_videos(math_question: MathQuestion):
    try:
        history = []
        if math_question.chat_id:
            history = cache.get(math_question.chat_id, [])
            print(f'History {history}')
        if math_question.image_url:
            math_question.question = vision_api_request(math_question.image_url)
            print(f'vision api question {math_question.question}')

        # history.append({"user": math_question.question})
        # cache.set(key=math_question.chat_id,value=history)
        query_response = generate_search_query(math_question.question)
        query = query_response.get('question', '')
        is_math_question = query_response.get('is_question', False)
        print(f'Query {query}')
        res_videos = []
        if is_math_question:
            videos =  find_videos_to_the_question(query)
            videos_for_question =  find_videos_to_the_question(math_question.question)
            print(f'lenght of videos {len(videos)} and videos for question {len(videos_for_question)}')
            if not videos and not videos_for_question:
                raise HTTPException(status_code=404, detail="No videos found")
            res_videos = list(videos) + list(videos_for_question)
        res,history = await handle_conversation(math_question.chat_id,math_question.question,res_videos)
        return {'response': res,"history":history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/yt/")
# async def search_youtube_for_math_videos(math_question: MathQuestion):
#     try:
#         if math_question.image_url:
#             math_question.question = vision_api_request(math_question.image_url)
#             print(f'vision api question {math_question.question}')
#
#         query = generate_search_query(math_question.question)
#         print(f'Query {query}')
#         videos = fetch_yt_data(query,math_question.question)
#         print(f'videos {videos}')
#         if not videos:
#             raise HTTPException(status_code=404, detail="No videos found")
#         return {"videos": videos,'query':query,'question':math_question.question}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
