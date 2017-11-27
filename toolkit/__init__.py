# -*- coding:utf-8 -*-
import os
import re
import time
import json
import types
import socket
import psutil
import signal
import logging

from queue import Empty
from functools import wraps, reduce

__version__ = '1.1.1'


def duplicate(iterable, keep=lambda x: x, key=lambda x: x, reverse=False):
    """
    保序去重
    :param iterable:
    :param keep: 去重的同时要对element做的操作
    :param key: 使用哪一部分去重
    :param reverse: 是否反向去重
    :return:
    """
    result = list()
    duplicator = list()
    if reverse:
        iterable = reversed(iterable)
    for i in iterable:
        keep_field = keep(i)
        key_words = key(i)
        if key_words not in duplicator:
            result.append(keep_field)
            duplicator.append(key_words)
    return list(reversed(result)) if reverse else result


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
    格式化html, 去掉多余的字符，类，script等。
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
    return reduce(lambda string, replacement: re.sub(replacement[0], replacement[1], string), trims, html)


def urldecode(query):
    """
    与urlencode相反，不过没有unquote
    :param query:
    :return:
    """
    if not query.strip():
        return dict()
    return dict(x.split("=") for x in query.strip().split("&"))


def re_search(re_str, text, dotall=True, default=""):
    """
    抽取正则规则的第一组元素
    :param re_str:
    :param text:
    :param dotall:
    :param default:
    :return:
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    if not isinstance(re_str, list):
        re_str = [re_str]

    for rex in re_str:
        rex = (re.compile(rex, re.DOTALL) if dotall else re.compile(rex)) if isinstance(rex, str) else rex
        match_obj = rex.search(text)

        if match_obj is not None:
            t = match_obj.group(1).replace('\n', '')
            return t

    return default


class P22P3Encoder(json.JSONEncoder):
    """
    python2转换python3时使用的json encoder
    """
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, (types.GeneratorType, map, filter)):
            return list(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


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


def _find_caller_name(is_func=False):
    frame = logging.currentframe()
    src_filename = os.path.normcase(get_ip.__code__.co_filename)
    while True:
        co = frame.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == src_filename:
            frame = frame.f_back
            continue
        break
    if is_func:
        return co.co_name
    else:
        return os.path.basename(co.co_filename).split(".")[0]


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
