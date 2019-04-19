import pytest

from toolkit.tools.managers import ExceptContext


def test_raise():
    with pytest.raises(Exception):
        with ExceptContext(Exception, errback=lambda name, *args: print(name)):
            raise Exception("test. ..")


def test_no_raise():
    with ExceptContext(Exception, errback=lambda name, *args: print(name) is None):
        raise Exception("test. ..")
