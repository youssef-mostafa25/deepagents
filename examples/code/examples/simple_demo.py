#!/usr/bin/env python3
"""
Simple Demo: Basic Coding Agent Usage

This is a minimal example showing how to use the coding agent
for simple tasks without the full interactive interface.
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to path to import the agent
sys.path.append(str(Path(__file__).parent.parent))
from coding_agent import agent


async def simple_fibonacci_demo():
    """Demo: Ask the agent to create a fibonacci function."""
    
    print("🤖 Simple Coding Agent Demo")
    print("=" * 40)
    print("\nTask: Create a fibonacci function with tests")
    print("-" * 40)
    
    task = """
    Create a Python function to calculate fibonacci numbers.
    Include:
    1. Proper error handling for invalid inputs
    2. Type hints and docstring
    3. At least 3 test cases
    4. Save the code to 'fibonacci.py'
    
    Make it clean and well-documented.
    """
    
    print("🧠 Agent is thinking and coding...")
    
    # Get the response from the agent
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    print("\n✅ Agent completed the task!")
    
    # Show the final response
    if result["messages"]:
        print("\n💬 Agent's response:")
        print("-" * 40)
        print(result["messages"][-1].content)
    
    # Show created files
    if "files" in result and result["files"]:
        print(f"\n📁 Files created ({len(result['files'])} total):")
        for filename, content in result["files"].items():
            print(f"\n📄 {filename} ({len(content)} characters)")
            print("─" * 30)
            # Show first few lines of each file
            lines = content.split('\n')
            preview_lines = min(10, len(lines))
            for i, line in enumerate(lines[:preview_lines]):
                print(f"{i+1:2d}: {line}")
            if len(lines) > preview_lines:
                print(f"... ({len(lines) - preview_lines} more lines)")
    
    return result


async def simple_debug_demo():
    """Demo: Ask the agent to debug some code."""
    
    print("\n" + "=" * 50)
    print("🐛 Debugging Demo")
    print("=" * 50)
    
    buggy_code = '''
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

# Test it
test_data = []
print("Average:", calculate_average(test_data))
'''
    
    task = f"""
    This code has a bug. Please identify and fix it:
    
    ```python
{buggy_code}
    ```
    
    Explain what's wrong and provide a corrected version with proper error handling.
    """
    
    print("🧠 Agent is debugging...")
    
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    print("\n✅ Debugging completed!")
    
    if result["messages"]:
        print("\n💬 Agent's debugging analysis:")
        print("-" * 40)
        print(result["messages"][-1].content)
    
    return result


async def main():
    """Run the simple demos."""
    try:
        # Demo 1: Basic function creation
        await simple_fibonacci_demo()
        
        # Demo 2: Debug existing code
        await simple_debug_demo()
        
        print("\n🎉 All demos completed successfully!")
        print("\nTo try more advanced features, run: python main.py")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Make sure you have set up your API keys correctly.")
        print("Example: export ANTHROPIC_API_KEY='your-key-here'")


if __name__ == "__main__":
    asyncio.run(main())