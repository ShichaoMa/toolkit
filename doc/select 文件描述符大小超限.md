[comment]: <> (![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR20CBKvtHnghLhQvx55PB5w8NOBnB7hLiHWsVGruQcjBcMD03e))
python调用select时出现如下错误

    
    
    Traceback (most recent call last):
      File "./offer_listing_monitor.py", line 161, in start
        readable, writable, _ = select.select(readable, self.clients.keys(), self.clients.keys(), 0.1)
    ValueError: filedescriptor out of range in select()
    

因为大量使用短链接，所以导致单进程的 fd 个数升高，超出了 1024 限制，出现了最开始的异常

### 解决方法

  * 因为这个值是定义在内核里面，所以如果在维持目前方案不变的前提下，解决这个问题就需要重新编译 Linux-kernel，将这个值提高
  * 修改 stpclient 的客户端，使用epoll，代替比较老旧的 select，当时使用 select 的原因是，fd 个数很少，性能上没有问题，同时 select 在其他平台上也可以得到支持

参考资料[Filedescriptor out of range in
select](http://www.jianshu.com/p/a74a48a54fce)


[comment]: <tags> (select)
[comment]: <description> (因为大量使用短链接，所以导致单进程的 fd 个数升高，超出了 1024 限制，出现了最开始的异常)
[comment]: <title> (select 文件描述符大小超限)
[comment]: <author> (夏洛之枫)