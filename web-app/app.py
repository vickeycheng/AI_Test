# -*- coding: utf-8 -*-
"""
Flask Web TODO Application
A modern web-based interface for the TODO application with Bootstrap styling
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file"""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False

@app.route('/')
def index():
    """Main page displaying all tasks"""
    tasks = load_tasks()
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.get('completed', False)])
    pending_tasks = total_tasks - completed_tasks
    
    return render_template('index.html', 
                         tasks=tasks, 
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """API endpoint to get all tasks"""
    tasks = load_tasks()
    return jsonify({
        'success': True,
        'tasks': tasks,
        'total': len(tasks)
    })

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """API endpoint to add a new task"""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        
        if not description:
            return jsonify({'success': False, 'error': 'Task description is required'}), 400
        
        tasks = load_tasks()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_task = {
            "id": len(tasks) + 1,  # Simple ID assignment
            "description": description,
            "completed": False,
            "created_at": now,
            "added_at": now
        }
        
        tasks.append(new_task)
        
        if save_tasks(tasks):
            return jsonify({
                'success': True, 
                'message': 'Task added successfully',
                'task': new_task
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to save task'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    """API endpoint to mark a task as completed"""
    try:
        tasks = load_tasks()
        
        # Find task by ID
        task_found = False
        for task in tasks:
            if task.get('id') == task_id:
                task['completed'] = not task.get('completed', False)  # Toggle completion
                task_found = True
                break
        
        if not task_found:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        if save_tasks(tasks):
            return jsonify({
                'success': True, 
                'message': 'Task updated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to save changes'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API endpoint to delete a task"""
    try:
        tasks = load_tasks()
        original_length = len(tasks)
        
        # Remove task by ID
        tasks = [task for task in tasks if task.get('id') != task_id]
        
        if len(tasks) == original_length:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        if save_tasks(tasks):
            return jsonify({
                'success': True, 
                'message': 'Task deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to save changes'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/delete-completed', methods=['DELETE'])
def delete_completed_tasks():
    """API endpoint to delete all completed tasks"""
    try:
        tasks = load_tasks()
        original_length = len(tasks)
        
        # Keep only incomplete tasks
        tasks = [task for task in tasks if not task.get('completed', False)]
        deleted_count = original_length - len(tasks)
        
        if save_tasks(tasks):
            return jsonify({
                'success': True, 
                'message': f'Deleted {deleted_count} completed tasks'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to save changes'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/delete-all', methods=['DELETE'])
def delete_all_tasks():
    """API endpoint to delete all tasks"""
    try:
        if save_tasks([]):
            return jsonify({
                'success': True, 
                'message': 'All tasks deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to delete tasks'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🚀 Starting TODO Web Application...")
    print("📱 Access your fancy UI at: http://localhost:5000")
    print("🎨 Features: Modern Bootstrap UI, Real-time updates, Mobile responsive")
    
    app.run(debug=True, host='0.0.0.0', port=5000)