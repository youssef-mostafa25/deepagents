from claude_everything.model import model
from claude_everything.prompts import TASK_DESCRIPTION
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool, BaseTool
from typing import TypedDict

class SubAgent(TypedDict):
    name: str
    description: str
    prompt: str
    tools: list[str]


def create_task_tool(tools, prompt_prefix, custom_agents: list[SubAgent]):
    agents = {
        "general-purpose": create_react_agent(
            model,
            prompt=prompt_prefix,
            tools=tools
        )
    }
    tools_by_name = {}
    for tool_ in tools:
        if not isinstance(tool_, BaseTool):
            tool_ = tool(tool_)
        tools_by_name[tool_.name] = tool_
    for _agent in custom_agents:
        agents[_agent['name']]: create_react_agent(
            model,
            prompt=_agent['prompt'],
            tools=[tools_by_name[t] for t in _agent['tools']]
        )

    other_agents_string = [f"- {_agent['name']}: {_agent['description']}" for _agent in custom_agents]

    @tool(description=TASK_DESCRIPTION.format(other_agents=other_agents_string))
    def task(description: str, subagent_type: str):
        if subagent_type not in agents:
            return f"Error: invoked agent of type {subagent_type}, the only allowed types are {[f'`{k}`' for k in agents]}"
        sub_agent = agents[subagent_type]
        result = sub_agent.invoke({
            "messages": [{"role": "user", "content": description}]
        })
        return result['messages'][-1].content

    return task
