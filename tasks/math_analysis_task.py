from textwrap import dedent
from crewai import Task

from models.video_detail import VideoDetail


class MathQuestionSearchTask:
    def create_search_query_task(self, agent, math_question):
        print(f"Creating search query task for math question: {math_question}")
        print(f"Agent: {agent}")
        return Task(
            description=dedent(f"""
                Objective: Transform the provided math question into a search query optimized for YouTube. 
                If the question provided is not a math question but a doubt or help, analyse that and provide a search query that can help the user to find the answer.
                if the equations provided are incomplete or incorrectly formatted, try to generated the best one possible.
                If it is off topic then tell the user it is off topic
                The query should be clear, concise, and designed to return relevant educational content that answers the question.
                Math Question: {math_question}
                """),
            agent=agent,
            expected_output="A string representing the YouTube search query.",
            verbose=True
        )
class FetchYouTubeLinksTask:
    def create_youtube_links_fetch_task(self, agent, search_query,question):
        query = {
                "search_query": {search_query},
                "question": {question},
                }
        return Task(
            description=dedent(f"""
                Objective: Fetch relevant YouTube video links based on the provided search query and direct question and get the relevant top 5 from retrived data
                This involves utilizing search tools to query YouTube (or the internet for YouTube links) and extract URLs of videos that best match the search criteria.
                Input Data: 
                ```json
                {query}
                ```
                """),
            agent=agent,
            expected_output="A list of YouTube video links relevant to the search query.",
            output_json=VideoDetail,
            verbose=True
        )