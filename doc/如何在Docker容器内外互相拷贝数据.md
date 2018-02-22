[comment]: <> (![](http://www.fimvisual.com/wp-content/uploads/2016/10/1003956-20160929094610156-2054520507.png))
#### 从容器内拷贝文件到主机上

    
    
    [root@oegw1 soft]# docker ps
    CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
    8d418a7b6021        postgres            "/docker-entrypoint.   7 hours ago         Up 7 hours                              test1    
    [root@oegw1 soft]# docker exec -t -i 8d418a7b6021 /bin/bash
    root@oegw1:/var/lib/postgresql# pwd
    /var/lib/postgresql
    root@oegw1:/var/lib/postgresql# ls
    data
    root@oegw1:/var/lib/postgresql# exit
    exit
    [root@oegw1 soft]# docker cp 8d418a7b6021:/var/lib/postgresql/data /opt/soft/
    

**完成拷贝**

#### 从主机上拷贝文件到容器内

    
    
    docker run -v /opt/soft:/mnt 8d418a7b6021
    

#### 用-v挂载主机数据卷到容器内,通过-v参数，冒号前为宿主机目录，必须为绝对路径，冒号后为镜像内挂载的路径。

    
    
    [root@oegw1 soft]# docker run -it -v /opt/soft:/mnt postgres /bin/bash
    

**这种方式的缺点是只能在容器刚刚启动的情况下进行挂载**


[comment]: <tags> (docker,copy)
[comment]: <description> (从docker中拷贝数据)
[comment]: <title> (如何在Docker容器内外互相拷贝数据)
[comment]: <author> (夏洛之枫)