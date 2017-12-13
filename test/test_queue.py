import unittest
from toolkit.queues import FifoDiskQueue


class FifoDiskQueueTest(unittest.TestCase):

    def setUp(self):
        self.queue = FifoDiskQueue("queue")

    def test_rid(self):
        self.queue.push(b"aaaaa")
        self.queue.push(b"bbbbb")
        self.assertListEqual([b"aaaaa", b"bbbbb"], self.queue.rid(2))


if __name__ == "__main__":
    unittest.main()
