from .task import Task
from typing import List, Optional

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys: List[int] = []         # Stores Task IDs for sorting
        self.values: List[Task] = []      # Stores the actual Task objects
        self.children: List['BTreeNode'] = []

# ---  The B-Tree Engine ---
class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(True)
        self.t = t  # Minimum degree (defines min/max keys)

    # ==========================
    # SEARCH
    # ==========================
    def search(self, k: int, node: Optional[BTreeNode] = None) -> Optional[Task]:
        """Returns the Task if found, else None."""
        if node is None:
            node = self.root

            

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        # Check if we found the key in this node
        if i < len(node.keys) and k == node.keys[i]:
            return node.values[i]

        # If leaf and not found, it doesn't exist
        if node.leaf:
            return None

        # Recurse to the correct child
        return self.search(k, node.children[i])

    # ==========================
    # INSERT
    # ==========================
    def insert(self, task: Task):
        k = task.id
        root = self.root
        
        # If root is full, tree grows in height
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, task)
        else:
            self._insert_non_full(root, task)

    def _insert_non_full(self, x: BTreeNode, task: Task):
        k = task.id
        i = len(x.keys) - 1
        
        if x.leaf:
            # Shift keys to make room
            x.keys.append(0)
            x.values.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                x.values[i + 1] = x.values[i]
                i -= 1
            x.keys[i + 1] = k
            x.values[i + 1] = task
        else:
            # Find child to descend into
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            
            # If child is full, split it first
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], task)

    def _split_child(self, x: BTreeNode, i: int):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        
        # Move last t-1 keys/values from y to z
        z.keys = y.keys[t:]
        z.values = y.values[t:]
        
        # If not leaf, move children too
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t] # Keep only first t children

        # Resize y
        mid_key = y.keys[t-1]
        mid_val = y.values[t-1]
        y.keys = y.keys[:t-1]
        y.values = y.values[:t-1]

        # Insert z into x's children
        x.children.insert(i + 1, z)
        x.keys.insert(i, mid_key)
        x.values.insert(i, mid_val)

    # ==========================
    # DELETE
    # ==========================
    def delete(self, k: int):
        self._delete_key(self.root, k)
        # If root becomes empty (and has children), shrink height
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete_key(self, x: BTreeNode, k: int):
        t = self.t
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1

        # Case 1: Key is in this node
        if i < len(x.keys) and x.keys[i] == k:
            if x.leaf:
                # 1a: Simple remove from leaf
                x.keys.pop(i)
                x.values.pop(i)
            else:
                # 1b: Key in internal node -> swap with predecessor/successor
                if len(x.children[i].keys) >= t:
                    pred_node = self._get_predecessor(x.children[i])
                    # Swap Data
                    x.keys[i] = pred_node.keys[-1]
                    x.values[i] = pred_node.values[-1]
                    # Recursively delete the swapped key from the child
                    self._delete_key(x.children[i], x.keys[i])
                elif len(x.children[i+1].keys) >= t:
                    succ_node = self._get_successor(x.children[i+1])
                    x.keys[i] = succ_node.keys[0]
                    x.values[i] = succ_node.values[0]
                    self._delete_key(x.children[i+1], x.keys[i])
                else:
                    # 1c: Both children are small -> Merge them
                    self._merge(x, i)
                    self._delete_key(x.children[i], k)

        # Case 2: Key is not here, find sub-tree
        else:
            if x.leaf:
                print(f"Key {k} not found.")
                return

            # Ensure the child we descend into has enough keys (>= t)
            flag = (i == len(x.keys))
            if len(x.children[i].keys) < t:
                self._fill(x, i)

            # Recurse
            if flag and i > len(x.keys):
                self._delete_key(x.children[i-1], k)
            else:
                self._delete_key(x.children[i], k)

    # --- Deletion Helpers ---
    def _get_predecessor(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node

    def _get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node

    def _fill(self, x, i):
        # Borrow from previous sibling
        if i != 0 and len(x.children[i-1].keys) >= self.t:
            self._borrow_from_prev(x, i)
        # Borrow from next sibling
        elif i != len(x.keys) and len(x.children[i+1].keys) >= self.t:
            self._borrow_from_next(x, i)
        # Merge siblings
        else:
            if i != len(x.keys):
                self._merge(x, i)
            else:
                self._merge(x, i-1)

    def _borrow_from_prev(self, x, i):
        child = x.children[i]
        sibling = x.children[i-1]

        # Rotate right: Sibling -> Parent -> Child
        child.keys.insert(0, x.keys[i-1])
        child.values.insert(0, x.values[i-1])
        
        x.keys[i-1] = sibling.keys.pop()
        x.values[i-1] = sibling.values.pop()

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, x, i):
        child = x.children[i]
        sibling = x.children[i+1]

        # Rotate left: Sibling -> Parent -> Child
        child.keys.append(x.keys[i])
        child.values.append(x.values[i])

        x.keys[i] = sibling.keys.pop(0)
        x.values[i] = sibling.values.pop(0)

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, x, i):
        child = x.children[i]
        sibling = x.children[i+1]
        t = self.t

        # Pull key from parent down into child
        child.keys.append(x.keys.pop(i))
        child.values.append(x.values.pop(i))

        # Merge sibling into child
        child.keys.extend(sibling.keys)
        child.values.extend(sibling.values)
        if not child.leaf:
            child.children.extend(sibling.children)

        # Remove sibling pointer
        x.children.pop(i+1)

    # ==========================
    # RANGE SEARCH
    # ==========================
    def search_range(self, start_id: int, end_id: int) -> List[Task]:
        """Returns all Tasks with IDs in the inclusive range [start_id, end_id]."""
        if start_id > end_id:
            start_id, end_id = end_id, start_id

        result: List[Task] = []
        self._search_range(self.root, start_id, end_id, result)
        return result

    def _search_range(self, node: BTreeNode, start_id: int, end_id: int, result: List[Task]):
        if not node or not node.keys:
            return

        i = 0
        while i < len(node.keys):
            key = node.keys[i]

            # Explore left child if it can contain keys within range.
            if not node.leaf and start_id <= key:
                self._search_range(node.children[i], start_id, end_id, result)

            # Add current key if within range.
            if start_id <= key <= end_id:
                result.append(node.values[i])

            # If current key exceeds end_id, no need to continue.
            if key > end_id:
                return

            i += 1

        # Explore rightmost child if range can extend beyond last key.
        if not node.leaf and end_id >= node.keys[-1]:
            self._search_range(node.children[i], start_id, end_id, result)


    # ==========================
    # PRINT (Traversal)
    # ==========================
    def traverse(self, node=None, level=0):
        if node is None:
            node = self.root
        
        print(f"Level {level}: {node.keys}")
        if not node.leaf:
            for child in node.children:
                self.traverse(child, level + 1)