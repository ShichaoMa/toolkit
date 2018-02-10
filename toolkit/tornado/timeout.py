import numbers


class Timeout(object):

    __slots__ = ['deadline', 'callback', 'tdeadline']

    def __init__(self, deadline, callback, io_loop):
        if not isinstance(deadline, numbers.Real):
            raise TypeError("Unsupported deadline %r" % deadline)
        self.deadline = deadline
        self.callback = callback
        self.tdeadline = (deadline, next(io_loop._timeout_counter))

    def __lt__(self, other):
        return self.tdeadline < other.tdeadline

    def __le__(self, other):
        return self.tdeadline <= other.tdeadline