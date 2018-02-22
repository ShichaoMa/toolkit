# 修改配置文件
```
vi /var/lib/pgsql/data/postgresql.conf

listen_addresses = '*'

vi /var/lib/pgsql/data/pg_hba.conf

Include the following line (at the end of the file):

host    username    all         192.168.0.10/32     md5
```
# 重启
```
sudo /etc/init.d/postgresql restart
/usr/lib/postgresql/9.5/bin/pg_ctl reload
```
参考资料

[Configure PostgreSQL to accept connections from network](https://www.faqforge.com/linux/server/postgresql/configure-postgresql-accept-connections/)

[PostgreSQL pg_hba.conf 文件简析](http://www.cnblogs.com/hiloves/archive/2011/08/20/2147043.html)

## 当使用pg_ctl reload的时候报错：
```
- pg_ctl: could not open PID file "/var/lib/postgresql/9.4/main/postmaster.pid": Permission denied
```
## 解决方法
```
sudo -u postgres /usr/lib/postgresql/9.4/bin/pg_ctl -D /var/lib/postgresql/9.4/main/ reload
```
错误原因可能是因为pg_ctl必须使用postgres用户来运行

参考资料

[What should the permissions be on for PostgreSQL /data files?](http://serverfault.com/questions/605493/what-should-the-permissions-be-on-for-postgresql-data-files)

## 重启时出现错误
```
longen@ubuntu-94:~$ sudo -u postgres /usr/lib/postgresql/9.5/bin/pg_ctl -D /var/lib/postgresql/9.5/main/ reload
sudo: unable to resolve host ubuntu-94
```
## 解决方法
修改hosts文件,增加对应关系
```
sudo vi /etc/hosts
192.168.200.94  ubuntu-94
```
[comment]: <tags> (postgresql)
[comment]: <description> (postgresql网络配置方法)
[comment]: <title> (postgresql network设置)
[comment]: <author> (夏洛之枫)