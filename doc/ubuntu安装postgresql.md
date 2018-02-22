#### 安装
- 安装postgresql server 和 client：
    ```bash
    sudo apt-get install postgresql postgresql-contrib postgresql-client
    ```
#### 服务
- 启动数据库
```bash
    sudo /etc/init.d/postgresql start
```
- 查看数据库状态
```bash
sudo /etc/init.d/postgresql status
```
- 关闭数据库
```bash
sudo /etc/init.d/postgresql stop
```
- 重启数据库
```bash
sudo /etc/init.d/postgresql restart
```
#### 创建用户 
- 创建数据库用户 root，并指定其为超级用户：
```bash
sudo -u postgres createuser --superuser root
```
- 登录数据库控制台，设置 root 用户的密码，退出控制台
```bash
sudo -u postgres psql
\password root # 设置密码
\q
```
#### 创建数据库
- 创建 test 数据库，指定用户为 root：
```bash
sudo -u postgres createdb -O root test
```
- 登录数据库控制台, 修改数据库 test 为 star：
```bash
alter database test rename to star
```
- 也可以删除不需要的数据库，如：
```bash
sudo -u postgres dropdb test
```
#### 登录数据库
- 使用 psql 命令：
  - -U 指定用户
  - -d 指定数据库
  - -h 指定服务器
  - -p 指定端口。
```bash
psql -U root -d test -h 127.0.0.1 -p 5432
```
- 实际的使用中，我们创建用户名和数据库跟系统名称一样（系统认证），然后通过执行下面命令即可登录我们指定的数据库。

```bash
psql
```


- 也可以通过环境变量指定默认的数据库（test）：
```bash
export PGDATABASE=test
```
#### 常用控制台命令
```bash
\h：查看SQL命令的解释，比如\h select。
\?：查看psql命令列表。
\l：列出所有数据库。
\c [database_name]：连接其他数据库。
\d：列出当前数据库的所有表格。
\d [table_name]：列出某一张表格的结构。
\du：列出所有用户。
\e：打开文本编辑器。
\conninfo：列出当前数据库和连接的信息。
```
参考文献 [ubuntu 下 PostgreSQL 使用小记](http://wenzhixin.net.cn/2014/01/12/hello_postgresql)

参考文献 [How To Use PostgreSQL with Your Ruby on Rails Application on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-ruby-on-rails-application-on-ubuntu-14-04)
![](http://ericsaupe.com/wp-content/uploads/2014/07/install-postgresql-934-on-mac.png)
[comment]: <tags> (ubuntu,postgresql)
[comment]: <description> (在ubuntu上安装postgresql)
[comment]: <title> (ubuntu安装postgresql)
[comment]: <author> (夏洛之枫)