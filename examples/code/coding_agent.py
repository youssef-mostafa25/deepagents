import os
import subprocess
import tempfile
import ast
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

from deepagents import create_deep_agent, SubAgent


def execute_python_code(code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute Python code safely in a temporary environment.
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Dictionary with execution results including stdout, stderr, and success status
    """
    try:
        # Create a temporary file to execute the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Execute the code
            result = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Code execution timed out after {timeout} seconds",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Error executing code: {str(e)}",
            "return_code": -1
        }


def validate_python_syntax(code: str) -> Dict[str, Any]:
    """
    Validate Python code syntax without executing it.
    
    Args:
        code: Python code to validate
        
    Returns:
        Dictionary with validation results
    """
    try:
        ast.parse(code)
        return {
            "valid": True,
            "error": None
        }
    except SyntaxError as e:
        return {
            "valid": False,
            "error": f"Syntax error at line {e.lineno}: {e.msg}"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": f"Parse error: {str(e)}"
        }


def run_unit_tests(test_code: str, main_code: str = "") -> Dict[str, Any]:
    """
    Run unit tests for the provided code.
    
    Args:
        test_code: Unit test code (using unittest or pytest)
        main_code: Main code to test (optional, can be imported)
        
    Returns:
        Dictionary with test results
    """
    try:
        # Combine main code and test code
        full_code = f"{main_code}\n\n{test_code}" if main_code else test_code
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(full_code)
            temp_file_path = temp_file.name
        
        try:
            # Try to run with unittest first
            result = subprocess.run(
                [sys.executable, '-m', 'unittest', temp_file_path.replace('.py', '').split('/')[-1]],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.path.dirname(temp_file_path)
            )
            
            if result.returncode != 0:
                # If unittest fails, try running the file directly
                result = subprocess.run(
                    [sys.executable, temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
                "return_code": result.returncode
            }
            
        finally:
            os.unlink(temp_file_path)
            
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "errors": f"Error running tests: {str(e)}",
            "return_code": -1
        }


def install_package(package_name: str) -> Dict[str, Any]:
    """
    Install a Python package using pip.
    
    Args:
        package_name: Name of the package to install
        
    Returns:
        Dictionary with installation results
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package_name],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "errors": "Package installation timed out",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "errors": f"Error installing package: {str(e)}",
            "return_code": -1
        }


# Sub-agent for code review and analysis
code_reviewer_prompt = """You are an expert code reviewer. Your job is to analyze Python code for:

1. **Code Quality**: Check for clean, readable, and maintainable code
2. **Best Practices**: Ensure adherence to Python best practices and PEP 8
3. **Security**: Identify potential security vulnerabilities
4. **Performance**: Suggest optimizations where applicable
5. **Testing**: Evaluate test coverage and quality
6. **Documentation**: Check for proper docstrings and comments

When reviewing code, provide:
- Specific line-by-line feedback
- Suggestions for improvements
- Security concerns (if any)
- Performance optimization opportunities
- Overall assessment and rating (1-10)

Be constructive and educational in your feedback. Focus on helping improve the code quality."""

code_reviewer_agent = {
    "name": "code-reviewer",
    "description": "Expert code reviewer that analyzes Python code for quality, security, performance, and best practices. Use this when you need detailed code analysis and improvement suggestions.",
    "prompt": code_reviewer_prompt,
    "tools": ["validate_python_syntax"]
}

# Sub-agent for debugging assistance
debugger_prompt = """You are an expert debugging assistant. Your job is to help identify and fix bugs in Python code.

When debugging:
1. **Analyze Error Messages**: Interpret stack traces and error messages
2. **Identify Root Causes**: Find the underlying cause of issues
3. **Suggest Fixes**: Provide specific solutions and code corrections
4. **Test Solutions**: Verify that fixes work correctly
5. **Explain Issues**: Help understand why the bug occurred

You have access to code execution tools to test fixes. Always validate your solutions by running the corrected code.

Be systematic in your approach:
- First understand the error
- Identify the problematic code section
- Propose a fix
- Test the fix
- Explain the solution"""

debugger_agent = {
    "name": "debugger",
    "description": "Expert debugging assistant that helps identify and fix bugs in Python code. Use when you encounter errors or unexpected behavior in code.",
    "prompt": debugger_prompt,
    "tools": ["execute_python_code", "validate_python_syntax"]
}

# Sub-agent for test generation
test_generator_prompt = """You are an expert test engineer specializing in Python testing. Your job is to create comprehensive unit tests for Python code.

When generating tests:
1. **Test Coverage**: Create tests that cover all functions, methods, and edge cases
2. **Test Types**: Include unit tests, integration tests, and edge case tests
3. **Frameworks**: Use appropriate testing frameworks (unittest, pytest)
4. **Assertions**: Write meaningful assertions that validate expected behavior
5. **Documentation**: Include clear test descriptions and comments

Test categories to consider:
- **Happy Path**: Normal expected inputs and outputs
- **Edge Cases**: Boundary conditions, empty inputs, large inputs
- **Error Cases**: Invalid inputs, exception handling
- **Integration**: How components work together

Always verify that your tests can run successfully and provide meaningful feedback."""

test_generator_agent = {
    "name": "test-generator",
    "description": "Expert test engineer that creates comprehensive unit tests for Python code. Use when you need to generate thorough test suites for your code.",
    "prompt": test_generator_prompt,
    "tools": ["run_unit_tests", "execute_python_code", "validate_python_syntax"]
}

# Main coding agent instructions
coding_instructions = """You are an expert Python developer and coding assistant. Your job is to help users with all aspects of Python programming including:

## Core Capabilities
- **Code Development**: Write clean, efficient, and well-documented Python code
- **Problem Solving**: Break down complex problems into manageable solutions
- **Code Review**: Analyze and improve existing code
- **Debugging**: Identify and fix bugs in Python code
- **Testing**: Create comprehensive test suites
- **Code Optimization**: Improve performance and efficiency

## Workflow
1. **Understand Requirements**: Carefully analyze what the user needs
2. **Plan Solution**: Break down the problem into steps
3. **Implement Code**: Write clean, well-documented code
4. **Test Code**: Verify functionality with comprehensive tests
5. **Review & Optimize**: Use sub-agents for code review and improvements

## Available Sub-Agents
- **code-reviewer**: For detailed code analysis and quality assessment
- **debugger**: For identifying and fixing bugs
- **test-generator**: For creating comprehensive test suites

## Best Practices
- Always write docstrings for functions and classes
- Follow PEP 8 style guidelines
- Handle errors gracefully with appropriate exception handling
- Write meaningful variable and function names
- Include type hints where appropriate
- Create comprehensive tests for your code

## File Management
- Save your main code to appropriate files (e.g., `main.py`, `solution.py`)
- Save tests to separate test files (e.g., `test_main.py`)
- Create documentation files when needed (e.g., `README.md`)

## Code Execution
You have access to tools that allow you to:
- Execute Python code safely
- Validate syntax before execution
- Run unit tests
- Install required packages

Always test your code before presenting it to the user. If there are errors, use the debugger sub-agent to help identify and fix issues.

Remember: Quality code is more important than quick code. Take time to write clean, tested, and well-documented solutions."""

# Create the coding agent
agent = create_deep_agent(
    [execute_python_code, validate_python_syntax, run_unit_tests, install_package],
    coding_instructions,
    subagents=[code_reviewer_agent, debugger_agent, test_generator_agent],
    local_filesystem=True
).with_config({"recursion_limit": 1000})