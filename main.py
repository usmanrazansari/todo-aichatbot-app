#!/usr/bin/env python3
"""
Todo Application - In-Memory Console App

A basic command-line Todo application that stores all tasks in memory.
"""
import sys
from todo_app.cli import TodoAppCLI


def main():
    """Main entry point for the application."""
    print("Welcome to the Todo Application!")
    print("Loading application...")

    # Initialize and run the CLI application
    app = TodoAppCLI()
    app.run()


if __name__ == "__main__":
    main()