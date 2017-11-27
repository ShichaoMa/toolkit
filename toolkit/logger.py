import os
import sys
import copy
import logging
import datetime

from functools import wraps
from logging import handlers
from pythonjsonlogger.jsonlogger import JsonFormatter

from . import _find_caller_name


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


class Logger(object):
    """
    logger的实现
    """
    logger = None

    def __new__(cls, *args, **kwargs):
        # 保证单例
        if not cls.logger:
            cls.logger = super(Logger, cls).__new__(cls)
        return cls.logger

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    @classmethod
    def init_logger(cls, settings, name=None):
        name = name or _find_caller_name()
        json = settings.get_bool('LOG_JSON', True)
        level = settings.get('LOG_LEVEL', 'DEBUG')
        stdout = settings.get_bool('LOG_STDOUT', True)
        dir = settings.get('LOG_DIR', 'logs')
        bytes = settings.get_int('LOG_MAX_BYTES', 10*1024*1024)
        backups = settings.get_int('LOG_BACKUPS', 5)
        logger = cls(name=name)
        logger.logger.propagate = False
        logger.json = json
        logger.name = name
        logger.format_string = '%(asctime)s [%(name)s]%(levelname)s: %(message)s'
        root = logging.getLogger()
        # 将的所有使用Logger模块生成的logger设置一样的logger level
        for log in root.manager.loggerDict.keys():
            root.getChild(log).setLevel(getattr(logging, level, 10))

        if stdout:
            logger.set_handler(logging.StreamHandler(sys.stdout))
        else:
            os.makedirs(dir, exist_ok=True)
            file_handler = handlers.RotatingFileHandler(
                os.path.join(dir, "%s.log"%name),
                maxBytes=bytes,
                backupCount=backups)
            logger.set_handler(file_handler)

        return logger

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
        return my_copy