# -*- coding:utf-8 -*-
import types

from functools import wraps, partial


class Combine(object):

    def __new__(cls, source_cls, part):
        s_p = dir(source_cls)
        c_p = [prop for prop in dir(part) if not prop.startswith("_")]
        for p in c_p:
            if p in s_p:
                setattr(source_cls, p, cls.conbine(getattr(source_cls, p), getattr(part, p)))
            else:
                setattr(source_cls, p, getattr(part, p))
        if "__init__" in s_p:
            init = source_cls.__init__

            @wraps(init)
            def inner(*args, **kwargs):
                init(*args, **kwargs)
                setattr(source_cls, part.__name__.lower(), part(args[0]))

            setattr(source_cls, "__init__", inner)
        return source_cls

    @staticmethod
    def conbine(prop1, prop2):
        if isinstance(prop1, types.FunctionType) and isinstance(prop2, types.FunctionType):
            @wraps(prop1)
            def wrapper(*args, **kwargs):
                prop1(*args, **kwargs)
                prop2(*args, **kwargs)
            return wrapper
        return prop2


def combine(part):
    """
      组合的装饰器实现，使用方法：
      @combine(Consoler)
      class Service():
          pass
      动态将Consoler组合到Service中，Service组合Consoler所有非下划线方法(依次调用)及属性(覆盖)，
      对于__init__方法，Service先调用自己的__init__然后再调用Consoler的__init__方法并传入Service实例,
      所以被组合的类__init__要有参数接收。
      """
    def outer(cls):
        return partial(Combine, part=part)(cls)
    return outer
