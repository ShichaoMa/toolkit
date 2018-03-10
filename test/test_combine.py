# -*- coding:utf-8 -*-
from toolkit import test_prepare
test_prepare()
from toolkit.combine import combine


class A:
    a = 1

    def __init__(self):
        print("__init__ in A. self:", self)

    def fun(self):
        print("fun in A. self:", self)
        return 2

    def __getattr__(self, item):
        if item == "d":
            return 33
        raise AttributeError


class B:
    a = 2

    def __init__(self):
        self.c = 11
        self.d = 55
        print("__init__ in B. self:", self)

    def fun(self):
        print("fun in B.  self:", self)
        return 3


@combine(B)
class C(A):
    """
    默认组合方式，所有方法各自调各自的
    """
    pass


c = C()
print(c.a)
print(c.fun())


@combine(B, after=False)
class D(A):
    """
    默认组合方式，所有方法各自调各自的,但除__init__的方法(fun)调用顺序变了
    """
    pass


d = D()
print(d.fun())


@combine(B, extend=True)
class E(A):
    """
    继承方式，除了__init__方法以外，使用E的实例来调用
    """
    pass


e = E()
print(e.fun())


@combine(B)
class G(A):
    """
    在__init__中调用普通方法，无论是继承还是组合的方式，全部使用G的实例调用。
    """
    def __init__(self):
        print("__init__ in G. self:", self)
        super(G, self).__init__()
        self.fun()


g = G()
print(g.c)


@combine(B)
class H(A):
    """
    B中的实例属性cc被代理了
    """
    pass

h = H()
print(h.c)


@combine(B)
class I(A):
    """
    I的类属性c存在，所以没有用使用B的实例属性
    """
    c = 22


i = I()
print(i.c)


@combine(B)
class J(A):
    """
    d使用__getattr__获取，没有使用B中的实例属性
    """
    pass

j = J()
print(j.d)


