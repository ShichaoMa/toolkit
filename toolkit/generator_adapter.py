# -*- coding:utf-8 -*-
try:
    from collections.abc import Coroutine, Generator
except ImportError:
        from types import GeneratorType as Generator
        Coroutine = Generator


class Node(object):

    def __init__(self, coroutine, parent=None):
        self.coroutine = coroutine
        self.parent = parent
        self.children = list()

    def append(self, child):
        return self.children.append(child)

    def send(self, result):
        return self.coroutine.send(result)

    def remove(self, child):
        return self.children.remove(child)

    def throw(self, typ, val=None, tb=None):
        return self.coroutine.throw(typ, val, tb)

    def __await__(self):
        pass

    def __iter__(self):
        return self.coroutine


class GeneratorAdapter(object):
    """
        Generator适配器，用于兼容yield在python2,python3低版本和python3.3以后的版本使用
        使用方法：
        generator = GeneratorAdapter(generator)
        在python3.3以后的版本，正常使用yield from
        对于之前的版本，使用yield返回一个生成器的效果与yield from相同
        对于低版本中生成器中的return 关键字不能使用的问题，使用Return方法代替。
        对于高版本python,你甚至可以混写yield和yield from。没有任何区别
    """
    def __init__(self, root):
        self.current_node = Node(root)

    def send(self, result):
        try:
            yielded = self.current_node.send(result)
            # 如果yield值是生成器或者协程，则创建子节点并将当前结点指向子节点，并预激
            while isinstance(yielded, (Generator, Coroutine)):
                child = Node(yielded, self.current_node)
                self.current_node.append(child)
                self.current_node = child
                yielded = yielded.send(None)
            # 否则返回当前的yield值。
            return yielded
        except (StopIteration, GeneratorExit) as e:
            # 生成器完成后，如果存在父生成器，则删除当前生成器，切换到父生成器，将当前生成器的返回值发送给父生成器
            if self.current_node.parent:
                self.current_node.parent.remove(self.current_node)
                self.current_node = self.current_node.parent
                return self.send(e.args[0] if e.args else None)
            else:
                raise

    def throw(self, typ, val=None, tb=None):
        return self.current_node.throw(typ, val, tb)

    def __iter__(self):
        return iter(self.current_node)



def Return(val):
    raise StopIteration(val)