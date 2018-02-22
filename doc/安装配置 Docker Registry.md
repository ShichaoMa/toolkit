[comment]: <> (![](https://codefresh.io/wp-content/uploads/2016/12/compose_swarm.png))
# 安装配置 Docker Registry

## 创建目录

    
    
    $ mkdir ~/docker-registry && cd $_
    $ mkdir data
    

## 编写 docker-compose 文件

    
    
    $ cd ~/docker-registry
    $ vi docker-compose.yml
    

## 添加一下内容

    
    
    registry:
      image: registry:2
      restart: always
      ports:
        - 127.0.0.1:5000:5000
      environment:
        REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /data
      volumes:
        - ./data:/data
    

## 安装配置 nginx

    
    
    $ mkdir ~/docker-registry/nginx
    $ cd ~/docker-registry
    

## 修改 docker-compose.yml

    
    
    nginx:
      image: "nginx:1.9"
      ports:
        - 443:443
      links:
        - registry:registry
      volumes:
        - ./nginx/:/etc/nginx/conf.d
    registry:
      image: registry:2
      ports:
        - 127.0.0.1:5000:5000
      environment:
        REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /data
      volumes:
        - ./data:/data
    

## 创建 registry.conf

    
    
    $ vi ~/docker-registry/nginx/registry.conf
    # 添加一下内容
    upstream docker-registry {
      server registry:5000;
    }
    
    server {
      listen 443;
      server_name 192.168.200.150;
    
      # SSL
      # ssl on;
      # ssl_certificate /etc/nginx/conf.d/domain.crt;
      # ssl_certificate_key /etc/nginx/conf.d/domain.key;
    
      # disable any limits to avoid HTTP 413 for large image uploads
      client_max_body_size 0;
    
      # required to avoid HTTP 411: see Issue #1486 (https://github.com/docker/docker/issues/1486)
      chunked_transfer_encoding on;
    
      location /v2/ {
        # Do not allow connections from docker 1.5 and earlier
        # docker pre-1.6.0 did not properly set the user agent on ping, catch "Go *" user agents
        if ($http_user_agent ~ "^(docker\/1\.(3|4|5(?!\.[0-9]-dev))|Go ).*$" ) {
          return 404;
        }
    
        # To add basic authentication to v2 use auth_basic setting plus add_header
        # auth_basic "registry.localhost";
        # auth_basic_user_file /etc/nginx/conf.d/registry.password;
        # add_header 'Docker-Distribution-Api-Version' 'registry/2.0' always;
    
        proxy_pass                          http://docker-registry;
        proxy_set_header  Host              $http_host;   # required for docker client's sake
        proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
        proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
        proxy_read_timeout                  900;
      }
    }
    

修改 server_name 未内网ip，本例中是 192.168.200.150

## 配置 nginx SSL

修改 registry.conf, 去掉 SSL注释

    
    
      # SSL
      ssl on;
      ssl_certificate /etc/nginx/conf.d/domain.crt;
      ssl_certificate_key /etc/nginx/conf.d/domain.key;


## 创建CA
    

    $ cd ~/docker-registry/nginx

    
    
## 生成CA私钥
    

    $ openssl genrsa -out devdockerCA.key 2048

    
    
## 生成CA公钥
    

    $ openssl req -x509 -new -nodes -key devdockerCA.key -days 10000 -out devdockerCA.crt

    
    
## 创建服务器密钥
创建服务器私钥，在nginx配置sslcertificatekey时使用
    

    $ openssl genrsa -out domain.key 2048

    
    
## 拷贝 /etc/ssl/openssl.cnf 到 ~/docker-registry/nginx 目录，修改openssl 以下部分，
    

    req_extensions = v3_req [ v3_req ]

    # Extensions to add to a certificate request

    basicConstraints = CA:FALSE keyUsage = nonRepudiation, digitalSignature, keyEncipherment subjectAltName = IP: 192.168.200.150

    
    
## 创建服务器公钥，在nginx配置ssl_certificate时使用
    

    $ openssl req -new -key domain.key -out dev-docker-registry.com.csr -config openssl.cnf 

创建过程中，Common Name 输入 192.168.200.150

## 生成自签名证书

    
    
    $ openssl x509 -req -in dev-docker-registry.com.csr -CA devdockerCA.crt -CAkey devdockerCA.key -CAcreateserial -out domain.crt -days 10000  -extensions v3_req -extfile openssl.cnf
    

## 安装 docker 服务

    
    
    $ sudo apt-get install docker docker-compose
    $ sudo systemctl restart docker.service
    

## 测试 SSL

    
    
    $ cd ~/docker-registry
    $ docker-compose up
        # 如果上一条命令被墙了，可以给其加个代理
        sudo vi /lib/systemd/system/docker.service
        # 在[service]加上
        Environment="HTTP_PROXY=http://192.168.200.90:8123"
        sudo systemctl daemon-reload
        sudo systemctl restart docker
    

命令行测试 curl https://192.168.200.150/v2/, 输出为{}

## 客户端访问 registry

客户端添加CA， 拷贝 ~/docker-registry/nginx/devdockerCA.crt 内容， 在客户机新建

    
    
    $ sudo vi /usr/local/share/ca-certificates/docker-dev-cert/devdockerCA.crt
    

添加拷贝内容。

## 更新证书

    
    
    $ sudo update-ca-certificates
    

## 重启 docker 服务

    
    
    $ sudo systemctl restart docker
    

## 测试

    
    
    $ docker tag roc_web 192.168.200.150/longen/roc_web
    $ docker push 192.168.200.150/longen/roc_web
    


[comment]: <tags> (docker,repository)
[comment]: <description> (docker私有仓库配置方法)
[comment]: <title> (安装配置 Docker Registry)
[comment]: <author> (夏洛之枫)