# -*- coding:utf-8 -*-
import types

from functools import wraps
from operator import attrgetter


def combine(part, words=(), keywords=(), after=True, extend=False):
    """
      组合的装饰器实现，使用方法：
      @combine(Consoler)
      class Service():
          pass
      动态将Consoler组合到Service中，Service组合Consoler所有非下划线方法及属性(覆盖)，
      after参数确定有相同方法存在时调用的顺序，True时Consoler方法在Service后调用。
      extend参数确定是否是继承关系，这决定了在调用part方法时使用part对象还是被组合的对象
      对于__init__方法，Service先调用自己的__init__然后再调用Consoler的__init__方法,
      调用Consoler时传入的参数为words, keywords指定，必须为Service实例属性，如:
      ("args.console_host", "args.console_port"), keywords 与words参数一样，
      不过在传入__init__时使用关键字参数的形式。
      属性优先级：Service实例属性，Console类属性，Service类属性，Console实例属性。
      """
    def outer(source_cls):
        if not hasattr(source_cls, "combines"):
            setattr(source_cls, "combines", [part])
        else:
            source_cls.combines.append(part)
        if words:
            wds = attrgetter(*words)
        if keywords:
            kwds = attrgetter(*keywords)
        s_p = dir(source_cls)
        c_p = [prop for prop in dir(part) if not prop.startswith("_")]

        for p in c_p:
            if p in s_p:

                def closure():
                    prop1 = getattr(source_cls, p)
                    prop2 = getattr(part, p)
                    if isinstance(prop1, types.FunctionType) \
                            and isinstance(prop2, types.FunctionType):

                        @wraps(prop1)
                        def wrapper(*args, **kwargs):
                            if extend:
                                self = args[0]
                            else:
                                self = getattr(
                                    args[0], part.__name__.lower(), args[0])
                            if after:
                                result = prop1(*args, **kwargs)
                                prop2(self, *args[1:], **kwargs)
                                return result
                            else:
                                result = prop2(self, *args[1:], **kwargs)
                                prop1(*args, **kwargs)
                                return result
                        return wrapper
                    return prop2

                setattr(source_cls, p, closure())
            else:
                setattr(source_cls, p, getattr(part, p))

        __init = getattr(source_cls, "__init__",
                         gen_default_method("__init__", locals()))

        @wraps(__init)
        def _init(*args, **kwargs):
            __init(*args, **kwargs)
            if len(words) == 0:
                a = tuple()
            elif len(words) == 1:
                a = [wds(args[0])]
            else:
                a = wds(args[0])
            if len(keywords) == 0:
                k = {}
            elif len(keywords) == 1:
                k = {keywords[0]: kwds(args[0])}
            else:
                k = dict(zip(keywords, kwds(args[0])))
            parter = part(*a, **k)
            setattr(args[0], part.__name__.lower(), parter)
            setattr(parter, source_cls.__name__.lower(), args[0])

        setattr(source_cls, "__init__", _init)

        def closure():
            __getattr = getattr(source_cls, "__getattr__",
                                gen_default_method(
                                    "__getattr__", locals(),
                                    "raise AttributeError"))
            part_name = part.__name__.lower()

            @wraps(__getattr)
            def _getattr(*args, **kwargs):
                try:
                    result = __getattr(*args, **kwargs)
                    return result
                except AttributeError:
                    if args[1] in \
                            [c.__name__.lower() for c in source_cls.combines]:
                        raise
                    return getattr(
                        getattr(
                            args[0], part_name, args[0]), *args[1:], **kwargs)
            return _getattr

        setattr(source_cls, "__getattr__", closure())

        return source_cls

    return outer


def gen_default_method(name, namespace=locals(), option=""):
    def_temp = """def {name}(self, *args, **kwargs):
    if [b for b in source_cls.__bases__ if hasattr(b, "{name}")]:
        return super(source_cls, self).{name}(*args, **kwargs)
    {option}
    """.format(name=name, option=option)
    exec(def_temp, namespace)
    return eval(name, namespace)
