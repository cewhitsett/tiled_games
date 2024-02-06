"""
Implementations of various types of queues
"""

from typing import Any, Optional, Union

from src.tiled_tools.common.custom_typing import AnyNumber


class AbstractQueue:
    """
    An abstract queue class that defines the interface for all queue implementations
    """

    def __init__(self, starting_items: Optional[list] = None):
        self.queue = []

        if starting_items is not None:
            for item in starting_items:
                self.push(item)

    def push(self, item):
        """
        Adds an item to the queue
        """
        raise NotImplementedError

    def pop(self):
        """Removes and returns the first item in the queue"""
        raise NotImplementedError

    def peek(self):
        """Returns the first item in the queue without removing it"""
        raise NotImplementedError

    def is_empty(self):
        """Returns True if the queue is empty"""
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.queue})"

    def __str__(self) -> str:
        return self.__repr__()


class Queue(AbstractQueue):
    """
    A basic queue implementation
    """

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop(0)

    def peek(self):
        return self.queue[0]


class Stack(AbstractQueue):
    """
    A basic stack implementation
    """

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop(-1)

    def peek(self):
        return self.queue[-1]


class PriorityWrapper:
    """
    A simple class that stores an item with its priority
    and helps with comparison. The higher the priority,
    the earlier the item will be popped from the queue
    """

    def __init__(self, item: Any, priority: AnyNumber):
        self.item = item
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority and self.item == other.item

    def __gt__(self, other):
        return self.priority > other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __ne__(self, other):
        return self.priority != other.priority

    def __repr__(self) -> str:
        return str(self.item)


class PriorityQueue(AbstractQueue):
    """
    A priority queue
    """

    def push(self, item: Union[PriorityWrapper, tuple, Any]):
        """
        Args:
            item (Union[PriorityWrapper,tuple]): The item to add to the queue. If a tuple is provided, it will be
            converted to a PriorityWrapper with the second element as the priority.

        """
        if isinstance(item, PriorityWrapper):
            self.queue.append(item)
        elif isinstance(item, tuple):
            self.queue.append(PriorityWrapper(item[0], item[1]))
        else:
            self.queue.append(PriorityWrapper(item, 0))

        self.queue.sort()

    def pop(self):
        return self.queue.pop(-1).item

    def peek(self):
        return self.queue[-1].item
