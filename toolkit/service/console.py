# -*- coding:utf-8 -*-
import sys
import time

from socket import socket
from threading import Thread, local
from code import InteractiveInterpreter


__all__ = ["CustomInteractiveInterpreter", "_local"]
_local = local()
_displayhook = sys.displayhook


class StringO(object):
    """
    替代标准输出
    """
    def __init__(self):
        self._buffer = []

    def isatty(self):
        return False

    def close(self):
        pass

    def flush(self):
        pass

    def seek(self, n, mode=0):
        pass

    def readline(self):
        if len(self._buffer) == 0:
            return ''
        ret = self._buffer[0]
        del self._buffer[0]
        return ret

    def reset(self):
        val = ''.join(self._buffer)
        del self._buffer[:]
        return val

    def _write(self, x):
        if isinstance(x, bytes):
            x = x.decode('utf-8', 'replace')
        self._buffer.append(str(x))

    def write(self, x):
        self._write(x)

    def writelines(self, x):
        self._write(''.join(x))


class ThreadedStream(object):

    """Thread-local wrapper for sys.stdout for the interactive console."""

    def push():
        if not isinstance(sys.stdout, ThreadedStream):
            sys.stdout = ThreadedStream()
        _local.stream = StringO()
    push = staticmethod(push)

    def fetch():
        try:
            stream = _local.stream
        except AttributeError:
            return ''
        return stream.reset()
    fetch = staticmethod(fetch)

    def displayhook(obj):
        try:
            stream = _local.stream
        except AttributeError:
            return _displayhook(obj)
        # stream._write bypasses escaping as debug_repr is
        # already generating HTML for us.
        if obj is not None:
            _local._current_ipy.locals['_'] = obj
            stream._write(obj)
    displayhook = staticmethod(displayhook)

    def __setattr__(self, name, value):
        raise AttributeError('read only attribute %s' % name)

    def __dir__(self):
        return dir(sys.__stdout__)

    def __getattribute__(self, name):
        if name == '__members__':
            return dir(sys.__stdout__)
        try:
            stream = _local.stream
        except AttributeError:
            stream = sys.__stdout__
        return getattr(stream, name)

    def __repr__(self):
        return repr(sys.__stdout__)


sys.displayhook = ThreadedStream.displayhook


class CustomInteractiveInterpreter(InteractiveInterpreter):

    def __init__(self, locals):
        super(CustomInteractiveInterpreter, self).__init__(locals)
        self.buffer = []
        self.stdout = sys.stdout
        self.more = False

    def runsource(self, source):
        source = source.rstrip() + '\n'
        try:
            ThreadedStream.push()
            source_to_eval = ''.join(self.buffer + [source])
            result = super(
                CustomInteractiveInterpreter, self).runsource(source_to_eval)
            if (self.more or result) and source != "\n":
                self.buffer.append(source)
                self.more = True
            else:
                del self.buffer[:]
                self.more = False
        finally:
            output = ThreadedStream.fetch()
            sys.stdout = self.stdout
        prompt = self.more and '... ' or '>>> '
        return prompt + output

    def write(self, data):
        sys.stdout.write(data)