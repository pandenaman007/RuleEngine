# backend/node.py

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Left child (for operators)
        self.right = right  # Right child (for operators)
        self.value = value  # Condition (for operands)

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"
