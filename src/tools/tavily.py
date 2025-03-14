from langchain_community.tools.tavily_search import TavilySearchResults
from typing import TypedDict


class TavilySearchResult(TypedDict):
    url: str
    content: str


class Tavily:
    def search(self, query: str) -> list[TavilySearchResult]:
        """
        Searches profile urls like LinkedIn or Twitter of a user
        Args:
            query(str): Search query
        Returns:
            list[TavilySearchResult]:
                - url(str)
                - content(str)
        """
        tsr = TavilySearchResults(
            max_results=1,
        )
        res = tsr.invoke(query)
        print("tavily>>", res)
        return res
