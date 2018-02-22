[comment]: <> (![](https://gss3.bdstatic.com/-Po3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike116%2C5%2C5%2C116%2C38/sign=e2eeaaa6b4fd5266b3263446ca71fc4e/024f78f0f736afc31a149928b119ebc4b7451266.jpg)
)
## ubuntu 安装 imagemagick
### 树莓派 安装 imagemagick
- 更换源
```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo nano /etc/apt/sources.list
# 注释掉之前的，添加
deb http://mirrors.aliyun.com/raspbian/raspbian/ wheezy main non-free contrib
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ wheezy main non-free contrib
# CTRL+X Y enter保存
sudo apt-get update && apt-get upgrade -y 
```
- 安装
```
 sudo  apt-get install imagemagick
```
- 使用convert进行图片转换

## 获取ip
```
ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'
```
## 挂nas
```
sudo apt-get install nfs-common
sudo mount -t nfs -o rw 192.168.200.89:/volume1/LINUXNFS /mnt/nas
```
## 开启vpn
```
sudo apt-get install pptp-linux
sudo pptpsetup --create vpn1 --server 58.96.182.136 --username derek --password luoding123 --encrypt --start
sudo route add default dev ppp0
```
## 查看dns解析
```
nslookup
```

## 查看端口占用情况
```
netstat -tln|grep 9999
lsof -i:9999
```
## 查看服务状态
```
sudo systemctl status
sudo systemctl status postgresql
# or
sudo service postgresql status
```
## 搜索目录包含指定字符的行
```
find . -name "*.py"|xargs grep Logger
```
## 高级搜索
```
# 先搜索当前目录下的2级目标，将结果排序后，使用parallel并行10个进程执行find搜索
find . -type d -maxdepth 2 | sort | parallel -t -P +10 "find {} -type f -regex '[^_]*\.jpg' > /Users/derek/nfs/{//}_{/}.list"

```

## 查看文件行数
```
wc -l
# 多文件
wc -ml
```

## top 查看linux性能
参考资料：[Linux Top 命令解析 比较详细](http://www.jb51.net/LINUXjishu/34604.html)

## systemctl使用
```
systemctl restart postgresql
# 查看所有服务
systemctl list-unit-files
```

## tar
```
-c: 建立压缩档案
-x：解压
-t：查看内容
-r：向压缩归档文件末尾追加文件
-u：更新原压缩包中的文件
```
这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。
```
-z：有gzip属性的
-j：有bz2属性的
-Z：有compress属性的
-v：显示所有过程
-O：将文件解开到标准输出
```
下面的参数-f是必须的
```
-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。

# 这条命令是将所有.jpg的文件打成一个名为all.tar的包。-c是表示产生新的包，-f指定包的文件名。
tar -cf all.tar *.jpg
# 这条命令是将所有.gif的文件增加到all.tar的包里面去。-r是表示增加文件的意思。
tar -rf all.tar *.gif
# 这条命令是更新原来tar包all.tar中logo.gif文件，-u是表示更新文件的意思。
tar -uf all.tar logo.gif
# 这条命令是列出all.tar包中所有文件，-t是列出文件的意思
tar -tf all.tar
# 这条命令是解出all.tar包中所有文件，-t是解开的意思
tar -xf all.tar
```
## 压缩
```
tar -cvf jpg.tar *.jpg //将目录里所有jpg文件打包成tar.jpg 

tar -czf jpg.tar.gz *.jpg   //将目录里所有jpg文件打包成jpg.tar后，并且将其用gzip压缩，生成一个gzip压缩过的包，命名为jpg.tar.gz

 tar -cjf jpg.tar.bz2 *.jpg //将目录里所有jpg文件打包成jpg.tar后，并且将其用bzip2压缩，生成一个bzip2压缩过的包，命名为jpg.tar.bz2

tar -cZf jpg.tar.Z *.jpg   //将目录里所有jpg文件打包成jpg.tar后，并且将其用compress压缩，生成一个umcompress压缩过的包，命名为jpg.tar.Z

rar a jpg.rar *.jpg //rar格式的压缩，需要先下载rar for linux

zip jpg.zip *.jpg //zip格式的压缩，需要先下载zip for linux
```
## 解压
```
tar -xvf file.tar //解压 tar包

tar -xzvf file.tar.gz //解压tar.gz

tar -xjvf file.tar.bz2   //解压 tar.bz2

tar -xZvf file.tar.Z   //解压tar.Z

unrar e file.rar //解压rar

unzip file.zip //解压zip
```
## 总结
```
1、*.tar 用 tar -xvf 解压

2、*.gz 用 gzip -d或者gunzip 解压

3、*.tar.gz和*.tgz 用 tar -xzf 解压

4、*.bz2 用 bzip2 -d或者用bunzip2 解压

5、*.tar.bz2用tar -xjf 解压

6、*.Z 用 uncompress 解压

7、*.tar.Z 用tar -xZf 解压

8、*.rar 用 unrar e解压

9、*.zip 用 unzip 解压

```

## 使用curl通过Get请求获取响应体同时获取响应码

```
curl -o - -s -w "%{http_code}\n" http://www.example.com/
```
[comment]: <tags> (ubuntu)
[comment]: <description> (常用命令)
[comment]: <title> (常用ubuntu指令)
[comment]: <author> (夏洛之枫)