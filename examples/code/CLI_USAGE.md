# Software Engineering CLI Usage Guide

## Overview
The Software Engineering CLI is an interactive command-line interface that provides AI-powered assistance for all your software development tasks. It uses the Deep Agents coding assistant to help with coding, debugging, testing, code review, and more.

## Getting Started

### Prerequisites
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables (copy from `.env.example`):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the CLI
```bash
python main.py
```

## Features

### 🎯 Smart Progress Tracking
- Real-time progress updates during task execution
- Estimated completion times
- Step-by-step progress indicators
- Session statistics (time spent, tasks completed)

### 🔧 Available Commands

#### Coding Tasks
- `code <description>` - Generate code for a specific task
- `debug <code>` - Debug problematic code and fix issues
- `review <code>` - Review code for best practices and quality
- `test <code>` - Generate comprehensive tests for code
- `optimize <code>` - Optimize code for better performance
- `explain <code>` - Explain how code works

#### Project Tasks
- `create <project_type>` - Create new project structures
- `refactor <code>` - Refactor existing code
- `api <description>` - Design and implement API endpoints
- `database <description>` - Design database schemas

#### Utility Commands
- `help` - Show available commands and usage
- `examples` - Display example tasks to try
- `clear` - Clear the screen
- `quit`, `exit`, `q` - Exit the CLI

### 💡 Usage Tips

1. **Be Specific**: The more detailed your request, the better the results
   ```
   ✅ Good: "Create a REST API for a todo list with CRUD operations, error handling, and input validation"
   ❌ Vague: "Make an API"
   ```

2. **Natural Language**: You don't need to use specific commands - just describe what you want
   ```
   "I need a function to parse CSV files and handle missing data"
   "Can you help me debug this sorting algorithm?"
   ```

3. **Sub-Agents**: The system automatically uses specialized sub-agents:
   - **Code Reviewer**: Analyzes code quality and best practices
   - **Debugger**: Identifies and fixes bugs
   - **Test Generator**: Creates comprehensive test suites

## Example Session

```
🛠️  What would you like to build or work on? Create a function to calculate fibonacci numbers

🚀 Starting task: Create a function to calculate fibonacci numbers
📋 Estimated steps: 3
────────────────────────────────────────────────────────────

⚡ Step 1/3: Analyzing requirements and planning approach
⏱️  Elapsed time: 2.1s

🤖 I'll create a fibonacci function with multiple implementation approaches...

[Agent creates optimized fibonacci function with memoization]

⚡ Step 2/3: Writing and running tests
⏱️  Elapsed time: 5.3s

[Agent generates comprehensive tests]

⚡ Step 3/3: Reviewing code quality and best practices
⏱️  Elapsed time: 8.7s

[Agent reviews the implementation]

✅ Task completed in 8.7s!
────────────────────────────────────────────────────────────
```

## Advanced Features

### Progress Tracking
The CLI automatically tracks:
- Task complexity estimation
- Real-time step updates
- Elapsed time monitoring
- Session statistics

### Smart Command Parsing
The CLI intelligently parses your input:
- Commands with arguments: `debug my_function.py`
- Natural language: `Can you help me create a web scraper?`
- Code snippets: Paste code directly for review/debugging

### File Management
- Automatically saves generated code to appropriate files
- Creates test files with proper naming conventions
- Organizes project structures logically

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**: Check your `.env` file configuration
   ```bash
   # Ensure your API keys are properly set
   cat .env
   ```

3. **Long Response Times**: Complex tasks may take longer - progress is shown in real-time

### Getting Help
- Type `help` in the CLI for command reference
- Type `examples` for sample tasks to try
- Check the main README.md for setup instructions

## Contributing

To improve the CLI:
1. Modify `main.py` for UI/UX enhancements
2. Update `coding_agent.py` for new capabilities
3. Add new sub-agents for specialized tasks

## License

Same license as the parent Deep Agents project.