# Coding Agent with Safety Validation

This is a specialized coding agent that includes automatic safety validation for shell commands using Claude via LangChain.

## File Structure

- `coding_agent.py` - Main agent implementation with tools and sub-agents
- `utils.py` - Safety validation utilities and command validation logic
- `main.py` - CLI interface for the coding agent
- `requirements.txt` - Python dependencies

## Features

- **Automatic Command Safety Validation**: All shell commands are validated by Claude before execution
- **Prompt Injection Detection**: Specifically detects prompt injection attempts and malicious commands
- **Comprehensive Tool Set**: File operations, HTTP requests, web search, and shell execution
- **Specialized Sub-Agents**: Code review, debugging, and test generation
- **Local Filesystem Support**: Works with real filesystem operations

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export TAVILY_API_KEY="your_tavily_api_key"
   export ANTHROPIC_API_KEY="your_anthropic_api_key"
   ```

3. **Run the Agent**:
   ```bash
   python main.py
   ```

## Safety Validation

The agent automatically validates all shell commands before execution using Claude. This includes:

- **Prompt Injection Detection**: Identifies attempts to manipulate the AI system
- **Malicious Command Detection**: Detects commands designed to harm the system
- **System Exploitation**: Reviews commands that try to exploit vulnerabilities

### Threat Types

- **PROMPT_INJECTION**: Attempts to manipulate the AI system through commands
- **MALICIOUS_COMMAND**: Commands designed to harm the system or steal data
- **SAFE**: Commands that are safe to execute

## Available Tools

- `execute_bash`: Execute shell commands (with safety validation)
- `http_request`: Make HTTP requests to APIs and web services
- `web_search`: Search the web for programming information
- `write_file`: Create and write to files
- `read_file`: Read file contents
- `edit_file`: Modify existing files
- `ls`: List directory contents
- `write_todos`: Manage task tracking

## Sub-Agents

- **Code Reviewer**: Analyzes code for quality, security, and best practices
- **Debugger**: Helps identify and fix bugs in any programming language
- **Test Generator**: Creates comprehensive test suites

## Example Usage

```python
from coding_agent import agent

# The agent will automatically validate all shell commands
# before execution and provide detailed safety assessments
```

## API Keys

- **TAVILY_API_KEY**: Required for web search functionality
- **ANTHROPIC_API_KEY**: Required for command safety validation

Both keys are optional but recommended for full functionality. Without the Anthropic API key, all shell commands will be blocked for safety.
