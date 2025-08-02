# -*- coding: utf-8 -*-
"""
Shared TODO Core Functionality
Common functions used by both CLI and Web applications
"""

import json
import os
from datetime import datetime

# Default tasks file path (relative to shared folder)
DEFAULT_TASKS_FILE = "tasks.json"

def get_tasks_file_path():
    """Get the full path to tasks.json in the shared folder"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, DEFAULT_TASKS_FILE)

def load_tasks(tasks_file=None):
    """Load tasks from JSON file"""
    if tasks_file is None:
        tasks_file = get_tasks_file_path()
    
    if not os.path.exists(tasks_file):
        return []
    
    try:
        with open(tasks_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks, tasks_file=None):
    """Save tasks to JSON file"""
    if tasks_file is None:
        tasks_file = get_tasks_file_path()
    
    try:
        with open(tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False

def add_task_data(description, tasks_file=None):
    """Add a new task to the data structure"""
    tasks = load_tasks(tasks_file)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate new ID
    max_id = max([task.get('id', 0) for task in tasks], default=0)
    new_id = max_id + 1
    
    new_task = {
        "id": new_id,
        "description": description,
        "completed": False,
        "created_at": now,
        "added_at": now
    }
    
    tasks.append(new_task)
    
    if save_tasks(tasks, tasks_file):
        return new_task
    else:
        return None

def complete_task_data(task_id, tasks_file=None):
    """Mark a task as completed by ID"""
    tasks = load_tasks(tasks_file)
    
    for task in tasks:
        if task.get('id') == task_id:
            task['completed'] = not task.get('completed', False)  # Toggle completion
            if save_tasks(tasks, tasks_file):
                return True
            break
    
    return False

def delete_task_data(task_id, tasks_file=None):
    """Delete a task by ID"""
    tasks = load_tasks(tasks_file)
    original_length = len(tasks)
    
    tasks = [task for task in tasks if task.get('id') != task_id]
    
    if len(tasks) < original_length:
        return save_tasks(tasks, tasks_file)
    
    return False

def delete_completed_tasks_data(tasks_file=None):
    """Delete all completed tasks"""
    tasks = load_tasks(tasks_file)
    original_length = len(tasks)
    
    tasks = [task for task in tasks if not task.get('completed', False)]
    deleted_count = original_length - len(tasks)
    
    if save_tasks(tasks, tasks_file):
        return deleted_count
    
    return 0

def delete_all_tasks_data(tasks_file=None):
    """Delete all tasks"""
    return save_tasks([], tasks_file)

def get_task_stats(tasks_file=None):
    """Get task statistics"""
    tasks = load_tasks(tasks_file)
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.get('completed', False)])
    pending_tasks = total_tasks - completed_tasks
    
    return {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'tasks': tasks
    }