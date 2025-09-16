# Import core components
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langchain_core.messages import HumanMessage
from langgraph_cognee import add_tool, search_tool, list_data_entries_tool, delete_data_entry_tool
from examples.utils.fs_util_tools import list_path_contents_tool, read_file_tool
import asyncio
import cognee
from dotenv import load_dotenv
import os
from cognee.modules.search.types import SearchType
load_dotenv()

async def main():
    from cognee.api.v1.config import config
    
    config.data_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/data_storage")
    )

    config.system_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/system")
    )

    # Set up storage
    store = InMemoryStore(
        index={
            "dims": 1536,
            "embed": "openai:text-embedding-3-small",
        }
    )


    # Create an agent with memory capabilities
    agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools=[
            add_tool,
            search_tool,
            list_data_entries_tool,
            delete_data_entry_tool,
            read_file_tool,
            list_path_contents_tool,
        ],
        store=store,
    )

#     response = agent.invoke(
#         {
#             "messages": [
#                 HumanMessage(content="""STEP 1: Use list_path_contents_tool to find all files in '/Users/daulet/Desktop/dev/langgraph-cognee/examples/data' directory.
# STEP 2: For each .txt file found, use read_file_tool to read its content.
# STEP 3: For each file content you read, MUST use add_tool to store it in the knowledge base.
# STEP 4: After adding all files, confirm all data was stored by using add_tool for each file's content."""),
#             ],
#         }
#     )
#     print("=== FIRST RESPONSE ===")
#     print(response["messages"][-1].content)

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(content="Using search tool, give me an overview of our contracts - how many we have, what is the total amount of money we have received from them, what is the total number of active contracts we have."),
            ],
        }
    )
    print("\n=== SECOND RESPONSE ===")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())