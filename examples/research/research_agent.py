import os
from typing import Literal

from tavily import TavilyClient


from claude_everything.graph import create_deep_agent



# Search tool to use to do research
def internet_search(query, max_results: int = 5, topic: Literal["general", "news", "finance"] = "general", include_raw_content: bool = False):
    """Run a web search"""
    tavily_async_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    search_docs = tavily_async_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic
        )
    return search_docs


# Prompt prefix to steer the agent to be an expert researcher
research_prompt_prefix = """You are an expert researcher. Your job is to write a through research report.

You have access to a few tools.

## `internet_search`

Use this to run an internet search for a given query. You can specify the number of results, the topic, and whether raw content should be included.
"""

# Create the agent
agent = create_deep_agent(
    [internet_search],
    research_prompt_prefix,
).with_config({"recursion_limit": 1000})
