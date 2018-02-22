- 暂停程序
```
import pdb
pdb.set_trace()
```
- 打印当前版本Pdb可用的命令,会打印当前版本Pdb可用的命令，如果要查询某个命令，可以输入 h [command]，例如：“h l” — 查看list命令 
```
h(elp)
```
- 可以列出当前将要运行的代码块 
```
l(ist)
```
- 设置断点，例如 “b 77″，就是在当前脚本的77行打上断点，还能输入函数名作为参数，断点就打到具体的函数入口，如果只敲b，会显示现有的全部断点 
```
b(reak)
```
- 设置条件断点，下面语句就是对第4个断点加上条件“a==3” ，当条件满足时断点生效.
```
condition bpnumber [condition]
(Pdb) condition 4 a==3
(Pdb) b
Num Type Disp Enb Where
4 breakpoint keep yes at /home/jchen/regression/regressionLogCMP.py:504
stop only if a==3
```
- 如果后面带有参数，就是清除指定的断点（我在Python2.4上从来没成功过！！！）；如果不带参数就是清除所有的断点 
```
cl(ear)
(Pdb) cl
Clear all breaks? y
```
- 禁用/激活断点
```
 disable/enable
(Pdb) disable 3
(Pdb) b
Num Type Disp Enb Where
3 breakpoint keep no at /home/jchen/regression/regressionLogCMP.py:505
```
- 让程序运行下一行，如果当前语句有一个函数调用，用n是不会进入被调用的函数体中的 
```
n(ext)
```
- 跟n相似，但是如果当前有一个函数调用，那么s会进入被调用的函数体中 
```
s(tep)
```
- 让程序正常运行，直到遇到断点
```
c(ont(inue))
```
- 让程序跳转到指定的行数
```
j(ump) # 只能在同一个代码块中跳
(Pdb) j 497
> /home/jchen/regression/regressionLogCMP.py(497)compareLog()
-> pdb.set_trace()
```
- 打印当前函数的参数 
```
a(rgs)
(Pdb) a
_logger =
_base = ./base/MRM-8137.log
_new = ./new/MRM-8137.log
_caseid = 5550001
_toStepNum = 10
_cmpMap = {‘_bcmpbinarylog’: ‘True’, ‘_bcmpLog’: ‘True’, ‘_bcmpresp’: ‘True’}
```
- 最有用的命令之一，打印某个变量
```
(Pdb) p _new
u’./new/MRM-8137.log’
```
- 感叹号后面跟着语句，可以直接改变某个变量
```
(Pdb) !spider_item_field=3
(Pdb) p spider_item_field
3
```
- Print a stack trace, with the most recent frame at the bottom.An arrow indicates the "current frame", which determines the context of most commands. 'bt' is an alias for this command.
打印栈路径，最近的Frame在最底下，有一个>指向当前决定上下指令的Frame
```
(Pdb) w
  /usr/local/bin/scrapy(9)<module>()
-> load_entry_point('Scrapy==1.0.5', 'console_scripts', 'scrapy')()
  /usr/local/lib/python2.7/dist-packages/scrapy/cmdline.py(143)execute()
-> _run_print_help(parser, _run_command, cmd, args, opts)
  /usr/local/lib/python2.7/dist-packages/scrapy/cmdline.py(89)_run_print_help()
-> func(*a, **kw)
  /usr/local/lib/python2.7/dist-packages/scrapy/cmdline.py(150)_run_command()
-> cmd.run(args, opts)
  /usr/local/lib/python2.7/dist-packages/scrapy/commands/crawl.py(58)run()
-> self.crawler_process.start()
  /usr/local/lib/python2.7/dist-packages/scrapy/crawler.py(252)start()
-> reactor.run(installSignalHandlers=False)  # blocking call
  /usr/local/lib/python2.7/dist-packages/twisted/internet/base.py(1193)run()
-> self.mainLoop()
  /usr/local/lib/python2.7/dist-packages/twisted/internet/base.py(1202)mainLoop()
-> self.runUntilCurrent()
  /usr/local/lib/python2.7/dist-packages/twisted/internet/base.py(824)runUntilCurrent()
-> call.func(*call.args, **call.kw)
  /usr/local/lib/python2.7/dist-packages/twisted/internet/defer.py(401)callback()
-> self._startRunCallbacks(result)
  /usr/local/lib/python2.7/dist-packages/twisted/internet/defer.py(509)_startRunCallbacks()
-> self._runCallbacks()
  /usr/local/lib/python2.7/dist-packages/twisted/internet/defer.py(596)_runCallbacks()
-> current.result = callback(current.result, *args, **kw)
  /home/ubuntu/jay-cluster/webWalker/walker/spiders/exception_process.py(32)wrapper_method()
-> return func(*args, **kwds)
  /home/ubuntu/jay-cluster/crawling/spiders/amazon_spider.py(26)parse_item()
-> self.common_property(response, item)
> /home/ubuntu/jay-cluster/webWalker/walker/spiders/__init__.py(82)common_property()
-> while field:
```
- u ，Move the current frame one level up in the stack trace
(to an older frame).将当前frame向上移动一层
```
(Pdb) u
> /home/ubuntu/jay-cluster/crawling/spiders/amazon_spider.py(26)parse_item()
-> self.common_property(response, item)

```
- Move the current frame one level down in the stack trace
(to a newer frame).将当前frame向下移动一层
```
(Pdb) d
> /home/ubuntu/jay-cluster/webWalker/walker/spiders/__init__.py(82)common_property()
-> while field:

```
- 退出调试 
```
 q(uit)
```
参考资料[用PDB库调试Python程序](http://www.cnblogs.com/dkblog/archive/2010/12/07/1980682.html)
[comment]: <tags> (python,pdb)
[comment]: <description> (python使用pdb进行调试)
[comment]: <title> (python pdb使用方法)
[comment]: <author> (夏洛之枫)