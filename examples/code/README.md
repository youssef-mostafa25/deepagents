# 🧠💻 Deep Agents Coding Assistant

This example demonstrates how to build a comprehensive coding assistant using the `deepagents` framework. The coding agent can help with code development, debugging, testing, code review, and optimization.

## ✨ Features

The coding agent includes:

### 🔧 Core Tools
- **Code Execution**: Safely execute Python code in isolated environments
- **Syntax Validation**: Check Python syntax without execution
- **Unit Testing**: Run comprehensive test suites
- **Package Installation**: Install required Python packages

### 🤖 Sub-Agents
- **Code Reviewer**: Expert code analysis for quality, security, and best practices
- **Debugger**: Identify and fix bugs with systematic debugging
- **Test Generator**: Create comprehensive unit tests and test suites

### 🎯 Capabilities
- Write clean, well-documented Python code
- Debug and fix existing code issues
- Generate comprehensive test suites
- Perform code reviews and suggest improvements
- Install and manage dependencies
- Follow Python best practices and PEP 8

## 🚀 Quick Start

### Prerequisites

```bash
# Install the required packages
pip install -r requirements.txt

# Set up your API keys (the agent uses Claude by default)
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Basic Usage

```python
from coding_agent import agent

# Simple usage
result = agent.invoke({
    "messages": [{"role": "user", "content": "Create a function to calculate fibonacci numbers"}]
})

# Access created files
files = result.get("files", {})
for filename, content in files.items():
    print(f"File: {filename}")
    print(content)
```

### Interactive Demo

Run the interactive demo to see the agent in action:

```bash
python main.py
```

This will give you options to:
1. **Basic Demos**: See automated demonstrations of core capabilities
2. **Advanced Demo**: Watch the agent build a complex project
3. **Interactive Mode**: Chat directly with the coding agent

## 📁 Project Structure

```
examples/code/
├── coding_agent.py    # Main agent implementation
├── main.py           # Interactive demo script
├── requirements.txt  # Project dependencies
└── README.md        # This file
```

## 🛠️ How It Works

### Architecture

The coding agent is built using the `deepagents` framework with:

1. **Main Agent**: Orchestrates the overall coding workflow
2. **Sub-Agents**: Specialized agents for specific tasks
3. **Tools**: Core functionality for code execution and validation
4. **File System**: Virtual file system for code and data management

### Workflow

1. **Understand Requirements**: Analyze the user's coding request
2. **Plan Solution**: Break down complex problems into steps
3. **Implement Code**: Write clean, documented code
4. **Test & Validate**: Create and run comprehensive tests
5. **Review & Optimize**: Use sub-agents for quality assurance

### Sub-Agent Details

#### 🔍 Code Reviewer
- Analyzes code quality and adherence to best practices
- Checks for security vulnerabilities
- Suggests performance optimizations
- Validates documentation and comments
- Provides detailed feedback and ratings

#### 🐛 Debugger
- Interprets error messages and stack traces
- Identifies root causes of bugs
- Suggests specific fixes
- Tests solutions to verify they work
- Explains why issues occurred

#### 🧪 Test Generator
- Creates comprehensive unit tests
- Covers happy path, edge cases, and error conditions
- Uses appropriate testing frameworks (unittest, pytest)
- Generates meaningful test descriptions
- Ensures good test coverage

## 💡 Usage Examples

### Example 1: Algorithm Implementation

```python
task = """
Create a Python function to implement the quicksort algorithm.
Include proper error handling, type hints, docstrings, and comprehensive tests.
"""

result = agent.invoke({"messages": [{"role": "user", "content": task}]})
```

### Example 2: Debug Existing Code

```python
buggy_code = '''
def calculate_average(numbers):
    return sum(numbers) / len(numbers)  # Division by zero possible
'''

task = f"""
This code has potential bugs. Please analyze and fix:
{buggy_code}

Use the debugger sub-agent to identify issues and provide a robust solution.
"""

result = agent.invoke({"messages": [{"role": "user", "content": task}])
```

### Example 3: Code Review

```python
code_to_review = '''
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
'''

task = f"""
Please review this code for best practices and suggest improvements:
{code_to_review}

Use the code-reviewer sub-agent for detailed analysis.
"""

result = agent.invoke({"messages": [{"role": "user", "content": task}])
```

## 🎯 Best Practices Implemented

The coding agent follows and enforces these best practices:

### Code Quality
- **PEP 8 Compliance**: Follows Python style guidelines
- **Type Hints**: Uses appropriate type annotations
- **Docstrings**: Comprehensive documentation for functions and classes
- **Error Handling**: Proper exception handling and validation
- **Meaningful Names**: Clear, descriptive variable and function names

### Testing
- **Comprehensive Coverage**: Tests for normal cases, edge cases, and errors
- **Multiple Frameworks**: Supports unittest and pytest
- **Test Documentation**: Clear test descriptions and assertions
- **Automated Validation**: Runs tests automatically after implementation

### Security
- **Input Validation**: Validates user inputs and parameters
- **Safe Execution**: Isolates code execution in temporary environments
- **Dependency Management**: Careful package installation and management
- **Error Messages**: Avoids exposing sensitive information in errors

## 🔧 Customization

### Adding Custom Tools

You can extend the agent with additional tools:

```python
def my_custom_tool(param: str) -> str:
    """Custom tool description."""
    # Your implementation here
    return result

# Add to the agent
agent = create_deep_agent(
    [execute_python_code, validate_python_syntax, run_unit_tests, install_package, my_custom_tool],
    coding_instructions,
    subagents=[code_reviewer_agent, debugger_agent, test_generator_agent]
)
```

### Creating Custom Sub-Agents

```python
custom_subagent = {
    "name": "performance-optimizer",
    "description": "Specializes in optimizing code performance",
    "prompt": "You are an expert in Python performance optimization...",
    "tools": ["execute_python_code", "validate_python_syntax"]
}

agent = create_deep_agent(
    tools,
    coding_instructions,
    subagents=[code_reviewer_agent, debugger_agent, test_generator_agent, custom_subagent]
)
```

### Using Different Models

```python
from langchain_openai import ChatOpenAI

# Use GPT-4 instead of Claude
model = ChatOpenAI(model="gpt-4")
agent = create_deep_agent(
    tools,
    coding_instructions,
    subagents=subagents,
    model=model
)
```

## 🚀 Advanced Features

### Streaming Responses

```python
async def stream_coding_session():
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "Create a web scraper"}]},
        stream_mode="values"
    ):
        if "messages" in chunk:
            chunk["messages"][-1].pretty_print()
```

### File System Integration

The agent maintains a virtual file system that you can interact with:

```python
# Pass initial files
result = agent.invoke({
    "messages": [{"role": "user", "content": "Refactor the code in main.py"}],
    "files": {"main.py": "# Your existing code here"}
})

# Access created/modified files
created_files = result["files"]
```

### Human-in-the-Loop

```python
# Add human feedback during execution
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Create a REST API"}]},
    config={
        "callbacks": [HumanApprovalCallbackHandler()],
        "recursion_limit": 1000
    }
)
```

## 🤝 Contributing

This is an example implementation that can be extended and improved. Some ideas for enhancements:

- **Language Support**: Add support for other programming languages
- **IDE Integration**: Create plugins for popular IDEs
- **Code Metrics**: Add tools for measuring code complexity and quality
- **Documentation Generation**: Automated API documentation creation
- **Deployment Tools**: Add deployment and CI/CD integration
- **Database Integration**: Tools for database schema and query optimization

## 📝 License

This example is part of the `deepagents` project and follows the same license terms.

## 🆘 Support

If you encounter issues or have questions:

1. Check the [main deepagents documentation](../../README.md)
2. Look at the example code and comments
3. Try the interactive demo mode to experiment
4. Create an issue in the main deepagents repository

---

**Happy Coding with Deep Agents! 🧠🤖💻**