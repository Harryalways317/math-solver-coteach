from pydantic import BaseModel, HttpUrl, Field


class VideoDetail(BaseModel):
    url: HttpUrl = Field(..., description="The direct URL to the video on YouTube")
    thumbnail: HttpUrl = Field(..., description="The URL to the video's thumbnail image")
    title: str = Field(..., description="The title of the video")
    description: str = Field(..., description="The description of the video")
    author: str = Field(..., description="The title of the channel that published the video")

class Question(BaseModel):
    question: str = Field(..., description="The question to be asked")
    is_question: bool = Field(..., description="Is the input a question related to math or not")

