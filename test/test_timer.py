# -*- coding:utf-8 -*-
import time
from toolkit.manager import Timer


def test_timer():
    with Timer() as timer:
        time.sleep(3)
        raise Exception("aa")

    print(timer.cost)


if __name__ == "__main__":
    test_timer()