# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python TODO application that demonstrates basic CRUD operations for task management. The application is a command-line interface written in Chinese that allows users to manage their tasks with persistence using JSON file storage.

## Commands

### Running the Application
```bash
python3 test_todo_app.py
```

The application runs interactively and presents a menu-driven interface. No additional setup or dependencies are required beyond Python 3.

### Testing
There are no automated tests in this repository. Testing should be done manually by running the application and verifying the following functionality:
- Adding new tasks
- Viewing all tasks
- Marking tasks as complete
- Deleting individual, multiple, or all tasks

## Architecture

### Core Components

- **test_todo_app.py**: Single-file application containing all functionality
- **tasks.json**: Auto-generated data file for task persistence (created when first task is added)

### Key Functions

- `load_tasks()` / `save_tasks()`: Handle JSON file I/O for task persistence
- `add_task()`: Creates new tasks with timestamps
- `view_tasks()`: Displays all tasks with completion status and creation time
- `complete_task()`: Marks tasks as completed
- `delete_task()`: Supports deletion of single, multiple, or all tasks
- `main()`: Interactive menu loop with Chinese interface

### Data Structure

Tasks are stored as JSON objects with the following schema:
```json
{
  "description": "Task description",
  "completed": false,
  "created_at": "YYYY-MM-DD HH:MM:SS",
  "added_at": "YYYY-MM-DD HH:MM:SS"
}
```

## Development Notes

- The interface is entirely in Chinese (Traditional/Simplified)
- No external dependencies required
- File encoding is UTF-8 to support Chinese characters
- Application uses 1-based indexing for user interaction but 0-based internally
- The `tasks.json` file is created automatically in the same directory as the script