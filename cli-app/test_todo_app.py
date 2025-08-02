# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(description):
    tasks = load_tasks()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.append({
        "description": description,
        "completed": False,
        "created_at": now,
        "added_at": now
    })
    save_tasks(tasks)
    print(f"已添加新任務（建立時間：{now}）。")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("目前沒有任務。")
        return
    for idx, task in enumerate(tasks, 1):
        status = "✔" if task["completed"] else "✗"
        created = task.get("created_at", "未知時間")
        print(f"{idx}. [{status}] {task['description']}（建立時間：{created}）")

def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("任務已標記為完成。")
    else:
        print("無效的任務編號。")

def delete_task(indices=None):
    tasks = load_tasks()
    if not tasks:
        print("目前沒有任務。")
        return
        
    if indices == 'all':
        tasks.clear()
        save_tasks(tasks)
        print("已刪除所有任務。")
        return
        
    if isinstance(indices, str):
        # Handle multiple indices like "1,2,3"
        try:
            indices = [int(i.strip()) - 1 for i in indices.split(',')]
            indices.sort(reverse=True)  # Sort in reverse to delete from end first
        except ValueError:
            print("無效的任務編號格式。請使用逗號分隔的數字，例如：1,2,3")
            return
            
    if isinstance(indices, int):
        indices = [indices]
        
    valid_indices = [i for i in indices if 0 <= i < len(tasks)]
    if not valid_indices:
        print("無效的任務編號。")
        return
        
    for index in valid_indices:
        tasks.pop(index)
    save_tasks(tasks)
    print(f"已刪除 {len(valid_indices)} 個任務。")


def main():
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