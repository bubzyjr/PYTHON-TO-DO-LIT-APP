#!/usr/bin/env python3
"""
Main Entry Point for the Python Todo List Application.

This script initializes the core components (StorageManager, TodoManager, and CLIInterface)
and starts the interactive command-line menu loop.
"""

from src.storage import StorageManager
from src.manager import TodoManager
from src.cli import CLIInterface


def main() -> None:
    """Initialize and run the Todo List application."""
    # Initialize storage layer pointing to JSON database
    storage = StorageManager(filepath="data/tasks.json")

    # Initialize business logic manager with storage
    manager = TodoManager(storage=storage)

    # Initialize interactive CLI interface
    cli = CLIInterface(manager=manager)

    # Start interactive main menu loop
    cli.run()


if __name__ == "__main__":
    main()
