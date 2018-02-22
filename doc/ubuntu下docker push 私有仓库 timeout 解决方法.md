[comment]: <> (![](https://cdn-images-1.medium.com/max/1600/1*sGHbxxLdm87_n7tKQS3EUg.png))
### push 的时候出现如下异常：

    
    
    ubuntu@dev:~$ docker push 192.168.200.90/kong
    The push refers to a repository [192.168.200.90/kong]
      Get https://192.168.200.90/v1/_ping: net/http: TLS handshake timeout
    

### 可能是因为docker使用了外网代理

    
    
    ubuntu@dev:~$ cat /lib/systemd/system/docker.service
    [Unit]
    Description=Docker Application Container Engine
    Documentation=https://docs.docker.com
    After=network.target docker.socket
    Requires=docker.socket
    
    [Service]
    Environment="HTTP_PROXY=http://192.168.200.90:8123"
    Type=notify
    # the default is not to use systemd for cgroups because the delegate issues still
    # exists and systemd currently does not support the cgroup feature set required
    # for containers run by docker
    ExecStart=/usr/bin/dockerd -H fd://
    ExecReload=/bin/kill -s HUP $MAINPID
    # Having non-zero Limit*s causes performance problems due to accounting overhead
    # in the kernel. We recommend using cgroups to do container-local accounting.
    LimitNOFILE=infinity
    LimitNPROC=infinity
    LimitCORE=infinity
    # Uncomment TasksMax if your systemd version supports it.
    # Only systemd 226 and above support this version.
    #TasksMax=infinity
    TimeoutStartSec=0
    # set delegate yes so that systemd does not reset the cgroups of docker containers
    Delegate=yes
    # kill only the docker process, not all processes in the cgroup
    KillMode=process
    
    # 注释掉Environment="HTTP_PROXY=http://192.168.200.90:8123"
    # Environment="HTTP_PROXY=http://192.168.200.90:8123"
    


[comment]: <tags> (docker,repository)
[comment]: <description> (dcoker私有仓库)
[comment]: <title> (ubuntu下docker push 私有仓库 timeout 解决方法)
[comment]: <author> (夏洛之枫)