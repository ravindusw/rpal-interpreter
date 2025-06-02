class Node:
    """
    A class representing a node in the abstract syntax tree
    Each node contains a value and a left and right children.
    """

    def __init__(self, value, left, right):
        """
        Initialize a new node.

        Attributes:
            value (str): The value of the node.
            right (Node): The right child
            left (Node): The left child
        """
        self.value = value
        self.right = right
        self.left = left

    def __repr__(self):
        return f"Node({self.value})"

    def __str__(self):
        return f"Node with value: {self.value}, Left: {self.left}, Right: {self.right}"
    

class Stack:
    """
    A simple stack implementation for managing nodes in the derivation tree.
    """

    def __init__(self):
        """
        Initialize an empty stack.
        """
        self.items = []

    def push(self, item):
        """
        Push an item onto the stack.

        Args:
            item (Node): The item to be pushed onto the stack.
        """
        self.items.append(item)

    def pop(self):
        """
        Pop an item from the stack.

        Returns:
            Node: The item popped from the stack.
        """
        return self.items.pop() if self.items else None

    def is_empty(self):
        """
        Check if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self.items) == 0
    
    def peek(self):
        """
        Peek at the top item of the stack without removing it.

        Returns:
            Node: The top item of the stack.
        """
        return self.items[-1] if not self.is_empty() else None
    
    