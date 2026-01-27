from .core import BTree, Task, intervalTree

class TaskManager:
    def __init__(self):
        self._Btree = BTree(t=3)
        self.interval = intervalTree()

    def add_task(self, id, start, end, val):
        new_task = Task(id, start, end, val)
        self._Btree.insert(new_task)
        self.interval.add(new_task)

    def get_task_id(self, task_id: int):
        return self._Btree.search(task_id)
    
    def get_task_range(self, start_time: int, end_time: int):
        return self.interval.search_overlap(start_time, end_time)

    def remove_task(self, task_id):
        self._Btree.delete(task_id)

    def display_all(self):
        print("\n--- ⁂ Current Task Hierarchy (B-Tree) ⁂ ---")
        self._tree.traverse()