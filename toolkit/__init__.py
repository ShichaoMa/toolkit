# -*- coding:utf-8 -*-
import os
import re
import sys
import pdb
import time
import json
import types
import ctypes
import socket
import signal
import inspect
import logging
import warnings

from queue import Empty
from future.utils import raise_from
from functools import wraps, reduce, partial

__version__ = '1.7.22'


_ITERABLE_SINGLE_VALUES = dict, str, bytes


def test_prepare(search_paths=[".."]):
    """
    单元测试时，动态添加模块搜索路径。
    :param search_paths:
    :return:
    """
    for search_path in search_paths:
        sys.path.insert(0, os.path.abspath(search_path))
    del sys.modules["toolkit"]


def debugger():
    try:
        debug = bool(eval(os.environ.get("DEBUG", "0").lower().capitalize()))
    except Exception:
        debug = False

    if debug:
        d = pdb.Pdb()
        d.set_trace( sys._getframe().f_back)


def arg_to_iter(arg):
    """
    将非可迭代对象转换成可迭代对象
    """
    if arg is None:
        return []
    elif not isinstance(arg, _ITERABLE_SINGLE_VALUES) \
            and hasattr(arg, '__iter__'):
        return arg
    else:
        return [arg]


class Compose(object):
    """
    连接多个函数
    如果is_pipe=True，那么将第一个函数的结果做为第二个函数的参数
    否则，返回所有函数结果集列表将传aggregation中进行聚合
    """
    def __init__(self, *functions, is_pipe=False,
                 aggregation=partial(reduce, lambda x, y: x and y)):
        self.functions = functions
        self.is_pipe = is_pipe
        self.aggregation = aggregation

    def __call__(self, *args, **kwargs):
        result_set = []
        for index, func in enumerate(self.functions):
            if not index or not self.is_pipe:
                result_set.append(func(*args, **kwargs))
            else:
                result_set[0] = func(result_set[0])
        return self.aggregation(
            result_set or [0, 0]) if len(result_set) !=1 else result_set[0]


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
    去掉匹配成功的字段
    :param value:
    :param old: 可以为正则表达示或字符串
    :param new:
    :return:
    """
    if hasattr(old, "sub"):
        return old.sub(new, value)
    else:
        return value.replace(old, new)


def wrap_key(json_str, key_pattern=re.compile(r"([a-zA-Z_]\w*)[\s]*\:")):
    """
    将javascript 对象字串串形式的key转换成被双字符包裹的格式如{a: 1} => {"a": 1}
    :param json_str:
    :param key_pattern:
    :return:
    """
    return key_pattern.sub('"\g<1>":', json_str)


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
    连接多个序列或字典
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
    将要被json.loads的字符串的单引号转换成双引号，
    如果该单引号是元素主体，而不是用来修饰字符串的。则不对其进行操作。
    :param json_str:
    :return:
    """
    if not isinstance(json_str, str):
        return json_str

    double_quote = []
    new_lst = []
    for index, val in enumerate(json_str):
        if val == '"' and not len(_get_last_backslash(json_str[:index])) % 2:
            if double_quote:
                double_quote.pop(0)
            else:
                double_quote.append(val)
        if val == "'" and not len(_get_last_backslash(json_str[:index])) % 2:
            if not double_quote:
                val = '"'
        new_lst.append(val)
    return "".join(new_lst)


def _get_last_backslash(strings, regex=re.compile(r"\\*$")):
    mth = regex.search(strings)
    if mth:
        return mth.group()
    return ""


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
    return reduce(lambda string, replacement:
                  re.sub(replacement[0], replacement[1], string), trims, html)


def urldecode(query):
    """
    与urlencode相反，不过没有unquote
    :param query:
    :return:
    """
    return dict(x.split("=")
                for x in query.strip().split("&")) if query.strip() else dict()


def re_search(regex, text, dotall=True, default=""):
    """
    抽取正则规则的第一组元素
    :param regex:
    :param text:
    :param dotall:
    :param default:
    :return:
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    if not isinstance(regex, list):
        regex = [regex]
    for rex in regex:
        rex = (re.compile(rex, re.DOTALL)
               if dotall else re.compile(rex)) if isinstance(rex, str) else rex
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
        return json.JSONEncoder.default(self, obj)


def retry_wrapper(
        retry_times, exception=Exception, error_handler=None, interval=0.1):
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
                        result = error_handler(
                            func.__name__, count, e, *args, **kwargs)
                        if result:
                            count -= 1
                    if count >= retry_times:
                        raise
                    time.sleep(interval)
        return wrapper
    return out_wrapper


def timeout(timeout_time, default):
    """
    装饰一个方法，用来限制其执行时间，超时后返回default，只能在主线程使用。
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
    return dict((k.replace(".", "_"), v) for k, v in data.items())


def groupby(it, key):
    """
    自实现groupby，itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    :return: 字典对象
    """
    groups = dict()
    for item in it:
        groups.setdefault(key(item), []).append(item)
    return groups


def parse_cookie(string, regex=re.compile(r'([^=]+)=([^\;]+);?\s?')):
    """
    解析cookie
    :param string:
    :param regex: 正则表达式
    :return:
    """
    return dict((k, v) for k, v in regex.findall(string))


def async_produce_wrapper(producer, logger, batch_size=10):
    """
    pykafka实现异步生产时，使用的装饰器
    `
    self.producer.produce =
    async_produce_wrapper(self.producer, self.logger)(self.producer.produce)
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


def load_function(function_str):
    """
    返回字符串表示的函数对象
    :param function_str: module1.module2.function
    :return: function
    """
    warnings.warn("load_function() is a deprecated alias since 1.7.19, "
                  "use load() instead.",
                  DeprecationWarning, 2)
    mod_str, _sep, function_str = function_str.rpartition('.')
    if mod_str:
        return getattr(load_module(mod_str), function_str)
    else:
        # 可能整体是一个模块
        return load_module(function_str)
    

load_class = load_function


def load_module(module_str):
    """
    返回字符串表示的模块
    :param module_str: os.path
    :return: os.path
    """
    warnings.warn("load_function() is a deprecated alias since 1.7.19, "
                  "use load() instead.",
                  DeprecationWarning, 2)
    return __import__(module_str, fromlist=module_str.split(".")[-1])


def load(prop_str):
    """
    返回字符串表示的模块、函数、类、若类的属性等
    :param prop_str: module1.class.function....
    :return: function
    """
    attr_list = []
    # 每次循环将prop_str当模块路径查找，成功则返回，
    # 失败则将模块路径回退一级，将回退的部分转换成属性
    # 至到加载模块成功后依次从模块中提取属性。
    ex = None
    while prop_str:
        try:
            obj = __import__(prop_str, fromlist=prop_str.split(".")[-1])
            for attr in attr_list:
                obj = getattr(obj, attr)
            return obj
        except (AttributeError, ImportError) as e:
            prop_str, _sep, attr_str = prop_str.rpartition('.')
            attr_list.insert(0, attr_str)
            try:
                raise_from(ImportError(), e)
            except Exception as e:
                ex = e
    else:
        raise ex


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


def thread_safe(lock):
    """
    对指定函数进行线程安全包装，需要提供锁
    :param lock: 锁
    :return:
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorate


def thread_safe_for_method(func):
    """
    对类中的方法进行线程安全包装
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with args[0].lock:
            return func(*args, **kwargs)
    return wrapper


def call_later(callback, call_args=tuple(), immediately=True, interval=1):
    """
    应用场景：
    被装饰的方法需要大量调用，随后需要调用保存方法，
    但是因为被装饰的方法访问量很高，而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后，再调用保存方法。
    规定间隔内，无论调用多少次被装饰方法，保存方法只会
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


def get_ip():
    """
    获取局域网ip
    :return:
    """
    try:
        import psutil
    except ImportError:
        warnings.warn(
            "get_ip function depends on psutil, try: pip install psutil. ")
        raise
    netcard_info = []
    info = psutil.net_if_addrs()
    for k,v in info.items():
        for item in v:
            if item[0] == 2 and not item[1]=='127.0.0.1':
                netcard_info.append((k,item[1]))

    if netcard_info:
        return netcard_info[0][1]


def _find_caller_name(is_func=False, steps=1):
    frame = logging.currentframe()
    for i in range(steps + 1):
        co = frame.f_code
        frame = frame.f_back

    if is_func:
        return co.co_name
    else:
        filename = os.path.basename(co.co_filename).split(".")[0]
        if filename == "__init__":
            filename = os.path.basename(os.path.dirname(co.co_filename))
        return filename


class LazyDict(object):
    """
    懒加载dict, 提供一个转换函数，只有在获取dict中的值时，才对指定值进行turn函数的调用
    """
    def __init__(self, d, turn):
        self.dict = d
        self.turn = turn

    def get(self, item):
        return self.dict.setdefault(item, self.turn(item, self.dict))

    def __getitem__(self, item):
        return self.get(item)

    def to_dict(self):
        return self.dict


def cache_property(func):
    """
    缓存属性，只计算一次
    :param func:
    :return:
    """
    @property
    @wraps(func)
    def wrapper(*args, **kwargs):
        if func.__name__ not in args[0].__dict__:
            args[0].__dict__[func.__name__] = func(*args, **kwargs)
        return args[0].__dict__[func.__name__]
    return wrapper


class cache_prop(object):
    """
    描述符版缓存属性，无法被覆盖
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if self.func.__name__ in instance.__dict__:
            return instance.__dict__[self.func.__name__]
        else:
            return instance.__dict__.setdefault(
                self.func.__name__, self.func(instance))

    def __set__(self, instance, value):
        raise AttributeError("{} is readonly.".format(self.func.__name__))


def cache_for(timeout=10):
    """
    缓存属性，指定缓存失效时间
    :param timeout: 缓存失效时间 second
    :return:`
    """
    def outer(func):
        @property
        @wraps(func)
        def inner(*args, **kwargs):
            prop_name = func.__name__
            prop_start_name = "%s_cache_start_time" % prop_name
            if time.time() - args[0].__dict__.get(prop_start_name, 0) > timeout:
                args[0].__dict__[prop_name] = func(*args, **kwargs)
                args[0].__dict__["%s_cache_start_time" % prop_name] = time.time()
            return args[0].__dict__[prop_name]
        return inner
    return outer


def free_namedtuple(func):
    """
    根据一个类及其参数创建一个类namedtuple class，
    但不同之处在于创建实例成功后可以自由赋值，初时化时指定的值决定其Hash和eq结果
    :param func:
    :return:
    """
    cls_tmpl = """
class {}(object):
    def __init__(self, {}):
        {}
    def __hash__(self):
        return {}

    def __eq__(self, other):
        return {}
"""

    args = inspect.getargspec(func).args
    if args and args[0] in ["self", "cls"]:
        args.pop(0)

    class_name = func.__name__.capitalize()
    init_arg = ", ".join(args + "=None" for args in args) if args else ""
    init_body = "".join(
        "self.{%s} = {%s}\n        " % (
            index, index) for index in range(len(args))).format(*args) if args else "pass"
    hash_body = " + ".join("hash(self.{})".format(arg) for arg in args) if args else "0"
    eq_body = " and ".join("self.{0} == other.{0}".format(arg) for arg in args) if args else "True"
    namespace = dict(__name__='entries_%s' % class_name)
    class_str = cls_tmpl.format(class_name, init_arg, init_body, hash_body, eq_body)
    exec(class_str, namespace)
    return namespace[class_name]


def cache_method(timeout=10):
    """
    缓存一个方法的调用结果，持续一定时长，
    根据不同的调用参数来缓存不同的结果，调用参数必须是可hash的，
    该方法调用正常时，希望返回真值(形式上为真)，若返回值为假，缓存效果会失效。
    :param timeout: 缓存时长 :s
    :return:
    """
    def cache(func):
        entry_class = free_namedtuple(func)
        data = dict()

        @wraps(func)
        def inner(*args, **kwargs):
            for k in data.keys():
                if time.time() - timeout > data[k].ts:
                    del data[k]

            entry = entry_class(*args[1:], **kwargs)
            entry.ts = time.time()
            stored = data.get(entry, entry)
            if entry not in data or time.time() - timeout > stored.ts:
                entry.result = func(*args, **kwargs)
                if entry.result:
                    data[entry] = entry
                return entry.result
            else:
                return stored.result
        return inner
    return cache


def cache_method_for_updated(func):
    """
    缓存方法调用结果直到实例的updated返回True，与cache_method类似。
    @param func:
    @return:
    """
    entry_class = free_namedtuple(func)
    data = dict()

    @wraps(func)
    def inner(*args, **kwargs):
        self = args[0]
        # 没有更新方法(直接使用子类，而不通过cache)，不进行缓存操作
        if not self.updated:
            return func(*args, **kwargs)
        # 如果pandora配置已更新，则清除所有缓存
        if self.updated():
            data.clear()
        entry = entry_class(*args[1:], **kwargs)
        stored = data.get(entry, entry)

        if entry not in data:
            entry.result = func(*args, **kwargs)
            if entry.result:
                data[entry] = entry
            return entry.result
        else:
            return stored.result

    return inner


class SafeValue(object):
    """
    获取某个对象的某个属性值，如果该属性不存在，则返回该对象
    """
    def __init__(self, node):
        self.node = node

    def __getattr__(self, item):
        return getattr(self.node, item, self.node)


def overflow(val, btc):
    """
    对于超出字节长度的数字转换成负数
    :param val:
    :param btc: 字节长度
    :return:
    """
    max_val = 2 ** (8*btc-1) - 1
    if not -max_val - 1 <= val <= max_val:
        val = (val + (max_val + 1)) % (2 * (max_val + 1)) - max_val - 1
    return val


def int_overflow(val):
    """
    类似js对于超过int范围的数转换成负数
    :param val:
    :return:
    """
    return overflow(val, 4)


def unsigned_right_shift(n, i):
    """
    无符号右移python实现
    :param n:
    :param i:
    :return:
    """
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def shift_left_for_js(num, count):
    """位运算左移js版"""
    return int_overflow(num << count)


def shift_right_for_js(num, count):
    """位运算左移js版"""
    return int_overflow(num >> count)


async def readexactly(stream, n):
    """
    asyncio stream read
    :param steam:
    :param n:
    :return:
    """
    if hasattr(stream, "_exception") and stream._exception is not None:
        raise stream._exception

    blocks = []
    while n > 0:
        block = await stream.read(n)
        if not block:
            break
        blocks.append(block)
        n -= len(block)

    return b''.join(blocks)


class NotImplementedProp(object):
    """
    用来对子类需要实现的类属性进行占位
    """
    def __get__(self, instance, owner):
        return NotImplemented


class classproperty(object):
    """
    property只能用于实例方法到实例属性的转换，使用classproperty来支持类方法到类属性的转换
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(owner)


def cache_classproperty(func):
    """
    缓存类属性，只计算一次
    :param func:
    :return:
    """
    @classproperty
    @wraps(func)
    def wrapper(*args, **kwargs):
        prop_name = "_" + func.__name__
        if prop_name not in args[0].__dict__:
            setattr(args[0], prop_name, func(*args, **kwargs))
        return args[0].__dict__[prop_name]
    return wrapper


if __name__ == "__main__":
    def a(v):
        return v
    def b(v):
        return v
    def c(v):
        return 2
    print(Compose(a,b,c)())
