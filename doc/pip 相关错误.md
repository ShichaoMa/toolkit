## 操作系统语言引起的错误
```
export LC_ALL=C
```
## How do I fix 'ImportError: cannot import name IncompleteRead'?
```
# 重新安装pip
sudo apt-get remove python-pip
sudo easy_install pip
```

## UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 52: ordinal not in range(128)
```
修改操作系统的字符集
export LC_ALL=en_US.UTF-8
若出错bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
则
locale-gen  en_US.UTF-8
```
[comment]: <tags> (pip)
[comment]: <description> (pip相关错误)
[comment]: <title> (pip 相关错误)
[comment]: <author> (夏洛之枫)