import os
import sys
import signal
import random
import logging
import traceback

from redis import Redis
from itertools import repeat
from argparse import ArgumentParser
from kafka import KafkaConsumer, KafkaProducer

from . import call_later
from .logger import Logger
from .managers import ExceptContext
from .settings import SettingsWrapper
from .daemon_ctl import common_stop_start_control

__all__ = ["ParallelMonitor", "LoggingMonitor"]


class ParallelMonitor(object):
    """
    支持多线程多进程统一管理
    """
    alive = True
    name = "parallel_monitor"
    children = []
    int_signal_count = 1

    def __init__(self):
        super(ParallelMonitor, self).__init__()
        self.open()

    def set_logger(self, logger=None):
        if not logger:
            self.logger = logging.getLogger(self.name)
            self.logger.setLevel(10)
            self.logger.addHandler(logging.StreamHandler(sys.stdout))
        else:
            self.logger = logger
            self.name = logger.name

    def stop(self, *args):
        if self.int_signal_count > 1:
            self.logger.info("force to terminate...")
            for th in self.children[:]:
                self.stop_child(th)
            pid = os.getpid()
            os.kill(pid, 9)

        else:
            self.alive = False
            self.logger.info("close process %s..." % self.name)
            self.int_signal_count += 1

    def open(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop_child(self, child):
        pass


class LoggingMonitor(object):
    """
    内建Logger和Settings的ParallelMonitor
    """
    name = "logging_monitor"
    wrapper = SettingsWrapper()
    _logger = None

    def __init__(self, settings, localsettings=None):
        super(LoggingMonitor, self).__init__()
        if isinstance(settings, dict):
            self.settings = settings
        else:
            self.settings = self.wrapper.load(local=localsettings, default=settings)

    def set_logger(self, logger=None):
        self._logger = logger

    @property
    def logger(self):
        if not self._logger:
            self._logger = Logger.init_logger(self.settings, self.name)
        return self._logger

    def log_err(self, func_name, *args):
        self.logger.error("Error in %s: %s. "%(func_name, "".join(traceback.format_exception(*args))))
        return True


class Service(LoggingMonitor, ParallelMonitor):
    """
        可执行程序，支持守护进程启动
    """
    name = "Service"
    parser = None

    def __init__(self):
        self.args = self.parse_args()
        super(Service, self).__init__(self.args.settings, self.args.localsettings)

    def enrich_parser_arguments(self):
        self.parser.add_argument("-d", "--daemon", help="Run backend. ")
        self.parser.add_argument("-s", "--settings", help="Setting module. ", default="settings")
        self.parser.add_argument("-ls", "--localsettings", help="Local setting module. ", default="localsettings")

    def parse_args(self, daemon_log_path='/dev/null'):
        self.parser = ArgumentParser(conflict_handler="resolve")
        self.enrich_parser_arguments()
        return common_stop_start_control(self.parser, daemon_log_path, 2)


class ProxyPool(LoggingMonitor):
    """
        Redis代理池
    """
    def __init__(self, settings):
        """
        proxy_sets指定多个redis set,随机选取proxy
        proxy
        :param settings:
        """
        super(ProxyPool, self).__init__(settings)
        self.protocols = self.settings.get("PROTOCOLS", "http,https").split(",")
        self.redis_conn = Redis(self.settings.get("REDIS_HOST"), self.settings.get_int("REDIS_PORT", 6379))
        self.proxy_sets = self.settings.get("PROXY_SETS", "proxy_set").split(",")
        self.account_password = self.settings.get("PROXY_ACCOUNT_PASSWORD")
        self.proxy = {}

    def proxy_choice(self):
        """
        顺序循环选取代理
        :return: 代理
        """
        proxy = self.redis_conn.srandmember(random.choice(self.proxy_sets))
        if proxy:
            proxy_str = "http://%s%s"%(self.account_password+"@"if self.account_password else "", proxy.decode())
            self.proxy = dict(zip(self.protocols, repeat(proxy_str)))
        return self.proxy


class ItemConsumer(Service):
    """
    kafka consumer.
    """
    name = "item_consumer"

    def __init__(self):
        super(ItemConsumer, self).__init__()
        self.topic_in = self.args.topic_in
        self.consumer_id = self.args.consumer or self.name
        with ExceptContext(Exception, errback=lambda *args: self.stop()):
            self.consumer = KafkaConsumer(self.topic_in,
                                          group_id=self.consumer_id,
                                          bootstrap_servers=self.settings.get("KAFKA_HOSTS").split(","),
                                          enable_auto_commit=False,
                                          consumer_timeout_ms=1000)

    def consume_errback(self, exception):
        self.logger.error("Consume feature failed: %s. " % str(exception))

    def consume_callback(self, value):
        self.logger.debug("Consume feature success: %s. " % str(value))

    @call_later("commit", interval=10, immediately=False)
    def consume(self, callback=lambda value: value, errback=lambda message: message):
        with ExceptContext(errback=self.log_err):
            with ExceptContext((StopIteration, OSError), errback=lambda *args: True):
                message = self.consumer.__next__()
                while message:
                    value = message.value
                    self.logger.debug('Consume message from %s, message is %s' % (self.topic_in, value))
                    if isinstance(value, bytes):
                        value = value.decode("utf-8")
                    value = callback(value)
                    if value:
                        return value
                    else:
                        message = errback(message)

    def commit(self):
        future = self.consumer.commit_async()
        future.add_callback(self.consume_callback)
        future.add_errback(self.consume_errback)

    def enrich_parser_arguments(self):
        super(ItemConsumer, self).enrich_parser_arguments()
        self.parser.add_argument("-ti", "--topic-in", help="Topic in. ")
        self.parser.add_argument("-c", "--consumer", help="consumer id. ")

    def stop(self, *args):
        super(ItemConsumer, self).stop(args)
        with ExceptContext(Exception, errback=lambda *args: True):
            if self.consumer:
                self.consumer.close()


class ItemProducer(Service):
    """
    kafka producer.
    """
    name = "item_producer"

    def __init__(self):
        super(ItemProducer, self).__init__()
        self.topic_out = self.args.topic_out
        with ExceptContext(Exception, errback=lambda *args: self.stop()):
            self.producer = KafkaProducer(bootstrap_servers=self.settings['KAFKA_HOSTS'].split(","), retries=3)

    def produce_callback(self, value):
        self.logger.debug("Product future success: %s"%value)

    def produce_errback(self, value):
        self.logger.debug("Product future failed: %s" % value)

    def produce(self, *messages):
        with ExceptContext(Exception, errback=self.log_err):
            for message in messages:
                if isinstance(message, str):
                    message = message.encode("utf-8")
                future = self.producer.send(self.topic_out, message)
                future.add_callback(self.produce_callback)
                future.add_errback(self.produce_errback)
                future.get(timeout=50)

    def enrich_parser_arguments(self):
        super(ItemProducer, self).enrich_parser_arguments()
        self.parser.add_argument("-to", "--topic-out", help="Topic out. ")

    def stop(self, *args):
        super(ItemProducer, self).stop(args)
