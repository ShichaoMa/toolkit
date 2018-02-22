[comment]: <> (![](https://scottlinux.com/wp-content/uploads/2014/10/systemd_logo_small.jpeg))
### 一个简单的开机启动配置文件如下:

打开配置文件`vi /lib/systemd/system/deer.service`

    
    
    [Unit]
    # 描述
    Description=deplicate images
    # 在哪个程序之后启动
    After=network.target
    # 依赖哪个程序
    Wants=network.target
    [Service]
    Type=simple
    # 执行命令
    ExecStart=/home/longen/deer/image_process.py --host 192.168.200.94 --port 4567
    [Install]
    WantedBy=multi-user.target
    

参考资料: [systemd - Ubuntu Wiki](https://wiki.ubuntu.com/systemd)
[systemd.exec](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)


[comment]: <tags> (ubuntu,systemd)
[comment]: <description> (ubuntu systemd配置)
[comment]: <title> (ubuntu systemd配置)
[comment]: <author> (夏洛之枫)