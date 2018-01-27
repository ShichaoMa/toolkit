import os
import sys
import copy
import logging
import datetime
import warnings

from functools import wraps
from logging import handlers
from threading import current_thread
from pythonjsonlogger.jsonlogger import JsonFormatter

from . import _find_caller_name
from .singleton import Singleton

__all__ = ["UDPLogstashHandler", "Logger"]


def extras_wrapper(self, item):
    """
    logger的extra转用装饰器
    :param self:
    :param item:
    :return:
    """
    def logger_func_wrapper(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) > 2:
                extras = args[1]
            else:
                extras = kwargs.pop("extras", {})
            extras = self.add_extras(extras, item)
            return func(args[0], extra=extras)

        return wrapper

    return logger_func_wrapper


class UDPLogstashHandler(handlers.DatagramHandler):
    """Python logging handler for Logstash. Sends events over UDP.
    :param host: The host of the logstash server.
    :param port: The port of the logstash server (default 5959).
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def makePickle(self, record):
        return self.formatter.format(record).encode("utf-8")


class Logger(object, metaclass=Singleton):
    """
    logger的实现
    """
    format_string = '%(asctime)s [%(name)s:%(threadname)s]%(levelname)s: %(message)s'

    def __init__(self, settings, name=None):
        self.name = name or _find_caller_name(steps=2)
        self.json = settings.get_bool('LOG_JSON', True)
        self.level = settings.get('LOG_LEVEL', 'DEBUG')
        self.stdout = settings.get_bool('LOG_STDOUT', True)
        self.dir = settings.get('LOG_DIR', 'logs')
        self.bytes = settings.get('LOG_MAX_BYTES', '10MB')
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
        formatter = self._get_formatter(self.json)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.debug("Logging to %s"%handler.__class__.__name__)

    def __getattr__(self, item):
        if item.upper() in logging._nameToLevel:
            return extras_wrapper(self, item)(getattr(self.logger, item))
        raise AttributeError

    def _get_formatter(self, json):
        if json:
            return JsonFormatter()
        else:
            return logging.Formatter(self.format_string)

    def add_extras(self, dict, level):
        my_copy = copy.deepcopy(dict)
        if 'level' not in my_copy:
            my_copy['level'] = level
        if 'timestamp' not in my_copy:
            my_copy['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if 'logger' not in my_copy:
            my_copy['logger'] = self.name
        my_copy["threadname"] = current_thread().getName()
        return my_copy

    @classmethod
    def init_logger(cls, name, settings):
        warnings.warn("init_logger is a deprecated alias, use Logger() instead.", DeprecationWarning, 2)
        return cls(name, settings)
