#!/usr/bin/env python3
"""
Extended Coding Agent Example

This example shows how to extend the base coding agent with additional
tools and sub-agents for specialized tasks.
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, Any, List
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from deepagents import create_deep_agent
from coding_agent import (
    execute_python_code, validate_python_syntax, 
    run_unit_tests, install_package, coding_instructions
)


def lint_python_code(code: str) -> Dict[str, Any]:
    """
    Lint Python code using flake8 and pylint.
    
    Args:
        code: Python code to lint
        
    Returns:
        Dictionary with linting results
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        results = {"linting_results": []}
        
        try:
            # Try flake8 first
            flake8_result = subprocess.run(
                ['flake8', '--max-line-length=88', temp_file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            results["linting_results"].append({
                "tool": "flake8",
                "success": flake8_result.returncode == 0,
                "output": flake8_result.stdout,
                "errors": flake8_result.stderr
            })
            
        except FileNotFoundError:
            results["linting_results"].append({
                "tool": "flake8",
                "success": False,
                "output": "",
                "errors": "flake8 not installed. Install with: pip install flake8"
            })
        
        try:
            # Try pylint
            pylint_result = subprocess.run(
                ['pylint', '--disable=all', '--enable=C,W,E', temp_file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Pylint returns 0 for no issues, higher numbers for various issue levels
            results["linting_results"].append({
                "tool": "pylint",
                "success": pylint_result.returncode < 16,  # 16+ indicates fatal errors
                "output": pylint_result.stdout,
                "errors": pylint_result.stderr
            })
            
        except FileNotFoundError:
            results["linting_results"].append({
                "tool": "pylint",
                "success": False,
                "output": "",
                "errors": "pylint not installed. Install with: pip install pylint"
            })
        
        # Overall success if at least one linter ran successfully
        results["success"] = any(r["success"] for r in results["linting_results"])
        
        return results
        
    except Exception as e:
        return {
            "success": False,
            "linting_results": [],
            "error": f"Error during linting: {str(e)}"
        }
    finally:
        # Clean up
        try:
            os.unlink(temp_file_path)
        except:
            pass


def format_python_code(code: str) -> Dict[str, Any]:
    """
    Format Python code using black formatter.
    
    Args:
        code: Python code to format
        
    Returns:
        Dictionary with formatting results and formatted code
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Run black formatter
            result = subprocess.run(
                ['black', '--quiet', temp_file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Read the formatted code
                with open(temp_file_path, 'r') as f:
                    formatted_code = f.read()
                
                return {
                    "success": True,
                    "formatted_code": formatted_code,
                    "changes_made": formatted_code != code,
                    "output": result.stdout,
                    "errors": result.stderr
                }
            else:
                return {
                    "success": False,
                    "formatted_code": code,
                    "changes_made": False,
                    "output": result.stdout,
                    "errors": result.stderr
                }
                
        except FileNotFoundError:
            return {
                "success": False,
                "formatted_code": code,
                "changes_made": False,
                "output": "",
                "errors": "black formatter not installed. Install with: pip install black"
            }
            
    except Exception as e:
        return {
            "success": False,
            "formatted_code": code,
            "changes_made": False,
            "output": "",
            "errors": f"Error during formatting: {str(e)}"
        }
    finally:
        # Clean up
        try:
            os.unlink(temp_file_path)
        except:
            pass


def check_security_issues(code: str) -> Dict[str, Any]:
    """
    Check Python code for security issues using bandit.
    
    Args:
        code: Python code to check
        
    Returns:
        Dictionary with security analysis results
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Run bandit security checker
            result = subprocess.run(
                ['bandit', '-f', 'json', temp_file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": True,
                "security_report": result.stdout,
                "errors": result.stderr,
                "return_code": result.returncode
            }
            
        except FileNotFoundError:
            return {
                "success": False,
                "security_report": "",
                "errors": "bandit not installed. Install with: pip install bandit",
                "return_code": -1
            }
            
    except Exception as e:
        return {
            "success": False,
            "security_report": "",
            "errors": f"Error during security check: {str(e)}",
            "return_code": -1
        }
    finally:
        # Clean up
        try:
            os.unlink(temp_file_path)
        except:
            pass


# Enhanced sub-agents with additional capabilities

performance_optimizer_prompt = """You are an expert Python performance optimizer. Your job is to analyze code and suggest optimizations for:

1. **Algorithm Efficiency**: Identify opportunities to improve time complexity
2. **Memory Usage**: Reduce memory consumption and prevent memory leaks
3. **Python-Specific Optimizations**: Use of built-in functions, list comprehensions, generators
4. **Caching and Memoization**: Where appropriate, add caching to improve performance
5. **Profiling**: Suggest profiling approaches to identify bottlenecks

When optimizing:
- Measure performance before and after changes
- Consider readability vs performance trade-offs
- Suggest appropriate data structures for the use case
- Identify unnecessary computations or repeated work
- Recommend vectorization where applicable (NumPy, Pandas)

Always validate that optimizations maintain correctness by running tests."""

performance_optimizer_agent = {
    "name": "performance-optimizer",
    "description": "Expert performance optimizer that analyzes and improves Python code efficiency, memory usage, and execution speed.",
    "prompt": performance_optimizer_prompt,
    "tools": ["execute_python_code", "validate_python_syntax"]
}

code_formatter_prompt = """You are an expert code formatter and style guide enforcer. Your job is to ensure code follows best practices for:

1. **Code Style**: PEP 8 compliance, consistent formatting
2. **Code Organization**: Proper imports, function ordering, class structure
3. **Documentation**: Comprehensive docstrings, inline comments
4. **Type Hints**: Complete and accurate type annotations
5. **Error Messages**: Clear, helpful error messages and logging

When formatting code:
- Use tools like black, flake8, and pylint for automated checks
- Ensure consistent naming conventions
- Organize imports properly (stdlib, third-party, local)
- Add missing docstrings and type hints
- Improve variable and function names for clarity
- Remove dead code and unused imports

Always test that formatted code still works correctly."""

code_formatter_agent = {
    "name": "code-formatter",
    "description": "Expert code formatter that ensures Python code follows PEP 8 and best practices for style, documentation, and organization.",
    "prompt": code_formatter_prompt,
    "tools": ["format_python_code", "lint_python_code", "validate_python_syntax"]
}

security_auditor_prompt = """You are an expert security auditor specializing in Python code security. Your job is to identify and fix:

1. **Input Validation**: Ensure all user inputs are properly validated
2. **SQL Injection**: Check for vulnerable database queries
3. **Code Injection**: Identify eval(), exec(), and similar dangerous functions
4. **File System Security**: Validate file operations and path traversal
5. **Cryptography**: Ensure proper use of encryption and hashing
6. **Dependencies**: Check for known vulnerabilities in dependencies

When auditing code:
- Use tools like bandit for automated security scanning
- Check for hardcoded secrets and credentials
- Validate all external inputs and API calls
- Ensure proper error handling that doesn't leak information
- Review authentication and authorization logic
- Check for race conditions and concurrency issues

Provide specific recommendations for fixing security issues."""

security_auditor_agent = {
    "name": "security-auditor", 
    "description": "Expert security auditor that identifies and fixes security vulnerabilities in Python code.",
    "prompt": security_auditor_prompt,
    "tools": ["check_security_issues", "validate_python_syntax"]
}

# Enhanced coding instructions
enhanced_instructions = """You are an advanced Python developer and coding assistant with access to enhanced tools and specialized sub-agents.

## Enhanced Capabilities
- **Code Formatting**: Automatic code formatting with black, flake8, pylint
- **Security Auditing**: Security vulnerability detection with bandit
- **Performance Optimization**: Algorithm and performance analysis
- **Comprehensive Testing**: Advanced test generation and coverage analysis

## Enhanced Sub-Agents
- **performance-optimizer**: Analyzes and improves code efficiency and speed
- **code-formatter**: Ensures code follows PEP 8 and formatting best practices  
- **security-auditor**: Identifies and fixes security vulnerabilities
- **code-reviewer**: General code quality and best practices review
- **debugger**: Bug identification and fixing assistance
- **test-generator**: Comprehensive test suite creation

## Enhanced Workflow
1. **Analysis**: Understand requirements and constraints
2. **Implementation**: Write clean, efficient code
3. **Formatting**: Use code-formatter for style compliance
4. **Security**: Use security-auditor for vulnerability assessment
5. **Performance**: Use performance-optimizer for efficiency improvements
6. **Testing**: Generate comprehensive tests
7. **Review**: Final quality assurance with code-reviewer

Always use the most appropriate sub-agent for each task and leverage the enhanced tools for better code quality."""

# Create the enhanced agent
enhanced_agent = create_deep_agent(
    [execute_python_code, validate_python_syntax, run_unit_tests, install_package,
     lint_python_code, format_python_code, check_security_issues],
    enhanced_instructions,
    subagents=[
        performance_optimizer_agent,
        code_formatter_agent, 
        security_auditor_agent,
        # Include original sub-agents
        {
            "name": "code-reviewer",
            "description": "Expert code reviewer that analyzes Python code for quality, security, performance, and best practices.",
            "prompt": "You are an expert code reviewer...",  # Would use full prompt from original
            "tools": ["validate_python_syntax", "lint_python_code"]
        },
        # ... other original subagents
    ]
)


async def demo_enhanced_agent():
    """Demonstrate the enhanced agent capabilities."""
    
    print("🚀 Enhanced Coding Agent Demo")
    print("=" * 50)
    
    task = """
    Create a web API endpoint that accepts user data and stores it in a database.
    Requirements:
    1. Input validation and sanitization
    2. SQL injection prevention
    3. Error handling and logging
    4. Performance optimization for high traffic
    5. Comprehensive security review
    6. Professional code formatting
    7. Complete test suite
    
    Use all enhanced capabilities including security auditing, performance optimization, 
    and code formatting. Make it production-ready.
    """
    
    print("🧠 Enhanced agent working...")
    print("This will demonstrate security auditing, performance optimization, and code formatting.")
    
    # In a real implementation, you would call the enhanced agent here
    print("\n✅ Enhanced agent would create a secure, optimized, well-formatted API endpoint!")
    print("Features demonstrated:")
    print("  • Security vulnerability scanning")
    print("  • Code formatting with black/flake8")
    print("  • Performance optimization suggestions")
    print("  • Comprehensive test generation")
    print("  • Professional documentation")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_enhanced_agent())