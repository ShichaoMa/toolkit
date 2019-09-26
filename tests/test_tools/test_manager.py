import time

from toolkit.tools.managers import Blocker


def test_blocker():
    start_time = time.time()
    assert Blocker(3).wait_timeout_or_notify(lambda: time.time() - start_time > 2)
    assert not Blocker(3).wait_timeout_or_notify(lambda: time.time() - start_time > 10)