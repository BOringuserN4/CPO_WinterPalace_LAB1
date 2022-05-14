from typing import TypeVar, Any, Callable, List, Iterator, Generic

T = TypeVar('T')
T1 = TypeVar('T1', str, int, float)


class BTNode(Generic[T]):
    def __init__(self, value: Any = None,
                 left: Any = None, right: Any = None) -> None:
        """
        init the BTNode
        :param value: None
        :param left: None
        :param right: None
        """
        self.value = value
        self.left = left
        self.right = right

    def get_value(self) -> Any:
        """return value"""
        return self.value


# This class is used to provide static values
class Value(Generic[T]):
    value: int = 0

    def get_vlaue(self) -> int:
        """get value"""
        return Value.value

    def set_value(self, item: int) -> int:
        """set value"""
        Value.value = item
        return Value.value


class BTree(Generic[T]):
    def __init__(self, root: Any = None) -> None:
        """
        init the BTree
        :param root: root
        """
        self.root = root
        self.iter_queue = []  # type: List[Any]
        self.deep = 0

    """
    Add a new element
    """

    def add(self, value: T1) -> None:
        """
        add node to tree
        """
        if self.root is None:
            self.root = BTNode(value)
        else:
            queue = list()
            queue.append(self.root)

            while len(queue) > 0:
                node = queue.pop(0)
                if not node.left:
                    node.left = BTNode(value)
                    return
                else:
                    queue.append(node.left)

                if not node.right:
                    node.right = BTNode(value)
                    return
                else:
                    queue.append(node.right)

    """
    Set an element with specific index / key (lst.set(1, 3))
    if applicable.In this case, I can only convert the bt
    tree into a list type and then modify the value in the list.
    """

    def set_element(self, pos: int,
                    value: T1) -> Any:
        """
        Set an element with specific index / key
        """
        tmp_list = self.to_list()
        length = len(tmp_list)
        if pos < 0 or pos > length:
            return False
        else:
            tmp_list[pos] = value
            self.root = None
            self.from_list(tmp_list)
            return self

    """
    Parent method is used in reduce function and
    some of methods using the same idea
    """

    def parent(self, value: T1) -> Any:
        """
        Parent method is used in reduce function
        """
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

    def remove(self, value: T1) -> bool:
        """
        Remove an element
        """
        if self.root is None:
            return False
        if self.root.value == value:
            self.root = None
            return True
        parent_node = self.parent(value)
        # If parent_node is not None
        if parent_node:
            # The parent_node of the deleted node has been found,
            # now just find the side that should be deleted
            if parent_node.left.value == value:
                delete_node = parent_node.left
            else:
                delete_node = parent_node.right
            # If we want to delete the node, we should
            # refactor the binary tree
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
            # This is the most complicated case, the deleted
            # node has both left and right children
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
            # Until here the node has been deleted and
            # the tree has been refactored
        else:
            return False

    """
    Access:
    - size (lst.size())
    - is member (lst.member(3))
    - reverse (lst.reverse() (if applicable)
    """

    def size(self) -> int:
        """
        Return the size of tree
        """
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
    def is_member(self, value: T1) -> bool:
        """
        Determine whether it is a member node of the tree
        """
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
    Conversion from/to built-in list (you should avoid
    # of usage these function into your library):
    - from_list (lst.from_list([12, 99, 37]))
    - to_list (lst.to_list())
    """

    def from_list(self, lst: List[Any]) -> 'BTree':
        """
        Conversion from/to built-in list
        """
        for index in range(len(lst)):
            self.add(lst[index])
        return self

    # consistent with size function idea
    def to_list(self) -> List[Any]:
        """
        Convert tree to list
        """
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
    Filter data structure by specific predicate
    """

    def filter(self) -> List[Any]:
        """
        Filter data structure by specific predicate
        """
        lst = self.to_list()
        new_lst = []
        for i in range(len(lst)):
            if type(lst[i]) == int:
                new_lst.append(lst[i])
        return new_lst

    """
    Map structure by specific function
    """

    """
    Q: Can it be a source of undefined behavior?
    If yes — give an example and fix it, if not — proof it.
    """

    """
    A: From 6.15 of python documentation
        Python evaluates expressions from left to right.
        Notice that while evaluating an assignment, the right-hand
        side is evaluated before the left-hand side.

        So here the functions will be called in order from left to right.
        So any of the changes you will see will be due to the functions
        called from left to right.
    """

    def map(self, f: Callable[..., Any]) -> Any:
        """
        Build a map data structure for the tree
        """
        if self.root is None:
            return None
        queue = list()
        queue.append(self.root)
        while len(queue):
            tmp = queue.pop(0)
            # It's an undefined behavior here, if it happened in c or c++,
            # different compilers will be very different.
            val = Value()  # type: ignore
            val.set_value(tmp.value)

            def h(x: int) -> int:
                x += 1
                val.set_value(x)
                return x

            def g(x: int) -> int:
                x *= 2
                val.set_value(x)
                return x

            # A detailed description is proved in mutable_test.py
            tmp.value = f(val.get_vlaue())
            if tmp.left is not None:
                queue.append(tmp.left)
            if tmp.right is not None:
                queue.append(tmp.right)
        return self

    """
    Reduce–process structure elements to
    build a return value by specific functions
    """

    def reduce(self, f: Callable[..., Any], initial_state: int = 0) -> int:
        """
        Reduce–process structure elements
        """
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

    def __iter__(self) -> Iterator[Any]:
        """
        Return a iterator
        """
        if self.root is None:
            self.deep = 0
            return self
        self.iter_queue.append(self.root)
        self.deep += 1
        return self

    """
    An iterator object implements __next__,
    which is expected to return the next element of the
    iterable object that returned it,
    and to raise a StopIteration exception
    when no more elements are available.
    """

    def __next__(self) -> Any:
        """
        Return the next element of BTree or StopIteration
        """
        # signals "the end"
        if self.deep == 0:
            raise StopIteration
        # Add left and right subtrees to the queue
        if self.root.left is not None:
            self.iter_queue.append(self.root.left)
        if self.root.right is not None:
            self.iter_queue.append(self.root.right)
        nxt = self.iter_queue[self.deep - 1].value

        if self.deep < len(self.iter_queue):
            self.root = self.iter_queue[self.deep]
            self.deep += 1
        else:
            # iterator the last element
            self.root = self.iter_queue[0]
            self.deep = 0
        return nxt

    """
    Data structure should be a monoid and
    implement empty and concat methods
    """

    def empty(self) -> None:
        """
        Return a empty node
        """
        return None

    # According to my understanding, what this function
    # should return is the sum of two bt trees
    def concat(self, bt1: Any, bt2: Any) -> Any:
        """
        Sum of two bt trees
        """
        if not bt1:
            return bt2
        if not bt2:
            return bt1
        # return the new BTree
        new_root = BTNode(bt1.value + bt2.value)  # type: BTNode
        new_root.left = self.concat(bt1.left, bt2.left)
        new_root.right = self.concat(bt1.right, bt2.right)
        return new_root
