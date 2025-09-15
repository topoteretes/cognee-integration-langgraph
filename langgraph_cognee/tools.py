from . import bootstrap # noqa: F401
import cognee
import asyncio
from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)

_shared_loop = asyncio.new_event_loop()

def _run_async(coro):
    """shared event loop"""
    return _shared_loop.run_until_complete(coro)

@tool
def add_tool(data: str):
    """
    Store information in the knowledge base for later retrieval.
    
    Use this tool whenever you need to remember, store, or save information 
    that the user provides. This is essential for building up a knowledge base 
    that can be searched later. Always use this tool when the user says things 
    like "remember", "store", "save", or gives you information to keep track of.

    Args:
        data (str): The text or information you want to store and remember.

    Returns:
        str: A confirmation message indicating that the item was added.
    """
    async def _add_and_cognify():
        await cognee.add(data)
        await cognee.cognify()
    
    logger.info(f"Adding data to cognee: {data}")
    _run_async(_add_and_cognify())
    return "Item added to cognee and processed"

@tool
def search_tool(query_text: str):
    """
    Search and retrieve previously stored information from the knowledge base.
    
    Use this tool to find and recall information that was previously stored.
    Always use this tool when you need to answer questions about information
    that should be in the knowledge base, or when the user asks questions
    about previously discussed topics.

    Args:
        query_text (str): What you're looking for, written as a natural language search query.

    Returns:
        list: A list of search results matching the query.
    """
    logger.info(f"Searching cognee for: {query_text}")
    result = _run_async(cognee.search(query_text))
    return result