# -*- coding: utf-8 -*-
"""
End-to-End Test Case: Vickey's Task Management Scenario

Test Scenario:
Vickey wants to create 3 tasks:
1. Morning call at tomorrow 8:00AM
2. Date with Jimmy  
3. Make a reservation for the restaurant
Then view all tasks to verify they are listed correctly.
"""

import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import patch
from datetime import datetime
import sys

# Import the module to test
sys.path.append('.')
import test_todo_app

class TestVickeyE2EScenario(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_tasks_file = test_todo_app.TASKS_FILE
        test_todo_app.TASKS_FILE = os.path.join(self.test_dir, "vickey_tasks.json")
        
        # Mock timestamp for consistent testing
        self.mock_timestamp = "2025-08-02 14:00:00"
    
    def tearDown(self):
        """Clean up after test"""
        test_todo_app.TASKS_FILE = self.original_tasks_file
        shutil.rmtree(self.test_dir)
    
    @patch('test_todo_app.datetime')
    @patch('builtins.print')
    def test_vickey_complete_workflow(self, mock_print, mock_datetime):
        """
        Complete E2E test simulating Vickey's workflow:
        1. Add 3 tasks
        2. View all tasks
        3. Verify correct display
        """
        
        # Mock the datetime for consistent timestamps
        mock_datetime.now.return_value.strftime.return_value = self.mock_timestamp
        
        print("\n=== VICKEY'S TODO MANAGEMENT SCENARIO ===")
        print("Simulating Vickey creating 3 tasks and viewing them...")
        
        # Step 1: Vickey adds first task - Morning call
        print("\n📞 Adding Task 1: Morning call at tomorrow 8:00AM")
        test_todo_app.add_task("Morning call at tomorrow 8:00AM")
        
        # Step 2: Vickey adds second task - Date with Jimmy
        print("💝 Adding Task 2: Date with Jimmy")
        test_todo_app.add_task("Date with Jimmy")
        
        # Step 3: Vickey adds third task - Restaurant reservation
        print("🍽️ Adding Task 3: Make a reservation for the restaurant")
        test_todo_app.add_task("Make a reservation for the restaurant")
        
        # Step 4: Vickey views all tasks to check they're listed
        print("\n👀 Viewing all tasks...")
        test_todo_app.view_tasks()
        
        # Verification: Load tasks directly to verify data integrity
        tasks = test_todo_app.load_tasks()
        
        # Assert that 3 tasks were created
        self.assertEqual(len(tasks), 3, "Should have exactly 3 tasks")
        
        # Verify task 1 details
        task1 = tasks[0]
        self.assertEqual(task1["description"], "Morning call at tomorrow 8:00AM")
        self.assertEqual(task1["completed"], False)
        self.assertEqual(task1["created_at"], self.mock_timestamp)
        
        # Verify task 2 details
        task2 = tasks[1]
        self.assertEqual(task2["description"], "Date with Jimmy")
        self.assertEqual(task2["completed"], False)
        self.assertEqual(task2["created_at"], self.mock_timestamp)
        
        # Verify task 3 details
        task3 = tasks[2]
        self.assertEqual(task3["description"], "Make a reservation for the restaurant")
        self.assertEqual(task3["completed"], False)
        self.assertEqual(task3["created_at"], self.mock_timestamp)
        
        # Verify that view_tasks was called and displayed all tasks
        view_calls = [call for call in mock_print.call_args_list if '✗' in str(call)]
        self.assertEqual(len(view_calls), 3, "Should display 3 tasks when viewing")
        
        # Verify specific task content in output
        all_output = ' '.join([str(call) for call in mock_print.call_args_list])
        self.assertIn("Morning call at tomorrow 8:00AM", all_output)
        self.assertIn("Date with Jimmy", all_output)
        self.assertIn("Make a reservation for the restaurant", all_output)
        
        print("\n✅ E2E Test Results:")
        print(f"✓ Created {len(tasks)} tasks successfully")
        print("✓ All tasks have correct descriptions")
        print("✓ All tasks are marked as incomplete (✗)")
        print("✓ All tasks have proper timestamps")
        print("✓ View function displays all tasks correctly")
        print("\n🎉 Vickey's workflow completed successfully!")
        
    def test_task_persistence_after_creation(self):
        """Test that Vickey's tasks persist after being created"""
        
        # Create the 3 tasks
        test_todo_app.add_task("Morning call at tomorrow 8:00AM")
        test_todo_app.add_task("Date with Jimmy")
        test_todo_app.add_task("Make a reservation for the restaurant")
        
        # Verify tasks persist by reloading
        tasks_first_load = test_todo_app.load_tasks()
        tasks_second_load = test_todo_app.load_tasks()
        
        self.assertEqual(tasks_first_load, tasks_second_load)
        self.assertEqual(len(tasks_second_load), 3)
        
    @patch('builtins.print')
    def test_task_display_format(self, mock_print):
        """Test that tasks are displayed in the correct format for Vickey"""
        
        # Add Vickey's tasks
        test_todo_app.add_task("Morning call at tomorrow 8:00AM")
        test_todo_app.add_task("Date with Jimmy")
        test_todo_app.add_task("Make a reservation for the restaurant")
        
        # View tasks
        test_todo_app.view_tasks()
        
        # Check that all print calls include the expected format
        task_display_calls = [call for call in mock_print.call_args_list 
                            if '1. [✗]' in str(call) or '2. [✗]' in str(call) or '3. [✗]' in str(call)]
        
        self.assertEqual(len(task_display_calls), 3, "Should display 3 numbered tasks")
        
        # Verify numbering format (1., 2., 3.)
        output_str = ' '.join([str(call) for call in mock_print.call_args_list])
        self.assertIn("1. [✗]", output_str)
        self.assertIn("2. [✗]", output_str) 
        self.assertIn("3. [✗]", output_str)

def run_vickey_scenario():
    """
    Run Vickey's scenario manually for demonstration
    """
    print("=" * 60)
    print("🎯 VICKEY'S TODO APP - END-TO-END SCENARIO")
    print("=" * 60)
    
    # Create temporary test environment
    test_dir = tempfile.mkdtemp()
    original_tasks_file = test_todo_app.TASKS_FILE
    test_todo_app.TASKS_FILE = os.path.join(test_dir, "demo_tasks.json")
    
    try:
        print("\n📝 Vickey is creating her tasks...")
        
        # Add the 3 tasks
        print("\n1️⃣ Adding: Morning call at tomorrow 8:00AM")
        test_todo_app.add_task("Morning call at tomorrow 8:00AM")
        
        print("\n2️⃣ Adding: Date with Jimmy")
        test_todo_app.add_task("Date with Jimmy")
        
        print("\n3️⃣ Adding: Make a reservation for the restaurant")
        test_todo_app.add_task("Make a reservation for the restaurant")
        
        print("\n" + "="*50)
        print("📋 VICKEY'S COMPLETE TASK LIST:")
        print("="*50)
        test_todo_app.view_tasks()
        
        print("\n✅ All tasks created and displayed successfully!")
        print("🎉 Vickey's E2E scenario completed!")
        
    finally:
        # Cleanup
        test_todo_app.TASKS_FILE = original_tasks_file
        shutil.rmtree(test_dir)

if __name__ == '__main__':
    # Run the manual demonstration first
    run_vickey_scenario()
    
    print("\n" + "="*60)
    print("🧪 RUNNING AUTOMATED TESTS")
    print("="*60)
    
    # Run the automated tests
    unittest.main(verbosity=2)