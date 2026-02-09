from .task import Task
from typing import Optional, List

# Assuming Task is already defined in core.py
# from .core import Task 

class IntervalNode:
    def __init__(self, task: Task):
        self.task = task
        self.low = task.start_time
        self.high = task.end_time
        # 'max_val' is the maximum 'end_time' in the subtree rooted at this node
        self.max = task.end_time
        self.left: Optional['IntervalNode'] = None
        self.right: Optional['IntervalNode'] = None

class IntervalTree:
    def __init__(self):
        self.root: Optional[IntervalNode] = None

    # ==========================
    # ADD (INSERT)
    # ==========================
    def add(self, task: Task):
        node = IntervalNode(task)
        if not self.root:
            self.root = node
        else:
            self.root = self._insert(self.root, node)

    def _insert(self, root: IntervalNode, node: IntervalNode):
        # 1. Standard BST Insert (sorted by low/start_time)
        if node.low < root.low:
            if root.left:
                self._insert(root.left, node)
            else:
                root.left = node
        else:
            if root.right:
                self._insert(root.right, node)
            else:
                root.right = node
        
        # 2. Update Max Value on the way up
        if root.max < node.high:
            root.max = node.high
            
        return root

    # ==========================
    # SEARCH (Find Overlaps)
    # ==========================
    def search_overlap(self, start: int, end: int) -> List[Task]:
        """Returns all tasks that overlap with the interval [start, end]."""
        result = []
        self._search(self.root, start, end, result)
        return result

    def _search(self, node: IntervalNode, start: int, end: int, result: List[Task]):
        if not node:
            return

        # Check for overlap: 
        # (Node.low <= Query.end) AND (Node.high >= Query.start)
        if node.low < end and node.high > start:
            result.append(node.task)

        # Optimization: Only go left if the left child's max is >= start
        if node.left and node.left.max >= start:
            self._search(node.left, start, end, result)
        
        # Always check right if node.low is less than query end
        # (Since the tree is sorted by low, valid intervals could be on the right)
        if node.right and node.low <= end:
            self._search(node.right, start, end, result)

    # ==========================
    # DELETE
    # ==========================
    def delete(self, task: Task):
        """Deletes a task by its start_time (low) and checks for exact object match."""
        self.root = self._delete(self.root, task)

    def _delete(self, root: IntervalNode, task: Task):
        if not root:
            return None

        if task.start_time < root.low:
            root.left = self._delete(root.left, task)
        elif task.start_time > root.low:
            root.right = self._delete(root.right, task)
        else:
            # Found a node with the same start time. 
            # In case of duplicates, ensure it's the exact same task ID/Object
            if root.task.id == task.id:
                # Node with only one child or no child
                if not root.left:
                    return root.right
                elif not root.right:
                    return root.left

                # Node with two children: Get inorder successor (smallest in right subtree)
                temp = self._min_value_node(root.right)
                
                # Copy the successor's data to this node
                root.task = temp.task
                root.low = temp.low
                root.high = temp.high
                
                # Delete the inorder successor
                root.right = self._delete(root.right, temp.task)
            else:
                # If start times match but IDs don't, keep searching right (handle duplicates)
                root.right = self._delete(root.right, task)

        # Update Max Value after deletion
        self._update_max(root)
        return root

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _update_max(self, node):
        """Recalculates the max value for a node based on its children."""
        node.max = node.high
        if node.left and node.left.max > node.max:
            node.max = node.left.max
        if node.right and node.right.max > node.max:
            node.max = node.right.max


    # PRINT
    
    def print_tree(self):
        """Pretty-prints the Interval Tree structure."""
        if not self.root:
            print("(empty Interval Tree)")
            return
        print("root")
        self._print_node(self.root, "", True)

    def _print_node(self, node: Optional[IntervalNode], prefix: str, is_last: bool):
        if not node:
            return

        connector = "└── " if is_last else "├── "
        print(
            f"{prefix}{connector}"
            f"id={node.task.id}, interval=[{node.low}, {node.high}], max={node.max}, value={node.task.value}"
        )

        children: List[tuple[str, IntervalNode]] = []
        if node.left:
            children.append(("left", node.left))
        if node.right:
            children.append(("right", node.right))


        child_prefix = prefix + ("    " if is_last else "│   ")
        for idx, (label, child) in enumerate(children):
            is_child_last = idx == len(children) - 1
            branch_connector = "└── " if is_child_last else "├── "
            print(f"{child_prefix}{branch_connector}{label}")
            next_prefix = child_prefix + ("    " if is_child_last else "│   ")
            self._print_node(child, next_prefix, True)



