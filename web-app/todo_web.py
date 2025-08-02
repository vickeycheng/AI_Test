# -*- coding: utf-8 -*-
"""
Web TODO Application
Flask web interface for task management using shared core functionality
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add shared folder to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shared'))

from todo_core import (
    load_tasks, add_task_data, complete_task_data, 
    delete_task_data, delete_completed_tasks_data, delete_all_tasks_data,
    get_task_stats
)

app = Flask(__name__)
app.secret_key = 'vickey-todo-secret-key'

@app.route('/')
def index():
    """Main page displaying all tasks"""
    stats = get_task_stats()
    
    return render_template('index.html', 
                         tasks=stats['tasks'], 
                         total_tasks=stats['total'],
                         completed_tasks=stats['completed'],
                         pending_tasks=stats['pending'])

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """API endpoint to get all tasks"""
    stats = get_task_stats()
    return jsonify({
        'success': True,
        'tasks': stats['tasks'],
        'total': stats['total'],
        'completed': stats['completed'],
        'pending': stats['pending']
    })

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """API endpoint to add a new task"""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        
        if not description:
            return jsonify({'success': False, 'error': 'Task description is required'}), 400
        
        new_task = add_task_data(description)
        
        if new_task:
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
        if complete_task_data(task_id):
            return jsonify({
                'success': True, 
                'message': 'Task updated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Task not found or update failed'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API endpoint to delete a task"""
    try:
        if delete_task_data(task_id):
            return jsonify({
                'success': True, 
                'message': 'Task deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/delete-completed', methods=['DELETE'])
def delete_completed_tasks():
    """API endpoint to delete all completed tasks"""
    try:
        deleted_count = delete_completed_tasks_data()
        return jsonify({
            'success': True, 
            'message': f'Deleted {deleted_count} completed tasks'
        })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/delete-all', methods=['DELETE'])
def delete_all_tasks():
    """API endpoint to delete all tasks"""
    try:
        if delete_all_tasks_data():
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
    print("🚀 Starting TODO Web Application...")
    print("📱 Access your fancy UI at: http://localhost:5000")
    print("🎨 Features: Light gray theme, Modern UI, Mobile responsive")
    
    app.run(debug=True, host='0.0.0.0', port=5000)