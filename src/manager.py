from .core import BTree, Task

class TaskManager:
    def __init__(self):
        self._tree = BTree(t=3)

    def add_task(self, id, start, end, val, name):
        new_task = Task(id, start, end, val, name)
        self._tree.insert(new_task)

    def get_task(self, task_id):
        return self._tree.search(task_id)

    def remove_task(self, task_id):
        self._tree.delete(task_id)

    def display_all(self):
        print("\n--- ⁂ Current Task Hierarchy (B-Tree) ⁂ ---")
        self._tree.traverse()