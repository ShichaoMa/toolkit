"""
实例创建时，调用顺序
元类的__call__
类的__new__
类的__init__
子类的元类(除type以外)必须是父类元类的子类
"""


class Singleton(type):
    """
    单例类实现
    """
    def __new__(mcs, *args, **kwargs):
        """
        元类msc通过__new__组建类对象，其中msc指Singleton
        :param args: 可以包含类构建所需要三元素，类名,父类,命名空间, 其中命名空间中__qualname__和函数的__qualname__均含有classname做为前缀，在这里，如果想替换类名，需要把以上全部替换才可以。
        :param kwargs: 可以自定义传递一些参数
        :return: 返回类对象,通过super(Singleton, mcs).__new__此时已经组装好了类
        """
        class_name, bases, dict = args
        from toolkit import debugger
        # class_name = class_name.capitalize()
        # dict["__qualname__"] = class_name.capitalize()
        # for value in dict.values():
        #     if hasattr(value, "__qualname__"):
        #         value.__qualname__ = value.__qualname__.replace(class_name, class_name.capitalize())
        cls = super(Singleton, mcs).__new__(mcs, class_name, bases, dict, **kwargs)
        return cls

    def __init__(cls, what, bases=None, dict=None):
        cls.instance = None
        super(Singleton, cls).__init__(what, bases, dict)

    def __call__(cls, *args, **kwargs):
        print(11111111)
        cls.instance = cls.instance or super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class abc(object, metaclass=Singleton):

    name = 1

    def __new__(cls, *args, **kwargs):
        print(33333333)
        return super().__new__(cls)

    def fun(self):
        pass


class bcd(abc, metaclass=TwoTon):

    def __new__(cls, *args, **kwargs):
        print(22222222)
        return object.__new__(cls)

    def bar(self):
        pass

print(bcd())
