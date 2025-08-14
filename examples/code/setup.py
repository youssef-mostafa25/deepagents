#!/usr/bin/env python3
"""
Setup script for the Deep Agents Coding Assistant example.

This script helps users set up the environment and dependencies
needed to run the coding agent example.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def print_step(step: str):
    """Print a step description."""
    print(f"\n🔧 {step}")


def run_command(command: list, description: str, check=True):
    """Run a shell command with error handling."""
    try:
        print(f"   Running: {' '.join(command)}")
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stderr:
            print(f"   Error details: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print(f"   ❌ Command not found: {command[0]}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print_step("Checking Python version")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"   ❌ Python {version.major}.{version.minor} detected")
        print("   ❌ Python 3.8 or higher is required")
        return False

    print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_dependencies():
    """Install required Python packages."""
    print_step("Installing dependencies")

    # Install main requirements
    success = run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Installing main requirements",
    )

    if not success:
        return False

    # Install optional development tools
    optional_packages = [
        "black",  # Code formatting
        "flake8",  # Linting
        "pylint",  # Advanced linting
        "bandit",  # Security scanning
        "pytest",  # Alternative test runner
    ]

    print("   Installing optional development tools...")
    for package in optional_packages:
        success = run_command(
            [sys.executable, "-m", "pip", "install", package],
            f"Installing {package}",
            check=False,
        )
        if success:
            print(f"   ✅ {package} installed")
        else:
            print(f"   ⚠️  {package} installation failed (optional)")

    return True


def setup_environment():
    """Set up environment configuration."""
    print_step("Setting up environment")

    env_example = Path(".env.example")
    env_file = Path(".env")

    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("   ✅ Created .env file from template")
        print("   📝 Please edit .env and add your API keys")
    elif env_file.exists():
        print("   ✅ .env file already exists")
    else:
        print("   ⚠️  No .env.example file found")

    return True


def check_api_keys():
    """Check if API keys are configured."""
    print_step("Checking API keys")

    required_keys = ["ANTHROPIC_API_KEY"]
    optional_keys = ["OPENAI_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]

    all_configured = True

    for key in required_keys:
        if os.getenv(key):
            print(f"   ✅ {key} is configured")
        else:
            print(f"   ❌ {key} is NOT configured (required)")
            all_configured = False

    for key in optional_keys:
        if os.getenv(key):
            print(f"   ✅ {key} is configured")
        else:
            print(f"   ⚠️  {key} is not configured (optional)")

    if not all_configured:
        print("\n   📝 To configure API keys:")
        print("      1. Copy .env.example to .env")
        print("      2. Edit .env and add your API keys")
        print("      3. Source the file: source .env")
        print("      4. Or export them: export ANTHROPIC_API_KEY='your-key'")

    return all_configured


def run_quick_test():
    """Run a quick test to verify the setup."""
    print_step("Running quick test")

    try:
        # Test imports
        print("   Testing imports...")
        import deepagents

        print("   ✅ deepagents imported successfully")

        # Test that we can create an agent (without invoking it)
        from coding_agent import agent

        print("   ✅ Coding agent created successfully")

        return True

    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Main setup function."""
    print_header("Deep Agents Coding Assistant Setup")

    print("This script will help you set up the coding assistant example.")
    print("It will:")
    print("• Check Python version compatibility")
    print("• Install required dependencies")
    print("• Set up environment configuration")
    print("• Verify API key configuration")
    print("• Run a quick test")

    # Get user confirmation
    response = input("\nProceed with setup? (y/N): ").strip().lower()
    if response not in ["y", "yes"]:
        print("Setup cancelled.")
        return

    success = True

    # Run setup steps
    if not check_python_version():
        success = False

    if success and not install_dependencies():
        success = False

    if success:
        setup_environment()

    # Check API keys (informational, doesn't block)
    api_keys_ok = check_api_keys()

    if success and not run_quick_test():
        success = False

    # Final summary
    print_header("Setup Summary")

    if success:
        print("✅ Setup completed successfully!")

        if api_keys_ok:
            print("\n🚀 You're ready to use the coding assistant!")
            print("\nTry these commands:")
            print("   python main.py                    # Interactive demo")
            print("   python examples/simple_demo.py    # Quick demo")
            print("   python examples/extended_agent.py # Advanced features")
        else:
            print("\n⚠️  Setup complete, but API keys need configuration.")
            print("   Please configure your API keys in .env file")
            print("   Then you'll be ready to use the assistant!")
    else:
        print("❌ Setup encountered errors.")
        print("   Please resolve the issues above and try again.")

    print(f"\n📖 See README.md for detailed usage instructions.")


if __name__ == "__main__":
    main()
