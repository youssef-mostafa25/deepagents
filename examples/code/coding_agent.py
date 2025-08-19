import os
import subprocess
import tempfile
import platform
import requests
from typing import List, Dict, Any, Optional, Union, Literal
from pathlib import Path

from tavily import TavilyClient
from deepagents import create_deep_agent, SubAgent
from utils import validate_command_safety
from subagents import code_reviewer_agent, debugger_agent, test_generator_agent

# Initialize Tavily client
try:
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
except KeyError:
    tavily_client = None

TARGET_DIRECTORY = "/Users/Desktop/test/langgraph"

def execute_bash(command: str, timeout: int = 30, cwd: str = None) -> Dict[str, Any]:
    """
    Execute bash/shell commands safely with prompt injection detection.

    Args:
        command: Shell command to execute
        timeout: Maximum execution time in seconds
        cwd: Working directory for command execution

    Returns:
        Dictionary with execution results including stdout, stderr, and success status
    """
    try:
        # First, validate command safety (focusing on prompt injection)
        safety_validation = validate_command_safety(command)
        
        # If command is not safe, return error without executing
        if not safety_validation.is_safe:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command blocked - safety validation failed:\nThreat Type: {safety_validation.threat_type}\nReasoning: {safety_validation.reasoning}\nDetected Patterns: {', '.join(safety_validation.detected_patterns)}",
                "return_code": -1,
                "safety_validation": safety_validation.model_dump()
            }
        
        # If command is safe, proceed with execution
        # Determine the appropriate shell based on platform
        if platform.system() == "Windows":
            shell_cmd = ["cmd", "/c", command]
        else:
            shell_cmd = ["bash", "-c", command]

        # Execute the command
        result = subprocess.run(
            shell_cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "safety_validation": safety_validation.model_dump()
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "return_code": -1,
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "return_code": -1,
        }


def http_request(
    url: str,
    method: str = "GET",
    headers: Dict[str, str] = None,
    data: Union[str, Dict] = None,
    params: Dict[str, str] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    Make HTTP requests to APIs and web services.

    Args:
        url: Target URL
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        headers: HTTP headers to include
        data: Request body data (string or dict)
        params: URL query parameters
        timeout: Request timeout in seconds

    Returns:
        Dictionary with response data including status, headers, and content
    """
    try:
        # Prepare request parameters
        kwargs = {"url": url, "method": method.upper(), "timeout": timeout}

        if headers:
            kwargs["headers"] = headers
        if params:
            kwargs["params"] = params
        if data:
            if isinstance(data, dict):
                kwargs["json"] = data
            else:
                kwargs["data"] = data

        # Make the request
        response = requests.request(**kwargs)

        # Try to parse JSON response, fallback to text
        try:
            content = response.json()
        except:
            content = response.text

        return {
            "success": response.status_code < 400,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": content,
            "url": response.url,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": 0,
            "headers": {},
            "content": f"Request timed out after {timeout} seconds",
            "url": url,
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "status_code": 0,
            "headers": {},
            "content": f"Request error: {str(e)}",
            "url": url,
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "headers": {},
            "content": f"Error making request: {str(e)}",
            "url": url,
        }

def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Search the web using Tavily for programming-related information."""
    if tavily_client is None:
        return {
            "error": "Tavily API key not configured. Please set TAVILY_API_KEY environment variable.",
            "query": query
        }
    
    try:
        search_docs = tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )
        return search_docs
    except Exception as e:
        return {
            "error": f"Web search error: {str(e)}",
            "query": query
        }

# Main coding agent instructions
coding_instructions = """You are an expert software developer and coding assistant. Your job is to help users with all aspects of programming across multiple languages including:

## Core Capabilities
- **Code Development**: Write clean, efficient, and well-documented code in any language
- **Problem Solving**: Break down complex problems into manageable solutions
- **Code Review**: Analyze and improve existing code across languages
- **Debugging**: Identify and fix bugs in any programming language
- **Testing**: Create comprehensive test suites using appropriate frameworks
- **Code Optimization**: Improve performance and efficiency
- **System Operations**: Handle build tools, package managers, and development environments

## Workflow
1. **Understand Requirements**: Carefully analyze what the user needs
2. **Plan Solution**: Break down the problem into steps
3. **Implement Code**: Write clean, well-documented code
4. **Test Code**: Verify functionality with comprehensive tests
5. **Review & Optimize**: Use sub-agents for code review and improvements

## Available Sub-Agents
- **code-reviewer**: For detailed code analysis and quality assessment across languages
- **debugger**: For identifying and fixing bugs in any programming language
- **test-generator**: For creating comprehensive test suites using appropriate frameworks

## Best Practices
- Write appropriate documentation for functions and classes
- Follow language-specific style guidelines and conventions
- Handle errors gracefully with appropriate exception handling
- Write meaningful variable and function names
- Use language-appropriate type systems when available
- Create comprehensive tests for your code

## Tools Available
- **execute_bash**: Run shell commands for compilation, testing, package management, etc. (All commands are validated for safety with focus on prompt injection detection using Claude before execution)
- **http_request**: Make API calls, download resources, interact with web services
- **web_search**: Search the web for programming documentation, tutorials, and solutions

## File Management
- Save code to appropriate files with correct extensions
- Organize projects with proper directory structure
- Create documentation files when needed (README.md, etc.)
- Use version control best practices

## Development Operations
You can handle:
- Building and compiling code (make, cmake, cargo build, etc.)
- Package management (npm, pip, gem, cargo, etc.)
- Running tests (pytest, jest, junit, go test, etc.)
- Code formatting (prettier, black, gofmt, etc.)
- Static analysis and linting
- Environment setup and configuration

## Web Search Usage
Use web_search to find:
- Programming language documentation and tutorials
- Framework-specific examples and best practices
- Error solutions and debugging help
- Latest library versions and installation guides
- Code examples and implementation patterns

## Safety Validation
All shell commands are automatically validated for safety before execution using Claude, with a focus on detecting prompt injection attempts and malicious commands. If a command is deemed unsafe, it will be blocked with a detailed explanation of the threat type and detected patterns. This ensures that only safe commands are executed on your local filesystem.
Always test your code using appropriate tools before presenting it to the user. If there are errors, use the debugger sub-agent to help identify and fix issues.

Remember: Quality code is more important than quick code. Take time to write clean, tested, and well-documented solutions."""

# Create the coding agent
agent = create_deep_agent(
    [execute_bash, http_request, web_search],
    coding_instructions,
    subagents=[code_reviewer_agent, debugger_agent, test_generator_agent],
    local_filesystem=True,
).with_config({"recursion_limit": 1000})
