[comment]: <> (![](http://unitedwebsoft.in/blog/wp-content/uploads/2017/06/ssh.jpg))
  * 生成公钥

    
    
    ssh-keygen
    

  * 复制到远程主机

    
    
    ssh-copy-id -i ~/.ssh/id_rsa.pub longen@192.168.200.80 -p 12016
    

参考[ 使用ssh-keygen和ssh-copy-id三步实现SSH无密码登录
](http://blog.chinaunix.net/uid-26284395-id-2949145.html)


[comment]: <tags> (ssh)
[comment]: <description> (ssh免密登录)
[comment]: <title> (SSH无密码登录)
[comment]: <author> (夏洛之枫)