### 这是在custom-redis项目中用到例子，介绍了元类new方法的实现，以及元类继承

```python
class Meta(type):
    """元类基类，给方法增加装饰器"""
    wrapper = None

    def __new__(typ, name, bases, properties):
        # 一些公共继承方法继承在DataStore里面，不需要被装饰，通过其基类来判断要构造的是否为DataStore类
        if bases[0] != object:
            for k, v in properties.items():
                if isinstance(v, types.FunctionType):
                    # 由于这个方法会被继承，通过提供不同的wrapper函数来做不同的包装， RedisMeta没有提供，所以不包装
                    properties[k] = typ.wrapper(v) if typ.wrapper else v
        return super(Meta, typ).__new__(typ, name, bases, properties)


class StoreMeta(Meta):
    """数据类专用元类"""
    wrapper = staticmethod(data_cmd_wrapper)


class CommonCmdMeta(StoreMeta):
    """通用函数类专用元类"""
    wrapper = staticmethod(common_cmd_wrapper)


class RedisMeta(CommonCmdMeta):
    """Redis类专用元类"""
    wrapper = None

    def __new__(typ, *args, **kwargs):
        # 这个地方非常诡异， 如果通过type(*args)来组建类，类会使用CommonCmdMeta来创建，可能原因是通过type返回的类是type创建的
        # 当使用默认type创建时，python认为该类没有指定元类，所以继续调用了父类的元类进行创建。
        # 通过type.__new__则会使用RedisMeta创建
        # 不通过super(RedisMeta, typ).__new__(typ, *args)创建，是因为这样会调用CommonCmdMeta.__new__，这不是我们想要的。
        # 这里我们不需要对CustomRedis类的函数进行包装操作，所以选择使用type.__new__创建
        return super(RedisMeta, typ).__new__(typ, *args)

    def __init__(cls, *args, **kwargs):
        # 当创建的实例(在这里是类)不是RedisMeta类型时，比如通过type()直接返回，__init__不会被调用。
        pass
```

详细代码参见[bases.py](https://github.com/ShichaoMa/custom_redis/blob/update3/custom_redis/server/bases.py)

实例化时的调用顺序

- 元类的__call__
- 类的__new__
- 类的__init__

子类的元类(除type以外)必须是父类元类的子类，使用了元类的类的子类也会使用该元类创建

参见[singleton.py](https://github.com/ShichaoMa/toolkit/blob/master/toolkit/singleton.py)

[comment]: <tags> (python,meta,class)
[comment]: <description> (python 元类，类，实例创建时的一些理解)
[comment]: <title> (python元类，类，实例)
[comment]: <author> (夏洛之枫)