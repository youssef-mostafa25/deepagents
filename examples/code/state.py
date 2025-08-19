from deepagents.state import DeepAgentState
from typing import Dict, Set, NotRequired
from typing_extensions import TypedDict

class CodingAgentState(DeepAgentState):
    """Extended state for coding agent with approval operation caching."""
    approved_operations: NotRequired[Dict[str, Set[str]]]
