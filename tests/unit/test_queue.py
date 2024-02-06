# pylint: disable=missing-docstring,line-too-long

import unittest

from src.tiled_tools.common.queues import PriorityQueue, PriorityWrapper, Queue, Stack


class TestQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = Queue()

    def test_push(self):
        self.queue.push(1)
        self.assertEqual(len(self.queue), 1)

        for i in range(10):
            self.queue.push(i)

        self.assertEqual(len(self.queue), 11)

    def test_pop(self):
        self.queue.push(1)
        self.queue.push(3)
        self.queue.push(2)

        self.assertEqual(self.queue.pop(), 1)
        self.assertEqual(self.queue.pop(), 3)
        self.assertEqual(self.queue.pop(), 2)

    def test_peek(self):
        self.queue.push(1)
        self.assertEqual(self.queue.peek(), 1)
        self.queue.push(3)
        self.queue.push(2)

        self.assertEqual(self.queue.peek(), 1)
        self.queue.pop()
        self.assertEqual(self.queue.peek(), 3)
        self.queue.pop()
        self.assertEqual(self.queue.peek(), 2)


class TestStack(unittest.TestCase):
    def setUp(self) -> None:
        self.stack = Stack()

    def test_push(self):
        self.stack.push(1)
        self.assertEqual(len(self.stack), 1)

        for i in range(10):
            self.stack.push(i)

        self.assertEqual(len(self.stack), 11)

    def test_pop(self):
        self.stack.push(1)
        self.stack.push(3)
        self.stack.push(2)

        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 1)

    def test_peek(self):
        self.stack.push(1)
        self.assertEqual(self.stack.peek(), 1)
        self.stack.push(3)
        self.stack.push(2)

        self.assertEqual(self.stack.peek(), 2)
        self.stack.pop()
        self.assertEqual(self.stack.peek(), 3)
        self.stack.pop()
        self.assertEqual(self.stack.peek(), 1)


class TestPriorityQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.priority_queue = PriorityQueue()

    def test_push(self):
        self.priority_queue.push(1)
        self.assertEqual(len(self.priority_queue), 1)

        for i in range(10):
            self.priority_queue.push(i)

        for i in range(10):
            self.priority_queue.push((i, i))

        for i in range(10):
            self.priority_queue.push(PriorityWrapper(i, i))

        self.assertEqual(len(self.priority_queue), 31)

    def test_pop_like_stack(self):
        self.priority_queue.push(1)
        self.priority_queue.push(3)
        self.priority_queue.push(2)

        self.assertEqual(self.priority_queue.pop(), 2)
        self.assertEqual(self.priority_queue.pop(), 3)
        self.assertEqual(self.priority_queue.pop(), 1)

    def test_peek_like_stack(self):
        self.priority_queue.push(1)
        self.assertEqual(self.priority_queue.peek(), 1)
        self.priority_queue.push(3)
        self.priority_queue.push(2)

        self.assertEqual(self.priority_queue.peek(), 2)
        self.priority_queue.pop()
        self.assertEqual(self.priority_queue.peek(), 3)
        self.priority_queue.pop()
        self.assertEqual(self.priority_queue.peek(), 1)

    def test_priority_wrapper(self):
        self.priority_queue.push(PriorityWrapper(1, 2))
        self.priority_queue.push(PriorityWrapper(3, 1))
        self.priority_queue.push(PriorityWrapper(2, 3))

        self.assertEqual(self.priority_queue.pop(), 2)
        self.assertEqual(self.priority_queue.pop(), 1)
        self.assertEqual(self.priority_queue.pop(), 3)
