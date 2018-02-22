[comment]: <> (![](http://www.mashichao.com/static/img/pretty/0.jpg))
在阅读流畅的python这本书时，发现p509页在介绍__getattribute__时说到，寻找属性是特殊属性或特殊方法时除外。

    
    
    In [6]: def q(name):
       ...:     def q_g(instance):
       ...:         print(4444444444444)
       ...:         return instance.__dict__[name]
       ...:     def q_s(instance, value):
       ...:         if value > 0:
       ...:             instance.__dict__[name] = value
       ...:         else:
       ...:             raise ValueError("value must be > 0")
       ...:     return property(q_g, q_s)
       ...:
    
    
      
    
    
    
    In [4]: class A:
       ...:     w = q("w")
       ...:     def __init__(self, description, w):
       ...:         self.d = description
       ...:         self.w = w
       ...:     def __getattribute__(self, name):
       ...:         print(3333333333)
       ...:         return super(A, self).__getattribute__(name)
       ...:
    In [8]: a = A(33, 44)
    3333333333
    
    In [9]: a.w
    3333333333
    4444444444444
    3333333333
    Out[9]: 44
    

通过以上的测试得出结果，当属性是描述符或__dict__，双下属性或方法时，同样会调用__getattribute__，因此可以猜测__getattribute__底层实现调用顺序为描述符，
self.\_\_dict\_\_.\_\_getitem\_\_, 类属性,
\_\_getattr\_\_方法。对于添加属性，__setattr__底层的调用为描述符，self.\_\_dict\_\_.\_\_setitem\_\_，如果描述符没有提供\_\_set\_\_方法，那么描述符会被覆盖。


[comment]: <tags> (__getattribute__,python)
[comment]: <description> (流畅的python中的错误)
[comment]: <title> (关于__getattribute__)
[comment]: <author> (夏洛之枫)