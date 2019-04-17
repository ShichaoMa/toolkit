import time
import unittest
from toolkit.tools.managers import Timer


class TimerTest(unittest.TestCase):

    def test_timer(self):
        with Timer() as timer:
            time.sleep(3)

        self.assertTrue(timer.cost > 3)
