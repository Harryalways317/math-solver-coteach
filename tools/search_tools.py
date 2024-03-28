import json
import os

import requests
from langchain.tools import tool
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper


import diskcache as dc

cache = dc.Cache('./.cache')

from dotenv import load_dotenv
load_dotenv()

class SearchTools():
    ddg_search = DuckDuckGoSearchRun()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    # llm = AzureChatOpenAI(model="gpt-4-32k", deployment_name="hom-gpt-4")
    llm = AzureChatOpenAI(model="gpt-3.5-turbo-0125", deployment_name="hom-gpt-4")

    @staticmethod
    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet
    about a a given topic and return relevant results"""
        # top_result_to_return = 4
        # url = "https://google.serper.dev/search"
        # payload = json.dumps({"q": query})
        # headers = {
        #     'X-API-KEY': os.environ['SERPER_API_KEY'],
        #     'content-type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        # # check if there is an organic key
        # if 'organic' not in response.json():
        #   return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
        # else:
        #   results = response.json()['organic']
        #   string = []
        #   for result in results[:top_result_to_return]:
        #     try:
        #       string.append('\n'.join([
        #           f"Title: {result['title']}", f"Link: {result['link']}",
        #           f"Snippet: {result['snippet']}", "\n-----------------"
        #       ]))
        #     except KeyError:
        #       next
        #
        #   return '\n'.join(string)
        cache_key = f"search_results_{query}"

        # Check if the search results are already in the cache
        if cache_key in cache:
            print(f"Cache hit for query: {query}")
            return cache.get(cache_key)
        results = SearchTools.ddg_search.run(query)
        print(f'DuckDuckGo results: {results}')
        # Cache the results before returning
        cache.set(cache_key, results)
        return results

    @staticmethod
    @tool("Search the wikipedia")
    def search_wikipedia(query):
        """Useful to search the internet
    about a a given topic and return relevant results"""
        # top_result_to_return = 4
        # url = "https://google.serper.dev/search"
        # payload = json.dumps({"q": query})
        # headers = {
        #     'X-API-KEY': os.environ['SERPER_API_KEY'],
        #     'content-type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        # # check if there is an organic key
        # if 'organic' not in response.json():
        #   return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
        # else:
        #   results = response.json()['organic']
        #   string = []
        #   for result in results[:top_result_to_return]:
        #     try:
        #       string.append('\n'.join([
        #           f"Title: {result['title']}", f"Link: {result['link']}",
        #           f"Snippet: {result['snippet']}", "\n-----------------"
        #       ]))
        #     except KeyError:
        #       next
        #
        #   return '\n'.join(string)
        results = SearchTools.wikipedia.run(query)
        return results

    def clean_search_query(query: str) -> str:
        # Some search tools (e.g., Google) will
        # fail to return results if query has a
        # leading digit: 1. "LangCh..."
        # Check if the first character is a digit
        if query[0].isdigit():
            # Find the position of the first quote
            first_quote_pos = query.find('"')
            if first_quote_pos != -1:
                # Extract the part of the string after the quote
                query = query[first_quote_pos + 1:]
                # Remove the trailing quote if present
                if query.endswith('"'):
                    query = query[:-1]
        return query.strip()

    def process_context(query, context):
        prompt = f"Considering the query '{query}' and the provided context '{context}', please analyze and summarize the information. " \
                 "Based on the analysis, generate a brief description or answer relevant to the query. " \
                 "Additionally, list any sources or references used in your response."
        res = SearchTools.llm.invoke(prompt)
        print("Response from GPT-4")
        print(res)
        return res

    # @staticmethod
    # @tool("Search the internet")
    # def search_internet(query):
    #     """Useful to search the internet about a given topic and return relevant results"""
    #     cleaned_query = SearchTools.clean_search_query(query)
    #     whoggle_service = WhoggleService()
    #     context = whoggle_service.run(cleaned_query)
    #     print("Context:")
    #     print(context)
    #     processed_context = SearchTools.process_context(query, context)
    #     return processed_context
