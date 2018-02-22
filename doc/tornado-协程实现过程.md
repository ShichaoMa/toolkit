以一个简单的调用为例来说明
```
import tornado.ioloop
from tornado.gen import coroutine
from tornado.concurrent import Future

@coroutine
def asyn_sum(a, b):
    print("begin calculate:sum %d+%d"%(a,b))
    future = Future()

    def callback(a, b):
        print("calculating the sum of %d+%d:"%(a,b))
        future.set_result(a+b)
    tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)

    result = yield future

    print("after yielded")
    print("the %d+%d=%d"%(a, b, result))

def main():
    future = asyn_sum(2,3)
    tornado.ioloop.IOLoop.instance().start()


main()

```
- 程序开始，定义了一个asyn_sum协程，在main函数中第一行调用了该协程
- 同时tornado.gen.coroutine中调用asyn_sum生成器，获取第一个yield值也就是future，并创建了一个Runner对象
```
try:
    orig_stack_contexts = stack_context._state.contexts
    yielded = next(result) # 这一行所示
    if stack_context._state.contexts is not orig_stack_contexts:
        yielded = TracebackFuture()
        yielded.set_exception(
            stack_context.StackContextInconsistentError(
                'stack_context inconsistency (probably caused '
                'by yield within a "with StackContext" block)'))
except (StopIteration, Return) as e:
    future.set_result(_value_from_stopiteration(e))
except Exception:
    future.set_exc_info(sys.exc_info())
else:
    _futures_to_runners[future] = Runner(result, future, yielded)
```
- Runner通过__init__调用了其方法handle_yield，并在检查future的完成情况，很明显在第一个代码块中`tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)`刚被加入事件循环，此时事件循环还未启动，所以callback中的`future.set_result(a+b)`并未被调用，因此future并未done。
```
if not self.future.done() or self.future is moment:
    def inner(f):
        # Break a reference cycle to speed GC.
        f = None # noqa
        self.run()
    self.io_loop.add_future(
        self.future, inner)
    return False
return True
```
- 让我们把注意力移到`self.io_loop.add_future(self.future, inner)`这么代码中，这么代码将inner在future完成之后加入到了事件循环的callbacks中，由下面的代码可以的看出
```
def add_future(self, future, callback):
    """Schedules a callback on the ``IOLoop`` when the given
    `.Future` is finished.
    The callback is invoked with one argument, the
    `.Future`.
    """
    assert is_future(future)
    callback = stack_context.wrap(callback)
    future.add_done_callback(
        lambda future: self.add_callback(callback, future))
```
- future在开启事件循环后马上就会完成，因此，随后就会调用`self.add_callback(callback, future)`这段代码将inner加入事件循环，继而调用了` self.run()`
- run会获取future的结果，同时发送结果给协程
```
orig_stack_contexts = stack_context._state.contexts
exc_info = None
try:
    value = future.result()
except Exception:
    self.had_exception = True
    exc_info = sys.exc_info()
future = None
if exc_info is not None:
    try:
        yielded = self.gen.throw(*exc_info)
    finally:
        # Break up a reference to itself
        # for faster GC on CPython.
        exc_info = None
else:
    yielded = self.gen.send(value)
```
- 相应的，结果就被赋值给了main中的`result = yield future`，继而结束了整个协程的调用。

#### 对于事件循环的理解
tornado中的事件循环，本质上使用epoll实现。epoll的最主要作用可能就是为了唤醒事件循环。实现方式就是创建一个管道，通过epoll监听管道输出（READ）,并设置了超时时间，此时epoll会在超时时间内阻塞，如果有callback加入。则通过管道写入任意字节唤醒epoll，这样就相当于实现了一个可唤醒的阻塞。唤醒之后，会依次执行callback。同时执行timeouts中的callback，timeouts使用堆来保证时间最近的在最上面。

#### 对于future对象的理解
future对象可以当成一次异步调用的代理人，异步调用在创建后，加入事件循环中。随着事件循环进行，异步调用被执行了，执行一结束，代理人马上获取结果，并置done=True，同时代理人会将异步调用后的全部回调函数执行，其中的一个回调函数就包括Runner.run，其作用是将异步调用结果赋值给yield左边的变量，同时继续执行接下来的代码，直到下一个yield出现。

#### 对嵌套协程的调用
首先要清楚子协程返回的也一个future对象，因为这个future还没有完成，返回对于yield左边的变量会阻塞住。当子协程完成时，通过raise Return或者StopIteration的方式通过一个异常来将结果值传递出来，并为result_future也就是子协程的future进行set_result，子协程future完成后，父协程继续。
python3.4以后，可能过yield from也就是新版的await来更容易的获取子协程的返回值。

### 总结
对于`a = yield b`这种结构。b是一个Future，那么a的最终结果值为Future.result()，对于b，若是一个生成器，将其变成协程的方法只是实现了操控生成器在返回一个Future对象的同时，将生成器中每次yield都变成异步执行。

[comment]: <tags> (tornado)
[comment]: <description> (tornado协程实现)
[comment]: <title> (tornado-协程实现过程)
[comment]: <author> (夏洛之枫)