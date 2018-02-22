[comment]: <> (![](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1506771469861&di=9d8060746c999dea15db06bb3d93e453&imgtype=0&src=http%3A%2F%2Fwww.xunzai.com%2Fdata%2Fupload%2F201506%2F201506%2F14343615147677.png))
  * 去 [WinRAR and RAR archiver downloads](http://www.rarlab.com/download.htm)下载 rarosx 
  * 在Mac OS X系统中默认不支持 RAR 文件的解压缩。下面演示如何在Mac OS X系统中使用 rar 命令行操作。 
  * 首先从rarlab 网站下载 rar／unrar 工具； 
  * 解压缩下载的 tar.gz 压缩包`tar xvf rarosx-5.2.0.tar.gz`，在下载目录Downloads下自动创建一个rar的目录，其中有rar ／ unrar 文件； 
  * 进入终端（命令窗口 `control＋空格`） 
  * 进入刚刚解压缩的rar 目录，使用 `cd Downloads/rar` 进入； 
  * 使用如下命令分别安装 `unrar` 和 `rar` 命令； 
  * 安装unrar命令：`sudo install -c -oUSERunrar/bin`安装rar命令：`sudoinstall−c−oUSER rar /bin`
  * 测试 `unrar` 和 `rar` 命令； 
  * 解压命令：`unrar x compressed-package.rar`
  * 解压缩 `xxx.rar` 压缩包，如果文件名有空格，则需要使用单引号包起来 如：`'xxx xx.rar'`


[comment]: <tags> (mac,rar)
[comment]: <description> (在mac上解压rar压缩包)
[comment]: <title> (在mac上解压rar压缩包)
[comment]: <author> (夏洛之枫)