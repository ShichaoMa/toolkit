[comment]: <> (![](https://dbader-static-defugurjmqrkjo.netdna-ssl.com/figures/python-abcs-header.png))
python中存在abc模块用来获取抽象类，通常的使用方法是先使用ABCMeta创建一个抽象类，使用abstractmethod定义需要子类实现的接口，再通过多继承(maxin)的方式使用它，如下

    
    
    from abc import ABC, ABCMeta, abstractmethod
    # 创建一个抽象基类
    class A(metaclass=ABCMeta):
        @abstractmethod
        def foo(self):
            print("这是一个抽象方法，不能直接调用，但可以在子类实例中调用")
    # 或者
    class A(ABC):
        @abstractmethod
        def foo(self):
            print("这是一个抽象方法，不能直接调用，但可以在子类实例中调用")
    
    # 直接继承抽象类
    class B(A):
        pass
    
    B() # 创建失败
    
    # 直接继承抽象类并实现抽象方法
    class C(A):
        def foo(self):
            super(C, self).foo()
            print("C中的实现")
    
    C()
    
    # 创建一个不相关的基类
    class D(object):
        def bar(self):
            print("这是一个不相关的方法")
    
    # 通过maxin来创建一个混合类
    class E(D, A):
        pass
    
    E() #创建失败，未实现A中的抽象方法
    
    # 通过maxin来创建一个混合类，并实现抽象方法
    class F(D, A):
        def foo(self):
            print("这是F中的实现")
    
    F()
    
    # 创建一个不相关的类，但实现了抽象方法
    class G(object):
        def foo(self):
            print("这是G中的实现")
    
    # 创建混合类
    class H(G, A):
        pass
    
    H()
    


[comment]: <tags> (python,abc)
[comment]: <description> (关于python中实现抽象类的手段)
[comment]: <title> (abc模块的使用方法)
[comment]: <author> (夏洛之枫)