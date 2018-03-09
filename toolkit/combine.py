# -*- coding:utf-8 -*-
import types

from operator import attrgetter
from functools import wraps, partial


class Combine(object):

    def __new__(cls, source_cls, part, words, keywords):
        if words:
            words = attrgetter(*words)
        if keywords:
            kwds = attrgetter(*keywords)
        s_p = dir(source_cls)
        c_p = [prop for prop in dir(part) if not prop.startswith("_")]
        for p in c_p:
            if p in s_p:
                setattr(source_cls, p, cls.combine(getattr(source_cls, p), getattr(part, p)))
            else:
                setattr(source_cls, p, getattr(part, p))

        init = source_cls.__init__

        @wraps(init)
        def inner(*args, **kwargs):
            init(*args, **kwargs)
            setattr(
                source_cls,
                part.__name__.lower(),
                part(
                    *words and words(args[0]),
                    **keywords and dict(zip(keywords, kwds(args[0])))
                ))
            setattr(source_cls, "__init__", inner)
        return source_cls

    @staticmethod
    def combine(prop1, prop2):
        if isinstance(prop1, types.FunctionType) and isinstance(prop2, types.FunctionType):
            @wraps(prop1)
            def wrapper(*args, **kwargs):
                prop1(*args, **kwargs)
                prop2(*args, **kwargs)
            return wrapper
        return prop2


def combine(part, words=(), keywords=()):
    """
      组合的装饰器实现，使用方法：
      @combine(Consoler)
      class Service():
          pass
      动态将Consoler组合到Service中，Service组合Consoler所有非下划线方法(依次调用)及属性(覆盖)，
      对于__init__方法，Service先调用自己的__init__然后再调用Consoler的__init__方法,
      调用Consoler时传入的参数为words, keywords指定，必须为Service实例属性，如:
      ("args.console_host", "args.console_port"), (
      """
    def outer(cls):
        return partial(Combine, part=part, words=words, keywords=keywords)(cls)
    return outer
