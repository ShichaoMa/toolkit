[comment]: <> (![](https://core-electronics.com.au/media/kbase/raspberry-pi-workshop-cover.png))
### 使用 vi 编辑文件，增加下列配置项`vi /etc/dhcpcd.conf`

    
    
    # 指定接口 eth0
    interface eth0
    # 指定静态IP，/24表示子网掩码为 255.255.255.0
    static ip_address=192.168.1.20/24
    # 路由器/网关IP地址
    static routers=192.168.1.1
    # 手动自定义DNS服务器
    static domain_name_servers=114.114.114.114
    

### 修改完成后，按esc键后输入 :wq 保存。重启树莓派就生效了

    
    
    sudo reboot
    


[comment]: <tags> (raspberry)
[comment]: <description> (树莓派配置静态ip)
[comment]: <title> (树莓派手动指定静态IP和DNS)
[comment]: <author> (夏洛之枫)