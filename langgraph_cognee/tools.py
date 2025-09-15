import cognee
import asyncio
from langchain_core.tools import tool

class _CogneeLangGraphTools:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._dirty = False
        self._cognify_running = False

    @tool
    async def add(self, data: str):
        """
        Add data to the Cognee knowledge base.

        Use this tool when you want to insert new information into the database
        so it becomes available for future searches. Adding data will also
        trigger the background "cognify" process, which processes and indexes
        the knowledge base so that the new data is searchable.

        Args:
            data (str): The text or content you want to store in the database.

        Returns:
            str: A confirmation message indicating that the item was added.
        """
        await cognee.add(data)
        if not self._cognify_running:
            self._dirty = True
            self._cognify_running = True
            asyncio.create_task(self._run_cognify())
        return "Item added to the database"

    @tool
    async def search(self, query_text: str):
        """
        Search for information in the Cognee knowledge base.

        Use this tool when you want to look up items that were previously added
        and processed by the cognify pipeline. This is useful for retrieving
        facts, documents, or other stored knowledge relevant to the query.

        Args:
            query_text (str): The search query, written in natural language.

        Returns:
            list: A list of search results matching the query.
        """
        return await cognee.search(query_text)
    
    async def _run_cognify(self):
        """Run the cognify process"""
        self._cognify_running = True
        while self._dirty:
            self._dirty = False
            async with self._lock:
                await cognee.cognify()
        self._cognify_running = False

_cognee_langgraph_tools = _CogneeLangGraphTools()

add_tool = _cognee_langgraph_tools.add
search_tool = _cognee_langgraph_tools.search