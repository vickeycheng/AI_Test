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
    tasks.append({"description": description, "completed": False})
    save_tasks(tasks)
    print("已添加新任務。")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("目前沒有任務。")
        return
    for idx, task in enumerate(tasks, 1):
        status = "✔" if task["completed"] else "✗"
        created = task.get("created_at", "未知時間")
        print(f"{idx}. [{status}] {task['description']}")

def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("任務已標記為完成。")
    else:
        print("無效的任務編號。")

def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
        print("任務已刪除。")
    else:
        print("無效的任務編號。")

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
            view_tasks()
            idx = input("請輸入要刪除的任務編號: ")
            if idx.isdigit():
                delete_task(int(idx) - 1)
            else:
                print("請輸入有效的數字。")
        elif choice == "5":
            print("再見！")
            break
        else:
            print("請輸入有效選項。")
            
if __name__ == "__main__":
    main()