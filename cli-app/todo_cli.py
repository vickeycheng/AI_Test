# -*- coding: utf-8 -*-
"""
CLI TODO Application
Command-line interface for task management using shared core functionality
"""

import sys
import os

# Add shared folder to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shared'))

from todo_core import (
    load_tasks, save_tasks, add_task_data, complete_task_data, 
    delete_task_data, delete_completed_tasks_data, delete_all_tasks_data,
    get_task_stats
)

def add_task(description):
    """Add a new task with CLI output"""
    task = add_task_data(description)
    if task:
        print(f"已添加新任務（建立時間：{task['created_at']}）。")
    else:
        print("添加任務失敗。")

def view_tasks():
    """Display all tasks in CLI format"""
    stats = get_task_stats()
    tasks = stats['tasks']
    
    if not tasks:
        print("目前沒有任務。")
        return
    
    for idx, task in enumerate(tasks, 1):
        status = "✔" if task.get("completed", False) else "✗"
        created = task.get("created_at", "未知時間")
        print(f"{idx}. [{status}] {task['description']}（建立時間：{created}）")

def complete_task(index):
    """Complete a task by display index (1-based)"""
    tasks = load_tasks()
    
    if 0 <= index < len(tasks):
        task_id = tasks[index].get('id')
        if complete_task_data(task_id):
            print("任務已標記為完成。")
        else:
            print("更新任務失敗。")
    else:
        print("無效的任務編號。")

def delete_task(indices=None):
    """Delete tasks by various methods"""
    stats = get_task_stats()
    tasks = stats['tasks']
    
    if not tasks:
        print("目前沒有任務。")
        return
        
    if indices == 'all':
        if delete_all_tasks_data():
            print("已刪除所有任務。")
        else:
            print("刪除失敗。")
        return
        
    if isinstance(indices, str):
        # Handle multiple indices like "1,2,3"
        try:
            display_indices = [int(i.strip()) for i in indices.split(',')]
            # Convert display indices (1-based) to actual task IDs
            task_ids = []
            for display_idx in display_indices:
                if 1 <= display_idx <= len(tasks):
                    task_ids.append(tasks[display_idx - 1].get('id'))
            
            deleted_count = 0
            for task_id in task_ids:
                if delete_task_data(task_id):
                    deleted_count += 1
            
            print(f"已刪除 {deleted_count} 個任務。")
            return
            
        except ValueError:
            print("無效的任務編號格式。請使用逗號分隔的數字，例如：1,2,3")
            return
            
    if isinstance(indices, int):
        # Single task deletion by display index
        if 1 <= indices + 1 <= len(tasks):
            task_id = tasks[indices].get('id')
            if delete_task_data(task_id):
                print("已刪除 1 個任務。")
            else:
                print("刪除失敗。")
        else:
            print("無效的任務編號。")

def main():
    """Main CLI application loop"""
    while True:
        print("\n待辦事項應用")
        print("1. 添加新任務")
        print("2. 查看所有任務")
        print("3. 標記任務為完成")
        print("4. 刪除任務")
        print("5. 退出")
        
        choice = input("請選擇功能 (1-5): ")
        
        if choice == "1":
            desc = input("請輸入任務描述: ")
            add_task(desc)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_tasks()
            idx = input("請輸入要標記完成的任務編號: ")
            if idx.isdigit():
                complete_task(int(idx) - 1)
            else:
                print("請輸入有效的數字。")
        elif choice == "4":
            print("\n刪除任務選項：")
            print("1. 刪除單個任務")
            print("2. 刪除多個任務")
            print("3. 刪除所有任務")
            print("4. 返回主選單")
            delete_choice = input("請選擇刪除方式 (1-4): ")
            
            if delete_choice == "1":
                view_tasks()
                idx = input("請輸入要刪除的任務編號: ")
                if idx.isdigit():
                    delete_task(int(idx) - 1)
                else:
                    print("請輸入有效的數字。")
            elif delete_choice == "2":
                view_tasks()
                indices = input("請輸入要刪除的任務編號（用逗號分隔，例如：1,2,3）: ")
                delete_task(indices)
            elif delete_choice == "3":
                confirm = input("確定要刪除所有任務嗎？(y/n): ")
                if confirm.lower() == 'y':
                    delete_task('all')
            elif delete_choice == "4":
                continue
            else:
                print("請輸入有效選項。")
        elif choice == "5":
            print("再見！")
            break
        else:
            print("請輸入有效選項。")

if __name__ == "__main__":
    main()