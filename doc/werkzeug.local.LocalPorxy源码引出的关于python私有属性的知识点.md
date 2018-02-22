[comment]: <> (![](http://werkzeug.pocoo.org/static/werkzeug.png))
 
源码中有如下代码
```
class LocalProxy(object):

    #__slots__ = ('__local', '__dict__', '__name__')

    def __init__(self, local, name=None):
        object.__setattr__(self, '_LocalProxy__local', local)
        print(self.__local)
        object.__setattr__(self, '__name__', name)
`
```
print是我后加去的，通过object.\_\_setattr\_\_(self, '_LocalProxy__local', local)，可以设置为LocalProxy设置__local私有属性，私有属性通过self.__local在类内部是可以访问的，但是如果通过外部实例的方式，则无法访问，比如
```
In [1]: class A:
   ...:     def __init__(self):
   ...:         self.__a = 0
   ...:

In [2]: A().__a
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-2-ae9317e12fa9> in <module>()
----> 1 A().__a

AttributeError: A instance has no attribute '__a'

In [3]: A()._A__a
Out[3]: 0

In [4]: dir(A())
Out[4]: ['_A__a', '__doc__', '__init__', '__module__']

In [5]: class B:
   ...:     def __init__(self):
   ...:         self._B__b = 0
   ...:         print self.__b
   ...:

In [6]: B()
0
Out[6]: <__main__.B instance at 0x028C56C0>

# 由上可知，如果通过self._LocalProxy__local，也可以实现对私有属性的访问。
# 至于为什么LocalProxy要使用object.__setattr__(self, '_LocalProxy__local', local)实现属性赋值而不是使用self.__local=local呢。
# 因为，通过self.__local的方式会触发LocalProxy 重写的方法__setattr__，这显然是不可以的。
```
[comment]: <tags> (werkzeug,python)
[comment]: <description> (werkzeug源码阅读有感)
[comment]: <title> (werkzeug.local.LocalPorxy源码引出的关于python私有属性的知识点)
[comment]: <author> (夏洛之枫)