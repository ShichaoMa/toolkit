"""
实例创建时，调用顺序
元类的__call__
类的__new__
类的__init__
子类的元类(除type以外)必须是父类元类的子类
使用了元类的类的子类也会使用该元类创建
"""
from threading import RLock


__all__ = ["Singleton"]


class Singleton(type):
    """
    单例类实现
    """
    lock = RLock()

    def __new__(mcs, *args, **kwargs):
        """
        元类msc通过__new__组建类对象，其中msc指Singleton
        :param args: 可以包含类构建所需要三元素，类名,父类,命名空间, 其中
        命名空间中__qualname__和函数的__qualname__均含有classname做为前缀，
        在这里，如果想替换类名，需要把以上全部替换才可以。
        :param kwargs: 可以自定义传递一些参数
        :return: 返回类对象,通过super(Singleton, mcs).__new__此时已经组装好了类
        """
        class_name, bases, dict = args
        dict["_instance"] = None
        cls = super(Singleton, mcs).__new__(
            mcs, class_name, bases, dict, **kwargs)
        return cls

    def __call__(cls, *args, **kwargs):
        with cls.lock:
            cls._instance = cls._instance or super(Singleton, cls).__call__(
                *args, **kwargs)
            return cls._instance


if __name__ == "__main__":

    class A(metaclass=Singleton):
        pass

    print(A() is A())