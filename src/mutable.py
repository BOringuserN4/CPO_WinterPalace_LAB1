"""
For your data structure you should implement the following features (in the brackets you can see
    examples of API for single-linked list):
    • Add a new element (lst.add(3))
    • Set an element with specific index / key (lst.set(1, 3)) if applicable.
    • Remove an element by (lst.remove(3)):
        - index for lists
        - key for dictionaries
        - value for sets value
    • Access:
        - size (lst.size())
        - is member (lst.member(3))
        - reverse (lst.reverse() (if applicable)
    • Conversion from/to built-in list (you should avoid of usage these function into your library):
        - from_list (lst.from_list([12, 99, 37]))
        - to_list (lst.to_list())
    • Filter data structure by specific predicate (lst.filter(is_even))
    • Map¹ structure by specific function (lst.map(increment))
    • Reduce² – process structure elements to build a return value by specific functions (lst.reduce(sum))
    • Data structure should be an iterator³ in Python style [Sayfan, 2016, Chapter 7. Classes & Iterators].
    • Data structure should be a monoid and implement empty and concat methods:

        Suppose that S is a set, and • is some binary operation S×S→S, then S with • (concat) is
        a monoid if it satisfies the following two axioms:

        Associativity
            For all a, b and c in S, the equation (a•b)•c = a•(b•c) holds.
        Identity element
            There exists an element e (empty) in S such that for every element a in S, the equations
            e•a = a•e = a hold.
        — Wikipedia - Monoid ⁴
Pay extra attention to return values and corner cases like:
    • What should happen, if a user puts None value to the data structure?
    • What should happen, if a user puts elements with different types (e.g., strings and numbers)?
"""


class BTNode(object):
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        return self.value


class BTree(object):
    def __init__(self, root=None):
        self.root = root
        self.level_queue = []
        self.cur = 0

    """
    Add a new element
    """

    def add(self, value):
        if self.root is None:
            self.root = BTNode(value)
        else:
            queue = list()
            queue.append(self.root)

            while len(queue) > 0:
                node = queue.pop(0)
                if not node.lchild:
                    node.left = BTNode(value)
                    return
                else:
                    queue.append(node.lchild)

                if not node.rchild:
                    node.right = BTNode(value)
                    return
                else:
                    queue.append(node.rchild)

    # Set an element with specific index / key
    # def set_element(self, value):
    #     value = 1
    #     return value

    def parent(self, value):
        if self.root.value == value:
            return None
        """Use the stack to iterate all nodes"""
        queue = list()
        queue.append(self.root)
        while len(queue):
            """Get the first element of the tmp stack"""
            tmp = queue.pop(0)
            if tmp.left and tmp.left.value == value:
                return tmp
            if tmp.right and tmp.right.value == value:
                return tmp
            """push the value to stack"""
            if tmp.left is not None:
                queue.append(tmp.left)
            if tmp.right is not None:
                queue.append(tmp.right)
        return None

    """
    Remove an element by 
    - value for sets value
    """

    def remove(self, value):
        if self.root is None:
            return False
        if self.root.value == value:
            self.root = None
            return True
        parent_node = self.parent(value)
        # If parent_node is not None
        if parent_node:
            # The parent_node of the deleted node has been found, now just find the side that should be deleted
            if parent_node.left.value == value:
                delete_node = parent_node.left
            else:
                delete_node = parent_node.right
            # If we want to delete the node, we should refactor the binary tree
            if delete_node.left is None:
                if parent_node.left.value == value:
                    parent_node.left = delete_node.right
                else:
                    parent_node.right = delete_node.right
                return True
            elif delete_node.right is None:
                if parent_node.left.value == value:
                    parent_node.left = delete_node.left
                else:
                    parent_node.right = delete_node.left
                return True
            # This is the most complicated case, the deleted node has both left and right children
            else:
                # Previous node and next node are seen as temporary nodes
                pre_node = delete_node
                next_node = delete_node.right

                if next_node.left is None:
                    pre_node.right = next_node.right
                    next_node.left = delete_node.left
                    next_node.right = delete_node.right
                else:
                    while next_node.left:
                        pre_node = next_node
                        next_node = next_node.left
                    pre_node.left = next_node.right
                    next_node.left = delete_node.left
                    next_node.right = delete_node.right

                if parent_node.left.value == value:
                    parent_node.left = next_node
                else:
                    parent_node.right = next_node
                return True
            # Until here the node has been deleted and the tree has been refactored
        else:
            return False

    """
    Access:
    - size (lst.size())
    - is member (lst.member(3))
    - reverse (lst.reverse() (if applicable)
    """

    def size(self):
        if self.root is None:
            return 0
        # Use recursive method
        left_sum = BTree(self.root.left).size()
        right_sum = BTree(self.root.right).size()
        # Exit conditions
        if left_sum == 0 and right_sum == 0:
            return 1
        elif left_sum == 0:
            return 1 + right_sum
        elif right_sum == 0:
            return 1 + left_sum
        else:
            return 1 + left_sum + right_sum

    # consistent with parent function idea
    def is_member(self, value) -> bool:
        if self.root.value == value:
            return True
        node_stack = list()
        node_stack.append(self.root)
        while len(node_stack):
            tmp = node_stack.pop(0)
            if tmp.left and tmp.left.value == value:
                return True
            if tmp.right and tmp.right.value == value:
                return True
            if tmp.left is not None:
                node_stack.append(tmp.left)
            if tmp.right is not None:
                node_stack.append(tmp.right)
        return False

    """
    Conversion from/to built-in list (you should avoid of usage these function into your library):
    - from_list (lst.from_list([12, 99, 37]))
    - to_list (lst.to_list())
    """

    def from_list(self, lst):
        for index in range(len(lst)):
            self.add(lst[index])
        return self

    # consistent with size function idea
    def to_list(self):
        if self.root is None:
            return []
        else:
            left_lst = BTree(self.root.left).to_list()
            right_lst = BTree(self.root.right).to_list()
            # Exit conditions
            if left_lst is None and right_lst is None:
                return [self.root.value]
            if left_lst is None:
                return [self.root.value] + right_lst
            if right_lst is None:
                return left_lst + [self.root.value]
            return left_lst + [self.root.value] + right_lst

    """
    Filter data structure by specific predicate (lst.filter(is_even))
    """

    def filter(self, p) -> list:
        lst = self.to_list()
        i = 0
        result = []
        while i < len(lst):
            if p(lst[i]):
                result.append(lst[i])
            else:
                i += 1
        return result

    """
    Map structure by specific function (lst.map(increment))
    """

    # consistent with parent function idea
    def map(self, f):
        if self.root is None:
            return None
        queue = list()
        queue.append(self.root)
        while len(queue):
            tmp = queue.pop(0)
            tmp.value = f(tmp.value)
            if tmp.left is not None:
                queue.append(tmp.left)
            if tmp.right is not None:
                queue.append(tmp.right)
        return self

    """
    Reduce – process structure elements to build a return value by specific functions(lst.reduce(sum))
    """

    # I have some doubts about this function, is this to compress the elements?
    def reduce(self, f, initial_state=0):
        state = initial_state
        lst = self.to_list()
        # i = 0
        # while i < len(lst):
        #    state = f(state, lst[i])
        #    i += 1
        # Apparently for is better than while here
        for i in range(len(lst)):
            state = f(state, lst[i])
        return state

    """
    Data structure should be an iterator in Python style
    """

    # still have problem
    def __iter__(self):
        if self.root is None:
            self.cur = 0
            return self
        self.level_queue.append(self.root)
        self.cur += 1
        return self

    # still have problem
    def __next__(self):
        if self.cur == 0:
            raise StopIteration
        if self.root.left is not None:
            self.level_queue.append(self.root.left)
        if self.root.right is not None:
            self.level_queue.append(self.root.right)
        tmp = self.level_queue[self.cur - 1].value
        if self.cur < len(self.level_queue):
            self.root = self.level_queue[self.cur]
            self.cur += 1
        else:
            self.root = self.level_queue[0]
            self.cur = 0
        return tmp

    """
    Data structure should be a monoid and implement empty and concat methods
    """

    # still have problem
    def empty(self):
        return None

    # still have problem
    def concat(self, bt1, bt2):
        if not bt1:
            return bt2
        if not bt2:
            return bt1
        new_root = BTNode(bt1.value + bt2.value)
        new_root.left = self.concat(bt1.left, bt2.left)
        new_root.right = self.concat(bt1.right, bt2.right)
        return new_root
