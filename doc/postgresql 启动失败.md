在ubuntu操作系统下通过 /etc/init.d/postgresql start 启动postgresql服务时，启动，关闭，状态均显示正常，但是ps -ef|grep postgresql   或进程号，却找不到进程，很怪异的错误
通过查log
```
tail -f /var/log/postgresql/postgresql-9.4-main.log
```
发现以下错误：
```
2016-11-09 14:32:52 CST [2669-1] FATAL:  data directory "/var/lib/postgresql/9.4/main" has group or world access
2016-11-09 14:32:52 CST [2669-2] DETAIL:  Permissions should be u=rwx (0700).

```
原来postgresql 不允许将数据存放目录开放最大权限， 改回0700即正常
```
sudo chmod -R 0700 /var/lib/postgresql/9.4/main
```
[comment]: <tags> (postgresql)
[comment]: <description> (postgresql启动失败的解决方法)
[comment]: <title> (postgresql 启动失败)
[comment]: <author> (夏洛之枫)