# Import core components
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langchain_core.messages import HumanMessage
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langgraph_cognee import add_tool, search_tool

from dotenv import load_dotenv
load_dotenv()

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
    ],
    store=store,
)

response = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="Please store this important information: Our biggest clients in order of importance are: 1. Google, 2. Apple, 3. Microsoft, 4. Amazon, 5. Meta, 6. Tesla, and 7. SpaceX. Make sure to save this so you can reference it later."
            ),
            HumanMessage(
                content="Who is our biggest client? Please search for the client information I just gave you."
            ),
        ],
        "config": {
            "callbacks": [
                ConsoleCallbackHandler()
            ]
        }
    }
)

print(response["messages"][-1].content)
