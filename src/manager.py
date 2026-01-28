from .core import BTree, intervalTree
from .core.models import Task

class TaskManager:
    def __init__(self):
        self._Btree = BTree(t=3)
        self.interval = intervalTree()

    def add_task(self, id, start, end, val):

        overlaps : list[Task] = self.interval.search_overlap(start, end) # returns a list of tasks.
        if overlaps:
            for task in overlaps:
                print(f"there is a conflict between {task.id} and {id}")
            return
        
        new_task = Task(id, start, end, val)
        self._Btree.insert(new_task)
        self.interval.add(new_task)

    def get_task_id(self, task_id: int):
        return self._Btree.search(task_id)
    
    def get_task_range(self, start_time: int, end_time: int):
        return self.interval.search_overlap(start_time, end_time)

    def remove_task(self, task_id):
        self._Btree.delete(task_id)
        self.interval.delete(self.get_task_id(task_id)) #check for time complicity

    def update_task(self, id, start, end, val):
        self.remove_task(id)
        self.add_task(id, start, end, val)


    def display_all(self):
        print("\n--- ⁂ Current Task Hierarchy (B-Tree) ⁂ ---")
        self._tree.traverse()