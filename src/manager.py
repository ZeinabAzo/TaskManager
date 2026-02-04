from .core.BTree import BTree
from .core.intervalTree import IntervalTree
from .core.task import Task

class TaskManager:
    def __init__(self):
        self._Btree = BTree()
        self.interval = IntervalTree()

    def add_task(self, id, start, end, val):

        if self.search_overlaps(id, start, end):
            return
        
        new_task = Task(id, start, end, val)
        self._Btree.insert(new_task)
        self.interval.add(new_task)

    def search_overlaps(self, id, start, end):
        overlaps : list[Task] = self.interval.search_overlap(start, end) # returns a list of tasks.
        if overlaps:
            for task in overlaps:
                print(f"there is a conflict between {task.id} and {id}")
            return True
        else:
            return False

    def get_task_id(self, task_id: int):
        return self._Btree.search(task_id)
    
    def get_task_range(self, start_time: int, end_time: int):
        return self.interval.search_overlap(start_time, end_time)

    def remove_task(self, task_id):
        self.interval.delete(self.get_task_id(task_id)) #check for time complicity
        self._Btree.delete(task_id)

    def update_task(self, id, start, end, val):
        self.remove_task(id)
        self.add_task(id, start, end, val)

    def get_task_id_range(self, start_id: int, end_id: int):
        return self._Btree.search_range(start_id, end_id)

    def display_all(self):
        print("\n--- ⁂ Current Task Hierarchy (B-Tree) ⁂ ---")
        self._tree.traverse()