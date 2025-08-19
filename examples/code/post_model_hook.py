"""
Post model hook for the coding agent with interrupt functionality.
"""

from typing import Dict, Any
from langchain_core.messages import AIMessage
from langgraph.types import interrupt


def create_coding_agent_post_model_hook():
    """Create a post model hook for the coding agent with interrupt functionality."""
    
    def post_model_hook(state: Dict[str, Any]) -> Dict[str, Any]:
        """Post model hook that checks for tool calls and triggers interrupts if needed."""
        # Get the last message from the state
        messages = state.get("messages", [])
        if not messages:
            return state
        
        last_message = messages[-1]
        
        if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
            return state
        
        approved_tool_calls = []
        
        for tool_call in last_message.tool_calls:
            tool_name = tool_call.get("name", "")
            tool_args = tool_call.get("args", {})
            
            local_tools = {
                "ls", "read_file", "write_file", "edit_file", 
                "glob", "grep", "write_todos", "execute_bash"
            }
            
            if tool_name not in local_tools:
                approved_tool_calls.append(tool_call)
                continue
            
            question = f"Do you want to approve this command?\n\nCommand: {tool_name}\nArgs: {tool_args}\n\nRespond with True to approve or False to reject."
            
            is_approved = interrupt({
                "question": question,
                "command": tool_name,
                "args": tool_args
            })
            
            if is_approved:
                approved_tool_calls.append(tool_call)
            else:
                continue
        
        if len(approved_tool_calls) != len(last_message.tool_calls):
            new_message = AIMessage(
                content=last_message.content,
                tool_calls=approved_tool_calls,
                additional_kwargs=last_message.additional_kwargs
            )
            
            new_messages = messages[:-1] + [new_message]
            state["messages"] = new_messages
        
        return state
    
    return post_model_hook
