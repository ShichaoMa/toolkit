## python描述符备忘
### 对于python2，描述符类不能是经典类
__get__
```
In [23]: class D(object):
    ...:     def __get__(self, instance, cls):
    ...:         print(111111111)
    ...:         return 11111111
    ...:     def __set__(self, value, instance):
    ...:         print(22222222222)
    ...:

In [24]: class A(object):
    ...:     d = D()
    ...:     @classmethod
    ...:     def fun(cls):
    ...:         print(cls.d)
    ...:

In [25]: a = A()
# 通过实例访问，是需要通过描述符的
In [26]: a.d
111111111
Out[26]: 11111111
# 通过类访问，也需要通过描述符
In [27]: A.d
111111111
Out[27]: 11111111
# 通过类赋值，会直接把描述符覆盖掉
In [28]: A.d = 3
# 描述符没有了
In [29]: A.d
Out[29]: 3

In [30]: a.d
Out[30]: 3

In [31]: a = A()
# 重新创建一个实例也不行
In [32]: a.d
Out[32]: 3
```