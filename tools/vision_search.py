import base64
import os
from io import BytesIO

import openai
import requests
from PIL import Image
from openai import OpenAI, OpenAIError,AsyncOpenAI
import diskcache as dc
from functools import wraps
import json
import dotenv

from utils.cache_utils import cache_response

dotenv.load_dotenv()

print(openai.api_key)
print(os.getenv("OPENAI_API_KEY"))
print("openai.api_key")
cache = dc.Cache("cache")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def download_and_encode_image(image_url, max_image=512):
    """
    Downloads an image from a URL, optionally resizes it, and converts to base64.

    Parameters:
    - image_url: URL of the image to download.
    - max_image: Maximum dimension to allow for resizing.

    Returns:
    - Base64 encoded string of the image.
    """

    """
    Just doing this cuz, i dont have trust giving urls directly to the openai api, as it will definately fail
    """


    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        print(f"Downloaded image from {image_url}")
        print(f"response.content {response.content[:100]}")
        img = Image.open(BytesIO(response.content))

        width, height = img.size

        # Convert the image to PNG and encode to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print(f'img_str {img_str[:100]}')
        return img_str
    else:
        raise Exception(f"Failed to download image: HTTP status code {response.status_code}")


@cache_response()
def vision_api_request(image_url, model="gpt-4-vision-preview",prompt='Extract the question as it is in the image, only return the question without any other text'):
    """
    Makes a vision API request using the specified model.

    Parameters:
    - image_url: The URL of the image to analyze.
    - model: The model to use for the vision API request.
    """
    try:
        encoded_string = download_and_encode_image(image_url)
        print(f'model {model}')
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url":
                                              f"data:image/jpeg;base64,{encoded_string}"},
                        },
                    ],
                }
            ],
            max_tokens=1500,
        )
        print("Vision API Request Successful")
        print(response)
        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None
