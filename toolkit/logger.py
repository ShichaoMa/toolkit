import os
import sys
import logging
import datetime

from functools import wraps
from logging import handlers
from threading import current_thread
from pythonjsonlogger.jsonlogger import JsonFormatter

from . import _find_caller_name
from .singleton import Singleton

__all__ = ["UDPLogstashHandler", "Logger"]


class UDPLogstashHandler(handlers.DatagramHandler):
    """Python logging handler for Logstash. Sends events over UDP."""
    def makePickle(self, record):
        return self.formatter.format(record).encode()


class Logger(object, metaclass=Singleton):
    """
    logger的实现
    """
    format_string = '%(asctime)s [%(name)s:%(threadname)s]%(level)s: %(message)s'

    def __init__(self, settings, name=None):
        self.name = name or _find_caller_name(steps=2)
        self.json = settings.get_bool('LOG_JSON', True)
        self.level = settings.get('LOG_LEVEL', 'DEBUG')
        self.stdout = settings.get_bool('LOG_STDOUT', True)
        self.dir = settings.get('LOG_DIR', 'logs')
        self.bytes = settings.get('LOG_MAX_BYTES', 10*1024*1024)
        self.backups = settings.get_int('LOG_BACKUPS', 5)
        self.udp_host = settings.get("LOG_UDP_HOST", "127.0.0.1")
        self.udp_port = settings.get_int("LOG_UDP_PORT", 5230)
        self.log_file = settings.get_bool('LOG_FILE', False)
        self.logger = logging.getLogger(self.name)
        self.logger.propagate = False
        self.set_up()

    def set_up(self):
        root = logging.getLogger()
        # 将的所有使用Logger模块生成的logger设置一样的logger level
        for log in root.manager.loggerDict.keys():
            root.getChild(log).setLevel(getattr(logging, self.level, 10))

        if self.stdout:
            self.set_handler(logging.StreamHandler(sys.stdout))
        elif self.log_file:
            os.makedirs(dir, exist_ok=True)
            file_handler = handlers.RotatingFileHandler(
                os.path.join(dir, "%s.log" % self.name),
                maxBytes=bytes,
                backupCount=self.backups)
            self.set_handler(file_handler)
        else:
            self.set_handler(UDPLogstashHandler(self.udp_host, self.udp_port))

    def set_handler(self, handler):
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self._get_formatter())
        self.logger.addHandler(handler)
        self.debug("Logging to %s" % handler.__class__.__name__)

    def __getattr__(self, item):
        if item.upper() in logging._nameToLevel:
            func = getattr(self.logger, item)

            @wraps(func)
            def wrapper(*args, **kwargs):
                extra = kwargs.pop("extra", {})
                extra.setdefault("level", item)
                extra.setdefault("timestamp",
                                 datetime.datetime.utcnow().strftime(
                                     '%Y-%m-%dT%H:%M:%S.%fZ'))
                extra.setdefault("logger", self.name)
                extra.setdefault("threadname", current_thread().getName())
                kwargs["extra"] = extra
                return func(*args, **kwargs)
            return wrapper

        raise AttributeError

    def _get_formatter(self):
        if self.json:
            return JsonFormatter()
        else:
            return logging.Formatter(self.format_string)
