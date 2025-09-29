# Import core components
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
import asyncio
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

load_dotenv()


async def main():
    # Create an agent with memory capabilities
    memory = InMemorySaver()
    agent = create_react_agent("openai:gpt-4o-mini", tools=[], checkpointer=memory)

    agent.step_timeout = None

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="""
                    Hi, my name is Hasslebuff.
                """
                )
            ],
        }
    )
    print("=== FIRST RESPONSE ===")
    print(response["messages"][-1].content)

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="""
                    What is my name?
                """
                )
            ],
        }
    )

    # Create a fresh agent instance to avoid memory interference
    fresh_agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools=[],
    )

    response = fresh_agent.invoke(
        {
            "messages": [
                HumanMessage(content="What is my name?"),
            ],
        }
    )
    print("\n=== SECOND RESPONSE ===")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
