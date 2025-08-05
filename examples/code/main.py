#!/usr/bin/env python3
"""
Deep Agents Software Engineering CLI

This script provides an interactive CLI experience for software engineering tasks
using the Deep Agents coding assistant. It helps with code development, debugging,
testing, code review, and more.
"""

import asyncio
import sys
import time
from typing import Optional, Dict, Any
from datetime import datetime
from coding_agent import agent


class ProgressTracker:
    """Tracks and displays progress of software engineering tasks."""
    
    def __init__(self):
        self.start_time = None
        self.current_step = ""
        self.steps_completed = 0
        self.total_steps = 0
    
    def start_task(self, description: str, estimated_steps: int = 1):
        """Start tracking a new task."""
        self.start_time = time.time()
        self.current_step = description
        self.steps_completed = 0
        self.total_steps = estimated_steps
        print(f"\n🚀 Starting task: {description}")
        print(f"📋 Estimated steps: {estimated_steps}")
        print("─" * 60)
    
    def update_step(self, step_description: str):
        """Update the current step being worked on."""
        self.current_step = step_description
        self.steps_completed += 1
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        print(f"\n⚡ Step {self.steps_completed}/{self.total_steps}: {step_description}")
        print(f"⏱️  Elapsed time: {elapsed:.1f}s")
        
    def complete_task(self):
        """Mark the task as completed."""
        if self.start_time:
            total_time = time.time() - self.start_time
            print(f"\n✅ Task completed in {total_time:.1f}s!")
            print("─" * 60)


def print_banner():
    """Print a nice banner for the CLI."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                   🤖 SOFTWARE ENGINEERING CLI                ║
║                    Powered by Deep Agents                    ║
║                                                              ║
║  Your AI-powered assistant for all software development     ║
║  tasks including coding, debugging, testing, and review.    ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_separator(title: str = "", char: str = "=", width: int = 60):
    """Print a visual separator with optional title."""
    if title:
        print(f"\n{char * width}")
        print(f" {title}")
        print(f"{char * width}")
    else:
        print(char * width)


def print_help():
    """Print help information about available commands and features."""
    help_text = """
🔧 AVAILABLE COMMANDS:
┌─────────────────────────────────────────────────────────────┐
│ CODING TASKS:                                               │
│  • code <description>     - Generate code for a task       │
│  • debug <code>          - Debug problematic code          │
│  • review <code>         - Review code for best practices  │
│  • test <code>           - Generate tests for code         │
│  • optimize <code>       - Optimize code performance       │
│  • explain <code>        - Explain how code works          │
│                                                             │
│ PROJECT TASKS:                                              │
│  • create <project_type> - Create a new project structure  │
│  • refactor <code>       - Refactor existing code          │
│  • api <description>     - Design API endpoints            │
│  • database <description>- Design database schema          │
│                                                             │
│ UTILITY COMMANDS:                                           │
│  • help                  - Show this help message          │
│  • examples              - Show example tasks              │
│  • quit, exit, q         - Exit the CLI                    │
│  • clear                 - Clear the screen                │
└─────────────────────────────────────────────────────────────┘

💡 TIPS:
  • Be specific in your requests for better results
  • The agent will use sub-agents for specialized tasks
  • All code is tested and validated automatically
  • Files are saved to the current directory when created
"""
    print(help_text)


def print_examples():
    """Print example tasks that users can try."""
    examples = """
📝 EXAMPLE TASKS TO TRY:

🔹 BEGINNER TASKS:
   • "Create a function to calculate fibonacci numbers"
   • "Debug this sorting algorithm: [paste your code]"
   • "Generate tests for a basic calculator class"

🔹 INTERMEDIATE TASKS:
   • "Create a REST API for a todo list application"
   • "Implement a caching system with TTL support"
   • "Build a log parser that extracts error patterns"

🔹 ADVANCED TASKS:
   • "Design a distributed task queue system"
   • "Create a web scraper with rate limiting and retry logic"
   • "Implement a basic blockchain with proof of work"

🔹 PROJECT TASKS:
   • "Create a complete Flask web application structure"
   • "Design a microservices architecture for an e-commerce app"
   • "Build a data pipeline for processing CSV files"

Just type any of these or describe your own software engineering task!
"""
    print(examples)


async def execute_coding_task(task_description: str, progress: ProgressTracker):
    """
    Execute a coding task with progress tracking and nice output formatting.
    
    Args:
        task_description: Description of the coding task
        progress: Progress tracker instance
    """
    try:
        # Estimate steps based on task complexity
        estimated_steps = estimate_task_complexity(task_description)
        progress.start_task(task_description, estimated_steps)
        
        print(f"\n🤖 Coding Agent is working on your task...")
        print(f"📝 Task: {task_description[:80]}{'...' if len(task_description) > 80 else ''}")
        
        step_count = 0
        message_buffer = []
        
        # Stream the agent's response with progress updates
        # Include subgraphs=True to show outputs from sub agents
        async for _, chunk in agent.astream(
            {"messages": [{"role": "user", "content": task_description}]},
            stream_mode="updates",
            subgraphs=True
        ):
            chunk = list(chunk.values())[0]
            if "messages" in chunk and chunk["messages"]:
                last_message = chunk["messages"][-1]
                
                # Extract clean text content from the message
                # Handle both direct content access and attribute access
                message_content = None
                if hasattr(last_message, 'content'):
                    message_content = last_message.content
                elif isinstance(last_message, dict) and 'content' in last_message:
                    message_content = last_message['content']
                
                if message_content:
                    text_content = extract_text_content(message_content)
                    
                    if text_content.strip():  # Only print if there's actual text content
                        # Look for progress indicators in the message
                        if any(keyword in text_content.lower() for keyword in ['analyzing', 'planning', 'implementing', 'testing', 'reviewing']):
                            step_count += 1
                            if step_count <= estimated_steps:
                                step_desc = extract_step_description(text_content)
                                progress.update_step(step_desc)
                        
                        # Print the clean text content
                        print(f"\n🤖 {text_content}")
                        print("─" * 40)
                
        progress.complete_task()
        
    except Exception as e:
        print(f"\n❌ Error executing task: {e}")
        print("💡 Try rephrasing your request or check your input.")


def estimate_task_complexity(task_description: str) -> int:
    """
    Estimate the number of steps for a task based on its description.
    
    Args:
        task_description: The task description
        
    Returns:
        Estimated number of steps
    """
    # Simple heuristic based on keywords and length
    complexity_keywords = {
        'create': 3, 'implement': 4, 'build': 5, 'design': 4,
        'debug': 2, 'fix': 2, 'review': 2, 'test': 2,
        'optimize': 3, 'refactor': 3, 'api': 4, 'database': 4,
        'web': 5, 'microservice': 6, 'distributed': 7, 'system': 5
    }
    
    task_lower = task_description.lower()
    base_complexity = 1
    
    for keyword, complexity in complexity_keywords.items():
        if keyword in task_lower:
            base_complexity = max(base_complexity, complexity)
    
    # Adjust based on length (longer descriptions usually mean more complex tasks)
    if len(task_description) > 200:
        base_complexity += 2
    elif len(task_description) > 100:
        base_complexity += 1
        
    return min(base_complexity, 10)  # Cap at 10 steps


def extract_text_content(message_content) -> str:
    """
    Extract text content from message content blocks, filtering out tool calls and other non-text content.
    
    Args:
        message_content: The message content (could be string, list of content blocks, etc.)
        
    Returns:
        Clean text content for display
    """
    if isinstance(message_content, str):
        return message_content
    
    if isinstance(message_content, list):
        text_parts = []
        for block in message_content:
            if isinstance(block, dict):
                # Handle text blocks
                if block.get('type') == 'text' and 'text' in block:
                    text_parts.append(block['text'])
                # Skip tool_use blocks (these are the ones we want to filter out)
                elif block.get('type') == 'tool_use':
                    continue
        return '\n'.join(text_parts).strip() if text_parts else ''
    
    # Fallback for other types - but avoid printing raw objects
    if hasattr(message_content, '__dict__'):
        return ""  # Don't print complex objects
    return str(message_content)


def extract_step_description(content: str) -> str:
    """
    Extract a meaningful step description from agent message content.
    
    Args:
        content: The message content
        
    Returns:
        A brief step description
    """
    # Look for common patterns that indicate what the agent is doing
    content_lower = content.lower()
    
    if 'analyzing' in content_lower:
        return "Analyzing requirements and planning approach"
    elif 'implementing' in content_lower or 'creating' in content_lower:
        return "Implementing the solution"
    elif 'testing' in content_lower:
        return "Writing and running tests"
    elif 'reviewing' in content_lower:
        return "Reviewing code quality and best practices"
    elif 'debugging' in content_lower:
        return "Debugging and fixing issues"
    elif 'optimizing' in content_lower:
        return "Optimizing performance and efficiency"
    else:
        # Fallback: use first few words of the content
        words = content.split()[:6]
        return " ".join(words) + ("..." if len(words) == 6 else "")


def parse_command(user_input: str) -> tuple[str, str]:
    """
    Parse user input into command and arguments.
    
    Args:
        user_input: Raw user input
        
    Returns:
        Tuple of (command, arguments)
    """
    parts = user_input.strip().split(' ', 1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    return command, args


async def software_engineering_cli():
    """Main CLI loop for software engineering tasks."""
    
    print_banner()
    
    print("\n🎯 Welcome to your AI Software Engineering Assistant!")
    print("Type 'help' for available commands or just describe what you want to build.")
    print("Type 'examples' to see sample tasks you can try.")
    print("Type 'quit' to exit.\n")
    
    progress = ProgressTracker()
    session_start = datetime.now()
    tasks_completed = 0
    
    while True:
        try:
            # Show session info
            session_time = datetime.now() - session_start
            print(f"\n┌─ Session: {session_time.seconds // 60}m {session_time.seconds % 60}s | Tasks completed: {tasks_completed} ─┐")
            
            user_input = input("🛠️  What would you like to build or work on? ").strip()
            
            if not user_input:
                continue
                
            command, args = parse_command(user_input)
            
            # Handle utility commands
            if command in ['quit', 'exit', 'q']:
                print(f"\n👋 Thanks for using the Software Engineering CLI!")
                print(f"📊 Session summary: {tasks_completed} tasks completed in {session_time}")
                break
                
            elif command == 'help':
                print_help()
                continue
                
            elif command == 'examples':
                print_examples()
                continue
                
            elif command == 'clear':
                print("\033[2J\033[H", end="")  # Clear screen
                print_banner()
                continue
            
            # Handle coding commands
            elif command in ['code', 'create', 'implement', 'build']:
                task = f"Create/implement: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'debug':
                task = f"Debug this code and fix any issues: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'review':
                task = f"Review this code for quality, best practices, and improvements: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'test':
                task = f"Generate comprehensive tests for this code: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'optimize':
                task = f"Optimize this code for better performance: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'explain':
                task = f"Explain how this code works and what it does: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'refactor':
                task = f"Refactor this code to improve its structure and maintainability: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'api':
                task = f"Design and implement an API: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            elif command == 'database':
                task = f"Design database schema and implementation: {args}" if args else user_input
                await execute_coding_task(task, progress)
                tasks_completed += 1
                
            else:
                # Treat as a general coding task
                await execute_coding_task(user_input, progress)
                tasks_completed += 1
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Thanks for using the Software Engineering CLI!")
            print(f"📊 Session summary: {tasks_completed} tasks completed")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("💡 Please try again or type 'help' for assistance.")


async def main():
    """Main entry point."""
    try:
        await software_engineering_cli()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())