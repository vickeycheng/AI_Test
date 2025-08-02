# -*- coding: utf-8 -*-
import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from datetime import datetime
import sys

# Import the module to test
sys.path.append('.')
import test_todo_app

class TestTodoApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_tasks_file = test_todo_app.TASKS_FILE
        test_todo_app.TASKS_FILE = os.path.join(self.test_dir, "test_tasks.json")
        self.sample_tasks = [
            {
                "description": "測試任務1",
                "completed": False,
                "created_at": "2024-01-01 10:00:00",
                "added_at": "2024-01-01 10:00:00"
            },
            {
                "description": "測試任務2",
                "completed": True,
                "created_at": "2024-01-01 11:00:00",
                "added_at": "2024-01-01 11:00:00"
            }
        ]
    
    def tearDown(self):
        """Clean up after each test"""
        test_todo_app.TASKS_FILE = self.original_tasks_file
        shutil.rmtree(self.test_dir)
    
    def test_load_tasks_no_file(self):
        """Test loading tasks when file doesn't exist"""
        tasks = test_todo_app.load_tasks()
        self.assertEqual(tasks, [])
    
    def test_load_tasks_with_file(self):
        """Test loading tasks from existing file"""
        with open(test_todo_app.TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.sample_tasks, f, ensure_ascii=False)
        
        tasks = test_todo_app.load_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["description"], "測試任務1")
        self.assertEqual(tasks[1]["completed"], True)
    
    def test_save_tasks(self):
        """Test saving tasks to file"""
        test_todo_app.save_tasks(self.sample_tasks)
        
        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists(test_todo_app.TASKS_FILE))
        
        with open(test_todo_app.TASKS_FILE, 'r', encoding='utf-8') as f:
            saved_tasks = json.load(f)
        
        self.assertEqual(len(saved_tasks), 2)
        self.assertEqual(saved_tasks, self.sample_tasks)
    
    @patch('test_todo_app.datetime')
    @patch('builtins.print')
    def test_add_task(self, mock_print, mock_datetime):
        """Test adding a new task"""
        mock_datetime.now.return_value.strftime.return_value = "2024-01-01 12:00:00"
        
        test_todo_app.add_task("新測試任務")
        
        tasks = test_todo_app.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "新測試任務")
        self.assertEqual(tasks[0]["completed"], False)
        self.assertEqual(tasks[0]["created_at"], "2024-01-01 12:00:00")
        mock_print.assert_called_once()
    
    @patch('builtins.print')
    def test_view_tasks_empty(self, mock_print):
        """Test viewing tasks when no tasks exist"""
        test_todo_app.view_tasks()
        mock_print.assert_called_with("目前沒有任務。")
    
    @patch('builtins.print')
    def test_view_tasks_with_data(self, mock_print):
        """Test viewing tasks with existing data"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.view_tasks()
        
        # Check that print was called for each task
        self.assertEqual(mock_print.call_count, 2)
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("測試任務1" in call for call in calls))
        self.assertTrue(any("測試任務2" in call for call in calls))
    
    @patch('builtins.print')
    def test_complete_task_valid_index(self, mock_print):
        """Test completing a task with valid index"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.complete_task(0)
        
        tasks = test_todo_app.load_tasks()
        self.assertTrue(tasks[0]["completed"])
        mock_print.assert_called_with("任務已標記為完成。")
    
    @patch('builtins.print')
    def test_complete_task_invalid_index(self, mock_print):
        """Test completing a task with invalid index"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.complete_task(10)
        
        mock_print.assert_called_with("無效的任務編號。")
    
    @patch('builtins.print')
    def test_delete_task_empty_list(self, mock_print):
        """Test deleting task when no tasks exist"""
        test_todo_app.delete_task(0)
        mock_print.assert_called_with("目前沒有任務。")
    
    @patch('builtins.print')
    def test_delete_task_all(self, mock_print):
        """Test deleting all tasks"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.delete_task('all')
        
        tasks = test_todo_app.load_tasks()
        self.assertEqual(len(tasks), 0)
        mock_print.assert_called_with("已刪除所有任務。")
    
    @patch('builtins.print')
    def test_delete_task_single_valid(self, mock_print):
        """Test deleting a single task with valid index"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.delete_task(0)
        
        tasks = test_todo_app.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "測試任務2")
        mock_print.assert_called_with("已刪除 1 個任務。")
    
    @patch('builtins.print')
    def test_delete_task_multiple_valid(self, mock_print):
        """Test deleting multiple tasks with valid indices"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.delete_task("1,2")
        
        tasks = test_todo_app.load_tasks()
        self.assertEqual(len(tasks), 0)
        mock_print.assert_called_with("已刪除 2 個任務。")
    
    @patch('builtins.print')
    def test_delete_task_invalid_format(self, mock_print):
        """Test deleting tasks with invalid format"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.delete_task("abc,def")
        
        mock_print.assert_called_with("無效的任務編號格式。請使用逗號分隔的數字，例如：1,2,3")
    
    @patch('builtins.print')
    def test_delete_task_invalid_index(self, mock_print):
        """Test deleting task with invalid index"""
        test_todo_app.save_tasks(self.sample_tasks)
        test_todo_app.delete_task(10)
        
        mock_print.assert_called_with("無效的任務編號。")
    
    def test_json_encoding_utf8(self):
        """Test that Chinese characters are properly handled in JSON"""
        chinese_tasks = [
            {
                "description": "中文測試任務",
                "completed": False,
                "created_at": "2024-01-01 10:00:00",
                "added_at": "2024-01-01 10:00:00"
            }
        ]
        
        test_todo_app.save_tasks(chinese_tasks)
        loaded_tasks = test_todo_app.load_tasks()
        
        self.assertEqual(loaded_tasks[0]["description"], "中文測試任務")
    
    def test_file_persistence(self):
        """Test that tasks persist across save/load cycles"""
        test_todo_app.save_tasks(self.sample_tasks)
        
        # Load tasks multiple times to ensure persistence
        for _ in range(3):
            tasks = test_todo_app.load_tasks()
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[0]["description"], "測試任務1")
    
    def test_edge_case_empty_description(self):
        """Test adding task with empty description"""
        test_todo_app.add_task("")
        tasks = test_todo_app.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "")
    
    def test_edge_case_long_description(self):
        """Test adding task with very long description"""
        long_desc = "很長的任務描述" * 100
        test_todo_app.add_task(long_desc)
        tasks = test_todo_app.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], long_desc)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)