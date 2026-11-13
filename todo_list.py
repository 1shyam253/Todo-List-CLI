#!/usr/bin/env python3
"""Todo List CLI - add, list, complete and delete tasks (stored in JSON)."""
import argparse, json, os, sys
DEFAULT_FILE = "todos.json"

def load(path):
    if not os.path.exists(path): return []
    with open(path, encoding="utf-8") as f: return json.load(f)

def save(path, tasks):
    with open(path, "w", encoding="utf-8") as f: json.dump(tasks, f, indent=2)

def main(argv=None):
    p = argparse.ArgumentParser(description="Todo List CLI")
    p.add_argument("--file", default=DEFAULT_FILE, help="JSON file to store tasks")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="Add a task"); a.add_argument("task")
    sub.add_parser("list", help="List tasks")
    c = sub.add_parser("complete", help="Mark a task done"); c.add_argument("id", type=int)
    d = sub.add_parser("delete", help="Delete a task"); d.add_argument("id", type=int)
    args = p.parse_args(argv)
    tasks = load(args.file)
    if args.cmd == "add":
        tasks.append({"id": (max((t["id"] for t in tasks), default=0) + 1), "task": args.task, "done": False})
        save(args.file, tasks); print(f"Added: {args.task}")
    elif args.cmd == "list":
        if not tasks: print("No tasks yet.")
        for t in tasks: print(f"[{'x' if t['done'] else ' '}] {t['id']}. {t['task']}")
    elif args.cmd == "complete":
        for t in tasks:
            if t["id"] == args.id: t["done"] = True; save(args.file, tasks); print(f"Completed task {args.id}"); return
        print(f"No task with id {args.id}", file=sys.stderr); return 1
    elif args.cmd == "delete":
        new = [t for t in tasks if t["id"] != args.id]
        if len(new) == len(tasks): print(f"No task with id {args.id}", file=sys.stderr); return 1
        save(args.file, new); print(f"Deleted task {args.id}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
