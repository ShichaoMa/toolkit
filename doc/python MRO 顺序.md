[comment]: <> (![](https://binaykumarray.files.wordpress.com/2016/05/maxresdefault.jpg?w=772))
# python mro顺序
### 定义
#### MRO（Method Resolution Order）：方法解析顺序。
Python语言包含了很多优秀的特性，其中多重继承就是其中之一，但是多重继承会引发很多问题，比如二义性，Python中一切皆引用，这使得他不会像C++一样使用虚基类处理基类对象重复的问题，但是如果父类存在同名函数的时候还是会产生二义性，Python中处理这种问题的方法就是MRO。
python 查找基类方法的顺序是广度优先 对于这种情况

### 历史中的MRO
如果不想了解历史，只想知道现在的MRO可以直接看最后的C3算法，不过C3所解决的问题都是历史遗留问题，了解问题，才能解决问题，建议先看历史中MRO的演化。
Python2.2以前的版本：经典类（classic class）时代
经典类是一种没有继承的类，实例类型都是type类型，如果经典类被作为父类，子类调用父类的构造函数时会出错。
这时MRO的方法为DFS（深度优先搜索（子节点顺序：从左到右））。
```
Class A:   # 是没有继承任何父类的
    def __init__(self):
        print "这是经典类"
```

inspect.getmro（A）可以查看经典类的MRO顺序

```
import inspect
class D:
    pass
 
class C(D):
    pass
 
class B(D):
    pass
 
class A(B, C):
    pass
 
if __name__ == '__main__':
    print inspect.getmro(A)
    
>>  (<class __main__.A at 0x10e0e5530>, <class __main__.B at 0x10e0e54c8>, <class __main__.D at 0x10e0e53f8>, <class __main__.C at 0x10e0e5460>)
```

MRO的DFS顺序如下图：

![](http://jbcdn2.b0.upaiyun.com/2016/07/67b3fe6d97b5882482cc0ca65cec6154.jpg)

#### 两种继承模式在DFS下的优缺点。
- 第一种，我称为正常继承模式，两个互不相关的类的多继承，这种情况DFS顺序正常，不会引起任何问题；

- 第二种，棱形继承模式，存在公共父类（D）的多继承（有种D字一族的感觉），这种情况下DFS必定经过公共父类（D），这时候想想，如果这个公共父类（D）有一些初始化属性或者方法，但是子类（C）又重写了这些属性或者方法，那么按照DFS顺序必定是会先找到D的属性或方法，那么C的属性或者方法将永远访问不到，导致C只能继承无法重写（override）。这也就是为什么新式类不使用DFS的原因，因为他们都有一个公共的祖先object。

### Python2.2版本：新式类（new-style class）诞生
为了使类和内置类型更加统一，引入了新式类。新式类的每个类都继承于一个基类，可以是自定义类或者其它类，默认承于object。子类可以调用父类的构造函数。

这时有两种MRO的方法
- 如果是经典类MRO为DFS（深度优先搜索（子节点顺序：从左到右））。
- 如果是新式类MRO为BFS（广度优先搜索（子节点顺序：从左到右））。

```
Class A(object):   # 继承于object
    def __init__(self):
        print "这是新式类"
```

A.__mro__ 可以查看新式类的顺序

MRO的BFS顺序如下图：

![](http://jbcdn2.b0.upaiyun.com/2016/07/21afdb3877fde91f7d5fad9a834aa347.jpg)

#### 两种继承模式在BFS下的优缺点。
第一种，正常继承模式，看起来正常，不过实际上感觉很别扭，比如B明明继承了D的某个属性（假设为foo），C中也实现了这个属性foo，那么BFS明明先访问B然后再去访问C，但是为什么foo这个属性会是C？这种应该先从B和B的父类开始找的顺序，我们称之为单调性。

第二种，棱形继承模式，这种模式下面，BFS的查找顺序虽然解了DFS顺序下面的棱形问题，但是它也是违背了查找的单调性。

因为违背了单调性，所以BFS方法只在Python2.2中出现了，在其后版本中用C3算法取代了BFS。

### Python2.3到Python2.7：经典类、新式类和平发展
因为之前的BFS存在较大的问题，所以从Python2.3开始新式类的MRO取而代之的是C3算法，我们可以知道C3算法肯定解决了单调性问题，和只能继承无法重写的问题。C3算法具体实现稍后讲解。

MRO的C3算法顺序如下图：看起简直是DFS和BFS的合体有木有。但是仅仅是看起来像而已。

![](http://jbcdn2.b0.upaiyun.com/2016/07/833725a0528db39994b79d7ced58cf65.jpg)

### Python3到至今：新式类一统江湖
Python3开始就只存在新式类了，采用的MRO也依旧是C3算法。

### 神奇的算法C3

判断mro要先确定一个线性序列，然后查找路径由由序列中类的顺序决定。所以C3算法就是生成一个线性序列。
如果继承至一个基类:
class B(A)
这时B的mro序列为[B,A]

如果继承至多个基类
class B(A1,A2,A3 ...)
这时B的mro序列 mro(B) = [B] + merge(mro(A1), mro(A2), mro(A3) ..., [A1,A2,A3])
merge操作就是C3算法的核心。
遍历执行merge操作的序列，如果一个序列的第一个元素，只出现在其他任何序列中的第一个元素，或者不在其他任何序列出现，则从所有执行merge操作序列中删除这个元素，合并到当前的mro中。
merge操作后的序列，继续执行merge操作，直到merge操作的序列为空。
如果merge操作的序列无法为空，则说明不合法。

例子：
```
class A(O):pass
class B(O):pass
class C(O):pass
class E(A,B):pass
class F(B,C):pass
class G(E,F):pass
```

A、B、C都继承至一个基类，所以mro序列依次为[A,O]、[B,O]、[C,O]
mro(E) = [E] + merge(mro(A), mro(B), [A,B])
       = [E] + merge([A,O], [B,O], [A,B])
执行merge操作的序列为[A,O]、[B,O]、[A,B]
A是序列[A,O]中的第一个元素，在序列[B,O]中不出现，在序列[A,B]中也是第一个元素，所以从执行merge操作的序列([A,O]、[B,O]、[A,B])中删除A，合并到当前mro，[E]中。
mro(E) = [E,A] + merge([O], [B,O], [B])
再执行merge操作，O是序列[O]中的第一个元素，但O在序列[B,O]中出现并且不是其中第一个元素。继续查看[B,O]的第一个元素B，B满足条件，所以从执行merge操作的序列中删除B，合并到[E, A]中。
mro(E) = [E,A,B] + merge([O], [O])
       = [E,A,B,O]

#### 实现C3算法的代码

```
def mro_C3(*cls):  
        if len(cls)==1:  
            if not cls[0].__bases__:  
                return  cls  
            else:  
                return cls+ mro_C3(*cls[0].__bases__)  
        else:  
            seqs = [list(mro_C3(C)) for C in cls ] +[list(cls)]  
            res = []  
            while True:  
              non_empty = list(filter(None, seqs))  
              if not non_empty:  
                  return tuple(res)  
              for seq in non_empty:  
                  candidate = seq[0]  
                  not_head = [s for s in non_empty if candidate in s[1:]]  
                  if not_head:  
                      candidate = None  
                  else:  
                      break  
              if not candidate:  
                  raise TypeError("inconsistent hierarchy, no C3 MRO is possible")  
              res.append(candidate)  
              for seq in non_empty:  
                  if seq[0] == candidate:  
                      del seq[0]  
```

#### C3算法反例

```
class Player:
    pass

class Enemy(Player):
    pass

class GameObject(Player, Enemy):
    pass
```

会提示

```
TypeError: Cannot create a consistent method resolution
order (MRO) for bases Player, Enemy
```

原因如下：Player和Enemy的mro依次为[Player, object], [Enemy, Player, object]
mro(GameObject) = [GameObject] + merge(mro(Enemy), mro(Player), [Player,Enemy])
= [GameObject] + merge([Player, object], [Enemy, Player, object], [Player,Enemy])
Player是merge中第一序列的第一位，而Play存在于第二个于第二个序列中且不是第一位，违反了C3算法规则,所以不允许这么做。

参考资料

[TypeError: Cannot create a consistent method resolution order
(MRO)](https://stackoverflow.com/questions/29214888/typeerror-cannot-create-a
-consistent-method-resolution-order-mro)

[你真的理解Python中MRO算法吗？](http://python.jobbole.com/85685/)

[python多重继承新算法C3](https://www.cnblogs.com/mingaixin/archive/2013/01/31/2887190.html)


[comment]: <tags> (mro,python)
[comment]: <description> (python中多继承方法的查找顺序)
[comment]: <title> (python MRO 顺序)
[comment]: <author> (夏洛之枫)