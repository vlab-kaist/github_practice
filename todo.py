import json
import os
from datetime import datetime


class TodoApp:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.todos = json.load(f)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def add(self, title, priority="medium"):
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "priority": priority,
            "done": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        }
        self.todos.append(todo)
        self.save()
        return todo

    def complete(self, todo_id):
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["done"] = True
                todo["completed_at"] = datetime.now().isoformat()
                self.save()
                return todo
        return None

    def delete(self, todo_id):
        self.todos = [t for t in self.todos if t["id"] != todo_id]
        self.save()

    def list_all(self):
        return self.todos

    def list_pending(self):
        return [t for t in self.todos if not t["done"]]

    def list_completed(self):
        return [t for t in self.todos if t["done"]]

    def search(self, keyword):
        return [t for t in self.todos if keyword.lower() in t["title"].lower()]

    def get_stats(self):
        total = len(self.todos)
        done = len([t for t in self.todos if t["done"]])
        pending = total - done
        return {"total": total, "done": done, "pending": pending}


if __name__ == "__main__":
    app = TodoApp()
    app.add("파이썬 공부하기", "high")
    app.add("장보기", "low")
    app.add("운동하기", "medium")
    app.add("깃허브 연습", "high")
    app.complete(1)

    print("=== 전체 할일 ===")
    for t in app.list_all():
        status = "✅" if t["done"] else "❌"
        print(f"  {status} [{t['priority']}] {t['title']}")

    print(f"\n통계: {app.get_stats()}")
