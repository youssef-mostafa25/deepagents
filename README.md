# Deep Agent

Using an LLM to call tools in a loop is the simplest form of an agent. 
This architecture, however, can yield agents that are “shallow” and fail to plan and act over longer, more complex tasks. 
Applications like “Deep Research”, “Manus, and “Claude Code” have gotten around this limitation by implementing a combination of four things:
a **planning tool**, **sub agents**, access to a **file system**, and a **detailed prompt**.

`deepagents` is a Python package that implements these in a general purpose way so that you can easily create a Deep Agent for your application.

## Installation

```bash
pip install deepagent
```

## Usage


A general-purpose AI agent built with LangGraph that includes two default tools:
1. **Sub-agent spawning**: Create new agent instances for handling subtasks
2. **Todo list management**: Organize tasks using a "replace entire state" pattern

## Features

- **General Purpose**: Handles a wide variety of tasks with Claude's capabilities
- **Sub-agent Delegation**: Spawn independent sub-agents for complex subtasks
- **Todo Management**: Built-in task tracking with priority and status management
- **Extensible**: Additional tools can be passed in at runtime
- **LangGraph Integration**: Built on LangGraph for robust state management

## Installation

```bash
pip install deepagent
```

Or you can install from source

```bash
pip install -e .
```

## Usage

See [examples/research](examples/research) for an example of how to use.

## Default Tools

### 1. Sub-agent Tool (`task`)

Spawns a new agent instance to handle specific subtasks:

```python
# The agent can use this internally like:
# def task(
#   description: str, 
#   subagent_type: str
# ):
```

### 2. Todo List Tool (`write_todos`)

Manages tasks with a replace-entire-state pattern:

```python
# The agent can use this internally like:
# def write_todos(
#     todos: list[Todo]
# )
```

Todo items have the following structure:
- `content`: Task description
- `status`: One of "pending", "in_progress", "completed"
