import argparse
import os
import sys
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.txt')
COMPLETED_FILE = os.path.join(os.path.dirname(__file__), 'completed.txt')


def read_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f]


def write_tasks(tasks):
    # atomic write: write to temp then replace
    tmp = TASKS_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        for t in tasks:
            f.write(t + '\n')
    os.replace(tmp, TASKS_FILE)


def add_task(task_text):
    if not task_text.strip():
        print('Cannot add empty task.')
        return
    tasks = read_tasks()
    tasks.append(task_text)
    write_tasks(tasks)
    print(f"Added task: {task_text}")


def list_tasks():
    tasks = read_tasks()
    if not tasks:
        print('No tasks for today. Enjoy your free time!')
        return
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t}")


def complete_task(index):
    tasks = read_tasks()
    if not tasks:
        print('No tasks to complete.')
        return
    if index < 1 or index > len(tasks):
        print(f'Invalid task number: {index}')
        return
    completed = tasks.pop(index - 1)
    write_tasks(tasks)
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(COMPLETED_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {completed}\n")
    print(f"Completed task: {completed}")


def build_parser():
    parser = argparse.ArgumentParser(prog='tasks', description='Simple CLI task manager')
    sub = parser.add_subparsers(dest='command')

    add_p = sub.add_parser('add', help='Add a new task')
    add_p.add_argument('task', nargs='*', help='Task description (quoted or as separate words)')

    sub.add_parser('list', help='List all tasks')

    comp_p = sub.add_parser('complete', help='Mark a task as complete by number')
    comp_p.add_argument('number', type=int, help='Task number to complete (from `list`)')

    return parser


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == 'add':
        text = ' '.join(args.task).strip()
        if not text:
            # interactive prompt fallback
            try:
                text = input('Task description: ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\nCancelled.')
                return
        add_task(text)
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'complete':
        complete_task(args.number)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
