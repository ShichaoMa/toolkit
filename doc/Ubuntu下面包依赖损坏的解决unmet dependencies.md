[comment]: <picture> (![](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1517125379&di=9a91536e804ca5a63efa8c661784bc1f&imgtype=jpg&er=1&src=http%3A%2F%2Fpic1.win4000.com%2Fwallpaper%2F4%2F53a795c66d5ae.jpg))
如下错误

    
    
    $ sudo apt-get install libjack0
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    You might want to run 'apt-get -f install' to correct these:
    The following packages have unmet dependencies:
     libbluetooth-dev : Depends: libbluetooth3 (= 4.101-0ubuntu13.1) but 4.101.1-0indt2 is to be installed
     libjack-jackd2-0 : Conflicts: libjack-0.116
                        Conflicts: libjack0 but 1:0.121.3+20120418git75e3e20b-2.1ubuntu1 is to be installed
     libjack-jackd2-0:i386 : Conflicts: libjack-0.116
                             Conflicts: libjack0 but 1:0.121.3+20120418git75e3e20b-2.1ubuntu1 is to be installed
     libjack0 : Conflicts: libjack-0.116
                Conflicts: libjack-0.116:i386
     libpulse-dev : Depends: libpulse0 (= 1:4.0-0ubuntu11.1) but 1:4.0-0ubuntu11indt2 is to be installed
     libpulse0 : Breaks: libpulse0:i386 (!= 1:4.0-0ubuntu11indt2) but 1:4.0-0ubuntu11.1 is to be installed
     libpulse0:i386 : Breaks: libpulse0 (!= 1:4.0-0ubuntu11.1) but 1:4.0-0ubuntu11indt2 is to be installed
     pulseaudio : Depends: libpulse0 (= 1:4.0-0ubuntu11.1) but 1:4.0-0ubuntu11indt2 is to be installed
    E: Unmet dependencies. Try 'apt-get -f install' with no packages (or specify a solution).
    

解决方法: `apt-get -f install`

如遇到空间不足，证明/boot满了 这时使用`dpkg --get-selections|grep linux`可以查看内核 想删除过期内核是不可能的，
因为没有依赖问题还没有解决。而解决依赖又需要空间，所以貌似死循环了 不过，可以通过将/boot目录下initrd和vmlinuz打头的文件暂时转移来腾空间。
然后运行`apt-get -f install`和`apt-get remove -y 内核名`

参考资料

[Ubuntu下面包依赖损坏的解决unmet
dependencies](http://blog.csdn.net/sy373466062/article/details/53991413)

[ubuntu boot空间不足的解决方法](http://blog.csdn.net/yypony/article/details/17260153)

[Linux学习笔记：解决因 /boot
分区空间不足导致的卸载旧内核失败](http://blog.csdn.net/cloud_xy/article/details/10278769)


[comment]: <tags> (ubuntu)
[comment]: <description> (Ubuntu下面包依赖损坏的解决unmet dependencies)
[comment]: <title> (Ubuntu下面包依赖损坏的解决unmet dependencies)
[comment]: <author> (夏洛之枫)