import argparse
import json
import os

# The name of our data file
DATA_FILE = 'tasks.json'
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_data_file():
    """Creates the tasks.json file with empty structure if it doesn't exist."""
    file_path = os.path.join(DATA_DIR, DATA_FILE)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f, indent=4)

def load_tasks():
    """Loads tasks from the JSON file. Returns empty list if file doesn't exist."""
    ensure_data_file()  # Make sure the file exists
    file_path = os.path.join(DATA_DIR, DATA_FILE)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    "Saves the list of tasks to the JSON file."
    file_path = os.path.join(DATA_DIR, DATA_FILE)
    with open(file_path, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    "Adds a new task to the list."
    tasks = load_tasks()
    tasks.append({'id': len(tasks) + 1, 'description': description, 'status': 'pending'})
    save_tasks(tasks)
    print(f"Added task: '{description}'")

def list_tasks():
    "Lists all tasks."
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(f"[{task['id']}] {task['description']} ({task['status']})")

def search_tasks(search_term):
    "Searches for tasks containing the search term."
    tasks = load_tasks()
    found_tasks = [task for task in tasks if search_term.lower() in task['description'].lower()]

    if not found_tasks:
        print(f"No tasks found matching '{search_term}'.")
        return

    print(f"Found {len(found_tasks)} task(s) matching '{search_term}':")
    for task in found_tasks:
        print(f"[{task['id']}] {task['description']} ({task['status']})")

def main():
    parser = argparse.ArgumentParser(description="A simple command-line task manager.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # 'add' command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', type=str, help='Makes an addition to the task list')

    # 'list' command
    list_parser = subparsers.add_parser('list', help='List all tasks')

    # 'search' command
    search_parser = subparsers.add_parser('search', help='Search for a task')
    search_parser.add_argument('term', type=str, help='searches for any task that includes the parameter')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'search':
        search_tasks(args.term)

if __name__ == "__main__":
    main()