[comment]: <> (![](http://s7.51cto.com/wyfs02/M01/74/4B/wKiom1YYf-qD2aXaAAQQhNGfnwc576.jpg-wh_651x-s_1733757554.jpg))
#### 创建rails应用
- 在根目录创建项目，使用-d postgresql 来声明使用postgresql作为数据库
```bash
cd ~
rails new star -d postgresql
```
- 然后进入应用目录
```bash
cd star
```
- 接下来配置应用数据库连接
#### 配置数据库连接
- 打开数据库配置文件
```bash
vi config/database.yml
```
- 在default片断下，找到pool: 5那一行，在其下方添加如下信息：
```bash
host: localhost
username: star
password:star
```
#### 创建应用数据库
- 使用rake命令创建development和test数据库
```bash
rake db:create
```
- 之后会生成两个数据库star_test和star_development
#### 测试配置
- 用来测试你的程序是正确使用了postgresql最简单的方式是尝试运行你的程序，例如运行默认开发环境，使用如下命令：
```bash
rails server
```
- 这会在http://localhost:3000启动的rails程序
- 如果你的程序在一个远程主机上，而且打算过一个web浏览器去访问它，那么最简单的方式就是绑定服务器的公共ip
```bash
rails server --binding=192.168.200.58
```

参考文献[How To Use PostgreSQL with Your Ruby on Rails Application on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-ruby-on-rails-application-on-ubuntu-14-04)

[comment]: <tags> (postgresql,ruby,rails,ubuntu)
[comment]: <description> (postgresql在ubuntu上配置rails的方法)
[comment]: <title> (PostgreSQL with Your Ruby on Rails Application on Ubuntu 14.04)
[comment]: <author> (夏洛之枫)