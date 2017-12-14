import unittest
from redis import Redis
from toolkit.queues import FifoDiskQueue, RedisQueue


class FifoDiskQueueTest(unittest.TestCase):

    def setUp(self):
        self.queue = FifoDiskQueue("queue")

    def test_rid_3(self):
        self.queue.push(b"aaaaa")
        self.queue.push(b"bbbbb")
        self.queue.push(b"ccccc")
        self.assertListEqual([b"aaaaa", b"bbbbb", b"ccccc"], self.queue.rid(3))

    def test_rid_2(self):
        self.queue.push(b"aaaaa")
        self.queue.push(b"bbbbb")
        self.assertListEqual([b"aaaaa", b"bbbbb"], self.queue.rid(3))

    def test_rid_1(self):
        self.queue.push(b"aaaaa")
        self.queue.push(b"bbbbb")
        self.queue.push(b"ccccc")
        self.assertListEqual([b"aaaaa"], self.queue.rid(1))

    def tearDown(self):
        self.queue.clear()


class RedisQueueTest(unittest.TestCase):

    def setUp(self):
        self.queue = RedisQueue(Redis(), "test_queue")

    def test_rid_3(self):
        self.queue.push(b"aaaaa")
        self.queue.push(b"bbbbb")
        self.queue.push(b"ccccc")
        self.assertListEqual([b"aaaaa", b"bbbbb", b"ccccc"], self.queue.rid(3))

    def test_rid_2(self):
        self.queue.push(b"aaaaa")
        self.queue.push(b"bbbbb")
        self.assertListEqual([b"aaaaa", b"bbbbb"], self.queue.rid(3))

    def test_rid_1(self):
        self.queue.push(b"aaaaa")
        self.queue.push(b"bbbbb")
        self.queue.push(b"ccccc")
        self.assertListEqual([b"aaaaa"], self.queue.rid(1))

    def tearDown(self):
        self.queue.clear()


if __name__ == "__main__":
    unittest.main()
