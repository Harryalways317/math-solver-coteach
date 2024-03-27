import json
from crewai import Crew

from agents.math_analysis_agent import MathQuestionAnalysisAgent, YouTubeSearchAgent
from tasks.math_analysis_task import MathQuestionSearchTask, FetchYouTubeLinksTask


class MathQuestionSearchCrew:
    def __init__(self, math_question):
        self.math_question = math_question
        self.agent = MathQuestionAnalysisAgent().math_question_to_query_agent()
        self.task = MathQuestionSearchTask().create_search_query_task(self.agent, math_question)

    def run(self):
        crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            verbose=True
        )
        result = crew.kickoff()
        if type(result) == dict:
            return result
        return json.loads(result)
class YouTubeSearchCrew:
    def __init__(self, search_query):
        self.search_query = search_query
        self.agent = YouTubeSearchAgent().create_youtube_search_agent()
        self.task = FetchYouTubeLinksTask().create_youtube_links_fetch_task(self.agent, search_query)

    def run(self):
        crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            verbose=True
        )
        result = crew.kickoff()
        if isinstance(result, dict):
            return result
        return json.loads(result)