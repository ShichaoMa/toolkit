## 安装

```
 sudo pip install shadowsocks
```

## 配置

### server

打开`/etc/shadowsocks.json` 加入以下代码：

```
{
    "server":"0.0.0.0",
    "server_port":8388,
    "local_address": "127.0.0.1",
    "local_port":1080,
    "password":"xxxxx",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open": false,
    "pid-file": "/root/shadowsocks/shadowsocks.pid",
    "log-file": "/root/shadowsocks/shadowsocks.log"

}
```

启动`ssserver -c /etc/shadowsocks.json -d start`

### client

- 创建配置文件

```
mkdir shadowsocks
cd shadowsocks/
vi shadowsocks.json
```

- 添加以下内容

```
{
  "server": "xxx.xxx.xxx.xxx",
  "server_port": 8388,
  "local_address": "127.0.0.1",
  "local_port": 1080,
  "password": "xxxxx",
  "timeout": 600,
  "method": "aes-256-cfb",
  "fast_open": false,
  "workers": 1,
  "pid-file": "/home/ubuntu/shadowsocks/shadowsocks.pid",
  "log-file": "/home/ubuntu/shadowsocks/shadowsocks.log"
}
```

启动`sslocal -c ~/shadowsocks/shadowsocks.json -d start`

## 配置http代理

- 安装 polipo

```
 sudo apt-get install polipo
```

- 配置polipo

```
vi /etc/polipo/config
```

- 添加以下内容

```
proxyAddress = "127.0.0.1"
proxyPort = "8123"
socksParentProxy = "127.0.0.1:1080"
socksProxyType = socks5
chunkHighMark = 50331648
objectHighMark = 16384
serverMaxSlots = 64
serverSlots = 16
serverSlots1 = 32
```

- 启动

```
sudo /etc/init.d/polipo restart
```
[comment]: <tags> (ubuntu,shadowsocks)
[comment]: <description> (shadowsocks在ubuntu上的安装方法)
[comment]: <title> (ubuntu安装ShadowSocks)
[comment]: <author> (夏洛之枫)