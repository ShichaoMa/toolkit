# -*- coding:utf-8 -*-
import os
import re
import sys
import copy
import time
import json
import types
import socket
import psutil
import signal
import logging
import datetime
import importlib

from queue import Empty
from logging import handlers
from functools import wraps, reduce
from pythonjsonlogger.jsonlogger import JsonFormatter


def duplicate(iterable, key=lambda x: x):
    """
    保序去重
    :param iterable:
    :param key:
    :return:
    """
    result = list()
    for i in iterable:
        keep = key(i)
        if keep not in result:
            result.append(keep)
    return result


def strip(value, chars=None):
    """
    strip字段
    :param value:
    :param chars:
    :return:
    """
    if isinstance(value, str):
        return value.strip(chars)
    return value


def decode(value, encoding="utf-8"):
    """
    decode字段
    :param value:
    :param encoding:
    :return:
    """
    return value.decode(encoding)


def encode(value, encoding="utf-8"):
    """
    encode字段
    :param value:
    :param encoding:
    :return:
    """
    return value.encode(encoding)


def rid(value, old, new):
    """
    去掉指定字段
    :param value:
    :param old:
    :param new:
    :return:
    """
    return value.replace(old, new)


def wrap_key(json_str, key_pattern=re.compile(r"([a-zA-Z_]\w*)[\s]*\:")):
    """
    将javascript 对象字串串形式的key转换成被双字符包裹的格式如{a: 1} => {"a": 1}
    :param json_str:
    :param key_pattern:
    :return:
    """
    json_str = key_pattern.sub('"\g<1>":', json_str)
    return json_str


def safely_json_loads(json_str, defaulttype=dict, escape=True):
    """
    返回安全的json类型
    :param json_str: 要被loads的字符串
    :param defaulttype: 若load失败希望得到的对象类型
    :param escape: 是否将单引号变成双引号
    :return:
    """
    if not json_str:
        return defaulttype()
    elif escape:
        data = replace_quote(json_str)
        return json.loads(data)
    else:
        return json.loads(json_str)


def chain_all(iter):
    """
    连接两个序列或字典
    :param iter:
    :return:
    """
    iter = list(iter)
    if not iter:
        return []
    if isinstance(iter[0], dict):
        result = {}
        for i in iter:
            result.update(i)
    else:
        result = reduce(lambda x, y: list(x)+list(y), iter)
    return result


def replace_quote(json_str):
    """
    将要被json.loads的字符串的单引号转换成双引号，如果该单引号是元素主体，而不是用来修饰字符串的。则不对其进行操作。
    :param json_str:
    :return:
    """
    if not isinstance(json_str, str):
        return json_str
    double_quote = []
    new_lst = []
    for index, val in enumerate(json_str):
        if val == '"' and json_str[index-1] != "\\":
            if double_quote:
                double_quote.pop(0)
            else:
                double_quote.append(val)
        if val== "'" and json_str[index-1] != "\\":
            if not double_quote:
                val = '"'
        new_lst.append(val)
    return "".join(new_lst)


def format_html_string(html):
    """
    格式化html
    :param html:
    :return:
    """
    trims = [(r'\n',''),
             (r'\t', ''),
             (r'\r', ''),
             (r'  ', ''),
             (r'\u2018', "'"),
             (r'\u2019', "'"),
             (r'\ufeff', ''),
             (r'\u2022', ":"),
             (r"<([a-z][a-z0-9]*)\ [^>]*>", '<\g<1>>'),
             (r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', ''),
             (r"</?a.*?>", '')]
    return reduce(lambda string, replacement: re.sub(replacement[0], replacement[1], html), trims, html)


def urldecode(query):
    """
    与urlencode相反，不过没有unquote
    :param query:
    :return:
    """
    if not query.strip():
        return dict()
    return dict(x.split("=") for x in query.strip().split("&"))


def re_search(re_str, text, dotall=True):
    """
    抽取正则规则的第一组元素
    :param re_str:
    :param text:
    :param dotall:
    :return:
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    if not isinstance(re_str, list):
        re_str = [re_str]

    for rex in re_str:
        if isinstance(rex, str):
            rex = re.compile(rex)
        if dotall:
            match_obj = rex.search(text, re.DOTALL)
        else:
            match_obj = rex.search(text)

        if match_obj is not None:
            t = match_obj.group(1).replace('\n', '')
            return t

    return ""


def retry_wrapper(retry_times, exception=Exception, error_handler=None, interval=0.1):
    """
    函数重试装饰器
    :param retry_times: 重试次数
    :param exception: 需要重试的异常
    :param error_handler: 出错时的回调函数
    :param interval: 重试间隔时间
    :return:
    """
    def out_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    count += 1
                    if error_handler:
                        result = error_handler(func.__name__, count, e, *args, **kwargs)
                        if result:
                            count -= 1
                    if count >= retry_times:
                        raise
                    time.sleep(interval)
        return wrapper

    return out_wrapper


def timeout(timeout_time, default):
    """
    Decorate a method so it is required to execute in a given time period,
    or return a default value.
    :param timeout_time:
    :param default:
    :return:
    """
    class DecoratorTimeout(Exception):
        pass

    def timeout_function(f):
        def f2(*args):
            def timeout_handler(signum, frame):
                raise DecoratorTimeout()

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            # triger alarm in timeout_time seconds
            signal.alarm(timeout_time)
            try:
                retval = f(*args)
            except DecoratorTimeout:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler)
            signal.alarm(0)
            return retval

        return f2

    return timeout_function


def custom_re(regex, text):
    """
    模仿selector.re
    :param regex:
    :param text:
    :return:
    """
    return re.findall(regex, text)


def replace_dot(data):
    """
    mongodb不支持key中带有.，该函数用来将.转换成_
    :param data:
    :return:
    """
    new_data = {}
    for k, v in data.items():
        new_data[k.replace(".", "_")] = v

    return new_data


def groupby(it, key):
    """
    自实现groupby，itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    :return: 字典对象
    """
    groups = dict()
    for item in it:
        groups.setdefault(key(item), []).append(item)
    return groups


def parse_cookie(string):
    """
    解析cookie
    :param string:
    :return:
    """
    results = re.findall('([^=]+)=([^\;]+);?\s?', string)
    my_dict = {}

    for item in results:
        my_dict[item[0]] = item[1]

    return my_dict


def async_produce_wrapper(producer, logger, batch_size=10):
    """
    pykafka实现异步生产时，使用的装饰器
    `
    self.producer.produce = async_produce_wrapper(self.producer, self.logger)(self.producer.produce)
    `
    :param producer:
    :param logger:
    :param batch_size:
    :return:
    """
    count = 0

    def wrapper(func):

        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            nonlocal count
            count += 1
            if count % batch_size == 0:  # adjust this or bring lots of RAM ;)
                while True:
                    try:
                        msg, exc = producer.get_delivery_report(block=False)
                        if exc is not None:
                            logger.error('Failed to deliver msg {}: {}'.format(
                                msg.partition_key, repr(exc)))
                        else:
                            logger.info('Successfully delivered msg {}'.format(
                                msg.partition_key))
                    except Empty:
                        break
            return result
        return inner
    return wrapper


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


def free_port():
    """
    Determines a free port using sockets.
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port


def _catch(li, index, default):
    try:
        return li[index]
    except IndexError:
        return default


def zip(*args, default=""):
    """
    enhance zip function
    :param args: ["a", "b", "c"], [1, 2]
    :param default: ""
    :return: [("a", 1), ("b", 2), ("c", "")]
    """
    max_length = max(map(lambda x: len(x), args))
    new_list = list()
    for i in range(max_length):
        new_ele = [_catch(li, i, default=default) for li in args]
        new_list.append(new_ele)
    return new_list


def thread_safe(lock):
    """
    对指定函数进行线程安全包装，需要提供锁
    :param lock: 锁
    :return:
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                lock.acquire()
                return func(*args, **kwargs)
            finally:
                lock.release()
        return wrapper
    return decorate


def call_later(callback, call_args=tuple(), immediately=True, interval=1):
    """
    应用场景：
    被装饰的方法需要大量调用，随后需要调用保存方法，但是因为被装饰的方法访问量很高，而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后，再调用保存方法。规定间隔内，无论调用多少次被装饰方法，保存方法只会
    调用一次，除非immediately=True
    :param callback: 随后需要调用的方法名
    :param call_args: 随后需要调用的方法所需要的参数
    :param immediately: 是否立即调用
    :param interval: 调用间隔
    :return:
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return func(*args, **kwargs)
            finally:
                if immediately:
                    getattr(self, callback)(*call_args)
                else:
                    now = time.time()
                    if now - self.__dict__.get("last_call_time", 0) > interval:
                        getattr(self, callback)(*call_args)
                        self.__dict__["last_call_time"] = now
        return wrapper
    return decorate


def thread_safe_for_method_in_class(func):
    """
    对类中的方法进行线程安全包装
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            self.lock.acquire()
            return func(*args, **kwargs)
        finally:
            self.lock.release()
    return wrapper


def daemonise(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 从母体环境脱离
    os.chdir("/")  # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符
    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())  # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


@timeout(5, "n")
def _t_raw_input(alive_pid):
    """重复启动时提示是否重启，5秒钟后超时返回n"""
    raw_input = globals().get("raw_input") or input
    return raw_input("The process with pid %s is running, restart it? y/n: " % alive_pid)


def common_stop_start_control(parser, monitor_log_path, wait=2):
    """
    开启关闭的公共实现
    :param parser: 一个argparse命令行参数解析对象，其它参数请调用些函数之前声明
    :param monitor_log_path: 如果通过--daemon 守护进程的方式启动，需要提供守护进程的stdout, stderr的文件路径
    :param wait: 轮循发起关闭信号的间隔时间
    :return: argparse的解析结果对象
    """
    parser.add_argument("-d", "--daemon", action="store_true", default=False)
    parser.add_argument("method", nargs="?", choices=["stop", "start", "restart", "status"])
    args = parser.parse_args()
    pid = os.getpid()
    filter_process_name = "%s .*%s"%(sys.argv[0], "start")
    if args.method == "stop":
        stop(filter_process_name, sys.argv[0], wait)
        sys.exit(0)
    if args.method == "status":
        alive_pid = _check_status(filter_process_name, [pid])
        prompt = ["PROCESS", "STATUS", "PID", "TIME"]
        status = [sys.argv[0].rstrip(".py"), "RUNNING" if alive_pid else "STOPPED",
                  str(alive_pid), time.strftime("%Y-%m-%d %H:%M:%S")]
        for line in format_line([prompt, status]):
            [print(i, end="") for i in line]
            print("")
        sys.exit(0)
    elif args.method == "restart":
        stop(filter_process_name, sys.argv[0], wait, ignore_pid=[pid])
        print("Start new process. ")
    else:
        alive_pid = _check_status(filter_process_name, ignore_pid=[pid])
        if alive_pid:
            result = _t_raw_input(alive_pid)
            if result.lower() in ["y", "yes"]:
                stop(filter_process_name, sys.argv[0], wait, ignore_pid=[pid])
            else:
                sys.exit(0)
    if args.daemon:
        daemonise(stdout=monitor_log_path, stderr=monitor_log_path)
    return args


def format_line(lines):
    if not lines:
        return [""]
    max_lengths = [0]*len(lines[0])
    for line in lines:
        for i, ele in enumerate(line):
            max_lengths[i] = max(len(ele), max_lengths[i])
    new_lines = []
    for line in lines:
        new_line = []
        for i, ele in enumerate(line):
            new_line.append(ele.ljust(max_lengths[i]+1))
        new_lines.append(new_line)
    return new_lines


def stop(name, default_name=None, timedelta=2, ignore_pid=[]):
    """
    关闭符合名字（regex)要求的进程
    :param name: regex用来找到相关进程
    :param default_name: 仅用做显示该进程的名字
    :param timedelta: 轮循发起关闭信号的间隔时间
    :param ignore_pid: 忽略关闭的进程号
    :return:
    """
    pid = _check_status(name, ignore_pid)
    if not pid:
        print("No such process named %s" % (default_name or name))
    while pid:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
        pid = _check_status(name, ignore_pid)
        if pid:
            print("Wait for %s exit. pid: %s" % (default_name or name, pid))
        time.sleep(timedelta)


def _check_status(name, ignore_pid):
    """
    找到主进程的pid
    :param name:
    :param ignore_pid:
    :return:
    """
    ignore = re.compile(r'ps -ef|grep')
    check_process = os.popen('ps -ef|grep "%s"' % name)
    processes = [x for x in check_process.readlines() if x.strip()]
    check_process.close()
    main_pid, main_ppid = None, None
    for process in processes:
        col = process.split()
        pid, ppid = col[1: 3]
        pid = int(pid) if int(pid) not in ignore_pid else None
        ppid = int(ppid)
        if not pid or ignore.search(process):
            continue
        main_pid, main_ppid = (pid, ppid) if not main_pid else ((pid, ppid) if main_ppid == pid else (main_pid, main_ppid))
    return main_pid and (int(main_pid) if int(main_pid) not in ignore_pid else None)


def get_ip():
    """
    获取局域网ip
    :return:
    """
    netcard_info = []
    info = psutil.net_if_addrs()
    for k,v in info.items():
        for item in v:
            if item[0] == 2 and not item[1]=='127.0.0.1':
                netcard_info.append((k,item[1]))

    if netcard_info:
        return netcard_info[0][1]


class LazyDict(object):
    """
    懒加载dict, 提供一个转换函数，只有在获取dict中的值时，才对指定值进行turn函数的调用
    """
    def __init__(self, d, turn):
        self.dict = d
        self.turn = turn

    def get(self, item):
        return self.dict.setdefault(item, self.turn(self.dict))

    def __getitem__(self, item):
           return self.get(item)

    def to_dict(self):
        return self.dict


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
    def init_logger(cls, settings, name):
        json = settings.get('LOG_JSON', True)
        level = settings.get('LOG_LEVEL', 'DEBUG')
        stdout = settings.get('LOG_STDOUT', True)
        dir = settings.get('LOG_DIR', 'logs')
        bytes = settings.get('LOG_MAX_BYTES', '10MB')
        backups = settings.get('LOG_BACKUPS', 5)
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


class SettingsWrapper(object):
    """
    配置文件加载装饰器用来加载和覆盖配置信息
    """
    my_settings = {}
    ignore = [
        '__builtins__',
        '__file__',
        '__package__',
        '__doc__',
        '__name__',
    ]

    def _init__(self):
        pass

    def load(self, local='localsettings.py', default='settings.py'):
        """
        加载配置字典
        :param local: 本地配置文件名
        :param default: 本地配置文件名
        :return: 配置信息字典
        """
        self._load_defaults(default)
        self._load_custom(local)

        return self.settings()

    def load_from_string(self, settings_string='', module_name='customsettings'):
        """
        从配置语句中获取配置信息
        :param settings_string: 配置信息语句
        :param module_name: 配置信息的环境变量
        :return:
        """
        mod = None
        try:
            mod = types.ModuleType(module_name)
            exec(settings_string in mod.__dict__)
        except TypeError:
            print("Could not import settings")
        self.my_settings = {}
        try:
            self.my_settings = self._convert_to_dict(mod)
        except ImportError:
            print("Settings unable to be loaded")

        return self.settings()

    def settings(self):
        """
        返回当时配置字典
        :return:
        """
        return self.my_settings

    def _load_defaults(self, default='settings.py'):
        """
        加载默认配置信息
        :param default:
        :return:
        """
        if isinstance(default, str) and default[-3:] == '.py':
            default = default[:-3]

        self.my_settings = {}
        try:
            if isinstance(default, str):
                settings = importlib.import_module(default)
            else:
                settings = default
            self.my_settings = self._convert_to_dict(settings)
        except ImportError:
            print("No default settings found")

    def _load_custom(self, settings_name='localsettings.py'):
        """
        加载自定义配置信息，覆盖默认配置
        :param settings_name:
        :return:
        """
        if isinstance(settings_name, str) and settings_name[-3:] == '.py':
            settings_name = settings_name[:-3]

        new_settings = {}
        try:
            if isinstance(settings_name, str):
                settings = importlib.import_module(settings_name)
            else:
                settings = settings_name
            new_settings = self._convert_to_dict(settings)
        except ImportError:
            print("No override settings found")

        for key in new_settings:
            if key in self.my_settings:
                item = new_settings[key]
                if isinstance(item, dict) and \
                        isinstance(self.my_settings[key], dict):
                    for key2 in item:
                        self.my_settings[key][key2] = item[key2]
                else:
                    self.my_settings[key] = item
            else:
                self.my_settings[key] = new_settings[key]

    def _convert_to_dict(self, setting):
        """
        将配置文件转化为字典
        :param setting:
        :return:
        """
        the_dict = {}
        set = dir(setting)
        for key in set:
            if key in self.ignore:
                continue
            value = getattr(setting, key)
            the_dict[key] = value
        return the_dict