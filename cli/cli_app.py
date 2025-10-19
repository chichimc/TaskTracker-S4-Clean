# cli/cli_app.py

from app.services.task_storage import load_tasks, save_tasks

def add_task():
    tasks = load_tasks()
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    task_id = max([task["id"] for task in tasks], default=0) + 1
    task = {"id": task_id, "title": title, "description": description}
    tasks.append(task)
    save_tasks(tasks)
    print("Task added!")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
    for task in tasks:
        print(f"[{task['id']}] {task['title']} - {task['description']}")

def main():
    while True:
        print("\n1. Add Task\n2. View Tasks\n3. Quit")
        choice = input("Select: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()