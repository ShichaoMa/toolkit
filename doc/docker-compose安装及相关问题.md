[comment]: <> (![](http://res.cloudinary.com/blog-mornati-net/image/upload/v1472668207/sz9sfwiji9foh0cv1v5p.png))
## 问题描述

    
    
    Unsupported config option for services service: 'tyk_mongo'
    

## 配置信息如下：

    
    
    version: '2'
    
    services:
        tyk_redis:
            image: redis:latest
            hostname: redis
            ports:
                - "6379:6379"
            networks:
                gateway:
                    aliases:
                        - redis
        tyk_mongo:
            image: mongo:latest
            command: ["mongod", "--smallfiles"]
            hostname: mongo
            ports:
                - "27017:27017"
            networks:
                gateway:
                    aliases:
                        - mongo
    

原因是因为docker-compose不支持version '2'， 重新安装新版本

# 安装

    
    
    sudo -i curl -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version
    


[comment]: <tags> (docker compose)
[comment]: <description> (docker-compose使用过程中可能遇到的问题汇总)
[comment]: <title> (docker-compose安装及相关问题)
[comment]: <author> (夏洛之枫)