#
# Not needed for the current implementation as searching youtube is enough, exposed by Google YouTube API
#


import json
import os

import requests
from langchain.tools import tool
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun



import diskcache as dc

cache = dc.Cache('./.cache')

from dotenv import load_dotenv
load_dotenv()

class SearchTools():
    ddg_search = DuckDuckGoSearchRun()
    # llm = AzureChatOpenAI(model="gpt-4-32k", deployment_name="hom-gpt-4")
    llm = AzureChatOpenAI(model="gpt-3.5-turbo-0125", deployment_name="hom-gpt-4")

    @staticmethod
    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet
    about a a given topic and return relevant results"""
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
