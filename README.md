# LangGraph Integration Cognee

A powerful integration between LangGraph and Cognee that provides intelligent knowledge management and retrieval capabilities for AI agents.

## Overview

LangGraph Integration Cognee combines the workflow orchestration capabilities of LangGraph with Cognee's advanced knowledge storage and retrieval system. This integration allows you to build AI agents that can efficiently store, search, and retrieve information from a persistent knowledge base.

## Features

- **Smart Knowledge Storage**: Add and persist information using Cognee's advanced indexing
- **Semantic Search**: Retrieve relevant information using natural language queries
- **Session Management**: Support for user-specific data isolation
- **LangGraph Integration**: Seamless integration with LangGraph's agent framework
- **Async Support**: Built with async/await for high-performance applications

## Installation

```bash
# Using uv (recommended)
uv add langgraph-integration-cognee

# Using pip
pip install langgraph-integration-cognee
```

## Available Tools

### `get_sessionized_cognee_tools(session_id: str = None)`
Returns sessionized cognee tools for isolated data management.

**Returns:** `(add_tool, search_tool)` - A tuple of tools for storing and searching data

### Individual Tools
- **`add_tool`**: Store information in the knowledge base
- **`search_tool`**: Search and retrieve previously stored information

## Session Management

LangGraph Integration Cognee supports user-specific sessions to isolate data between different users or contexts:

```python
from langgraph_integration_cognee import get_sessionized_cognee_tools

# Create tools for specific user sessions
user1_tools = get_sessionized_cognee_tools("user-123")
user2_tools = get_sessionized_cognee_tools("user-456")

# Each user will have their own isolated knowledge base
```

## Configuration

Make sure to set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or use a `.env` file:

```env
OPENAI_API_KEY=your-api-key-here
```

## Examples

Check out the `examples/` directory for more comprehensive usage examples:

- `examples/example.py`: Complete workflow with contract management
- `examples/guide.ipynb`: Jupyter notebook tutorial with step-by-step guidance

## Requirements

- Python 3.12+
- OpenAI API key
- Dependencies automatically managed via pyproject.toml