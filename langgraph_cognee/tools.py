from . import bootstrap  # noqa: F401
import cognee
import asyncio
from langchain_core.tools import tool
import logging
import threading
import concurrent.futures

logger = logging.getLogger(__name__)

# Create a dedicated background event loop
_loop = None
_loop_thread = None


def _start_background_loop():
    global _loop, _loop_thread
    if _loop is None:
        _loop = asyncio.new_event_loop()

        def run_loop():
            asyncio.set_event_loop(_loop)
            _loop.run_forever()

        _loop_thread = threading.Thread(target=run_loop, daemon=True)
        _loop_thread.start()


def _run_async(coro):
    """Run coroutine safely on a background event loop."""
    _start_background_loop()
    fut = asyncio.run_coroutine_threadsafe(coro, _loop)
    try:
        # Add timeout and better error handling
        result = fut.result(timeout=120)  # 120 second timeout
        logger.info("Async operation completed successfully")
        return result
    except concurrent.futures.TimeoutError:
        logger.error("Async operation timed out after 120 seconds")
        raise Exception("Operation timed out - check for deadlocks")
    except Exception as e:
        logger.error(f"Async operation failed with exception: {e}")
        import traceback

        traceback.print_exc()
        raise


_lock = asyncio.Lock()
_cognify_queue = asyncio.Queue()


async def _enqueue_cognify():
    global _lock, _cognify_queue

    if _lock.locked():
        if _cognify_queue.qsize() == 0:
            await _cognify_queue.put(None)
        return

    try:
        async with _lock:
            await cognee.cognify()
            while not _cognify_queue.empty():
                await _cognify_queue.get()
                await cognee.cognify()

    except Exception as e:
        logger.error(f"Error during cognify: {e}")
        while not _cognify_queue.empty():
            await _cognify_queue.get()
        raise


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
    logger.info(f"Adding data to cognee: {data}")
    _run_async(cognee.add(data))
    _run_async(_enqueue_cognify())
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
    result = _run_async(cognee.search(query_text, top_k=100))
    logger.info(f"Search results: {result}")
    return result


@tool
def list_data_entries_tool():
    """
    List all data entries in the knowledge base to find data IDs for deletion.

    Use this tool FIRST when you need to delete data. It automatically finds the default
    dataset and returns all data entries with their IDs. Look for the entries you want
    to delete and use their data_id with delete_data_entry_tool.

    Returns:
        list: List of data entries, each containing an ID and other metadata that you can use for deletion.
    """
    logger.info("Listing data entries in cognee")
    result = _run_async(cognee.datasets.list_data())

    logger.info("Getting dataset ID and listing data entries")
    result = _run_async(cognee.datasets.list_data())
    return result


@tool
def delete_data_entry_tool(data_id: str):
    """
    Delete a specific data entry from the knowledge base.

    Use this tool as the SECOND STEP in deletion. First use list_data_entries_tool
    to see all data entries and find the specific data_id you want to delete,
    then use this tool to delete that entry.

    Args:
        data_id (str): The specific data entry ID from list_data_entries_tool.

    Returns:
        str: Confirmation that the data entry was deleted.
    """
    logger.info(f"Deleting data entry from cognee: {data_id}")
    _run_async(cognee.delete(data_id))
    return f"Successfully deleted data entry: {data_id}"
