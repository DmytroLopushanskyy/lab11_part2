"""
File: node.py

Node classes for one-way linked structures and two-way
linked structures.
"""


class Node:
    """
    Represents a Node in a linked structure
    """
    def __init__(self, data, next_el=None):
        """
        Instantiates a Node with default next of None
        :param data: int
        :param next_el: Node
        """
        self.data = data
        self.next_el = next_el


class TwoWayNode(Node):
    """
    Represents a Node in a linked structure
    """
    def __init__(self, data, previous=None, next_el=None):
        """
        Instantiates a Node with default next and previous of None
        :param data: int
        :param previous: TwoWayNode
        :param next_el: TwoWayNode
        """
        Node.__init__(self, data, next_el)
        self.previous = previous

    def __str__(self):
        """
        String representation of TwoWayNode.
        :return: str
        """
        return str(self.data)
