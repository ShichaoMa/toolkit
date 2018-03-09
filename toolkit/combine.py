# -*- coding:utf-8 -*-
import types

from operator import attrgetter
from functools import wraps, partial


def combine(part, words=(), keywords=(), after=True, extend=False):
    """
      组合的装饰器实现，使用方法：
      @combine(Consoler)
      class Service():
          pass
      动态将Consoler组合到Service中，Service组合Consoler所有非下划线方法(依次调用)及属性(覆盖)，
      对于__init__方法，Service先调用自己的__init__然后再调用Consoler的__init__方法,
      调用Consoler时传入的参数为words, keywords指定，必须为Service实例属性，如:
      ("args.console_host", "args.console_port"), keywords 与args参数一样，不过在传入__init__时
      使用关键字参数的形式。
      after确定有相同方法存在时调用的顺序
      extend确定是否是继承关系，这决定了在调用part方法时使用part对象还是被组合的对象
      """
    def outer(source_cls):
        if words:
            wds = attrgetter(*words)
        if keywords:
            kwds = attrgetter(*keywords)
        s_p = dir(source_cls)
        c_p = [prop for prop in dir(part) if not prop.startswith("_")]
        for p in c_p:
            if p in s_p:
                prop1 = getattr(source_cls, p)
                prop2 = getattr(part, p)
                if isinstance(prop1, types.FunctionType) and isinstance(prop2, types.FunctionType):

                    @wraps(prop1)
                    def wrapper(*args, **kwargs):
                        if extend:
                            self = args[0]
                        else:
                            self = getattr(args[0], part.__name__.lower())
                        if after:
                            prop1(*args, **kwargs)
                            prop2(self, *args[1:], **kwargs)
                        else:
                            prop2(self, *args[1:], **kwargs)
                            prop1(*args, **kwargs)
                    setattr(source_cls, p, wrapper)
                    continue
            setattr(source_cls, p, getattr(part, p))

        init = source_cls.__init__

        @wraps(init)
        def inner(*args, **kwargs):
            init(*args, **kwargs)
            parter = part(
                    *words and words(args[0]),
                    **keywords and dict(zip(keywords, kwds(args[0])))
                )
            setattr(args[0], part.__name__.lower(), parter)
            setattr(parter, source_cls.__name__.lower(), args[0])
        setattr(source_cls, "__init__", inner)

        return source_cls
    return outer
