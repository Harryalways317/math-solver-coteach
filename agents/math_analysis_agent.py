import os

import requests
from crewai import Agent

from tools.search_tools import SearchTools
from tools.youtube_search import YouTubeSearchTools


class MathQuestionAnalysisAgent:
    def math_question_to_query_agent(self):
        """Agent dedicated to converting math questions into YouTube search queries."""
        return Agent(
            role='Math Question Analysis Agent',
            goal='To convert a given math question into a concise, search-friendly query for YouTube.',
            backstory='Armed with a deep understanding of mathematical terminology and the nuances of search engine optimization, this agent excels at translating complex math questions into effective search queries.',
            tools=[],
            verbose=True
        )
class YouTubeSearchAgent:
    def create_youtube_search_agent(self):
        """Agent dedicated to fetching YouTube video links based on search queries."""
        return Agent(
            role='YouTube Search Agent',
            goal='To fetch relevant YouTube video links based on a provided search query and the question. ',
            backstory='Expert in navigating digital content, this agent leverages search engine capabilities to sift through the web and pinpoint YouTube videos that best match the search criteria. the param for function is query',
            tools=[YouTubeSearchTools.search_youtube],
            verbose=True
        )


