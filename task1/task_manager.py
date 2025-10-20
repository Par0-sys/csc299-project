#!/usr/bin/env python3
"""Simple task manager CLI.

Commands:
  add "title" [--desc "description"] [--tags tag1,tag2]
  list [--tag TAG]
  search QUERY

Data is stored in data/tasks.json relative to this file.
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    tags: List[str] = None
    created_at: str = ""

    def to_dict(self):
        d = asdict(self)
        d["tags"] = d.get("tags") or []
        return d


def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"tasks": []}, f, indent=2)


def read_tasks() -> List[Task]:
    ensure_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    tasks = []
    for t in data.get("tasks", []):
        tasks.append(Task(
            id=t.get("id"),
            title=t.get("title", ""),
            description=t.get("description", ""),
            tags=t.get("tags", []) or [],
            created_at=t.get("created_at", ""),
        ))
    return tasks


def write_tasks(tasks: List[Task]):
    ensure_data_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"tasks": [t.to_dict() for t in tasks]}, f, indent=2)


def add_task(title: str, description: str = "", tags: Optional[List[str]] = None) -> Task:
    tasks = read_tasks()
    next_id = max((t.id for t in tasks), default=0) + 1
    created_at = datetime.utcnow().isoformat() + "Z"
    task = Task(id=next_id, title=title, description=description, tags=tags or [], created_at=created_at)
    tasks.append(task)
    write_tasks(tasks)
    return task


def list_tasks(tag: Optional[str] = None) -> List[Task]:
    tasks = read_tasks()
    if tag:
        tasks = [t for t in tasks if tag in (t.tags or [])]
    return tasks


def search_tasks(query: str) -> List[Task]:
    q = query.lower()
    tasks = read_tasks()
    results = [t for t in tasks if q in t.title.lower() or q in (t.description or "").lower() or any(q in ta.lower() for ta in (t.tags or []))]
    return results


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(prog="task_manager", description="Simple JSON-backed task manager CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("--desc", default="", help="Description")
    p_add.add_argument("--tags", default="", help="Comma-separated tags")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--tag", default="", help="Filter by tag")

    p_search = sub.add_parser("search", help="Search tasks")
    p_search.add_argument("query", help="Search query")

    args = parser.parse_args(argv)

    if args.cmd == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        task = add_task(args.title, args.desc, tags)
        print(f"Added task #{task.id}: {task.title}")

    elif args.cmd == "list":
        tag = args.tag or None
        tasks = list_tasks(tag)
        if not tasks:
            print("No tasks found.")
            return
        for t in tasks:
            tags = ",".join(t.tags or [])
            print(f"#{t.id} {t.title} [{tags}]\n  {t.description}")

    elif args.cmd == "search":
        results = search_tasks(args.query)
        if not results:
            print("No results.")
            return
        for t in results:
            tags = ",".join(t.tags or [])
            print(f"#{t.id} {t.title} [{tags}]\n  {t.description}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
