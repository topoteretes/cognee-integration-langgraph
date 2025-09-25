# Import core components
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langgraph_cognee import get_sessionized_cognee_tools
import asyncio
from dotenv import load_dotenv
import os
import cognee

load_dotenv()


async def main():
    from cognee.api.v1.config import config

    config.data_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/data_storage")
    )

    config.system_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/system")
    )

    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    add_tool, search_tool = get_sessionized_cognee_tools('daulet-test-user')
    
    # Create an agent with memory capabilities
    agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools=[
            add_tool,
            search_tool,
        ],
    )

    agent.step_timeout = None

    # """
    #     # Step 1. open file and read the content + add to cognee
    # """
    # data_dir = os.path.join(os.path.dirname(__file__), "data")
    # for filename in os.listdir(data_dir):
    #     if filename.endswith(".txt"):
    #         file_path = os.path.join(data_dir, filename)
    #         with open(file_path, "r") as f:
    #             content = f.read()
    #             await cognee.add(content)
    # await cognee.cognify()

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="""
                    We have signed a contract with the following company: "Meditech Solutions". Company is in the healthcare industry. Start date is Jan 2023 and end date is Dec 2025. Contract value is £1.2M.
                """
                ),
                HumanMessage(
                    content="""
                    We have signed a contract with the following company: "QuantumSoft". Company is in the technology industry. Start date is Aug 2024 and end date is Aug 2028. Contract value is £5.5M.
                """
                ),
                HumanMessage(
                    content="""
                    We have signed a contract with the following company: "Orion Retail Group". Company is in the retail industry. Start date is Mar 2024 and end date is Mar 2026. Contract value is £850K.
                """
                ),
            ],
        }
    )
    """
        Do a research on the following topic: "What contracts are in the healthcare industy?"
    """
    # Create a fresh agent instance to avoid memory interference
    fresh_agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools=[
            add_tool,
            search_tool,
        ],
    )

    response = fresh_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="I need to research our contract portfolio. Can you search for any contracts we have with companies in the healthcare industry? Please use the search functionality to find this information."
                ),
            ],
        }
    )
    print("\n=== SECOND RESPONSE ===")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
