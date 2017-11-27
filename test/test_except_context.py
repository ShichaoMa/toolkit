from ..toolkit.manager import ExceptContext


def test_ExceptContext():
    with ExceptContext(Exception, errback=lambda name, *args:print(name)):
        raise Exception("test. ..")


if __name__ == "__main__":
    test_ExceptContext()