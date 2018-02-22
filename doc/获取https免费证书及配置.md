[comment]: <> (![](https://letsencrypt.org/images/howitworks_authorization.png))
# 获取免费证书

  * 克隆letsencrypt`git clone https://github.com/letsencrypt/letsencrypt`
  * 执行`cd letsencrypt &./letsencrypt-auto`
  * 按提示输入邮箱，域名，出现如下信息即成功生成证明和私钥

    
    
    IMPORTANT NOTES:
     - Unable to install the certificate
     - Congratulations! Your certificate and chain have been saved at:
       /etc/letsencrypt/live/mashichao.com/fullchain.pem
       Your key file has been saved at:
       /etc/letsencrypt/live/mashichao.com/privkey.pem
       Your cert will expire on 2018-05-01. To obtain a new or tweaked
       version of this certificate in the future, simply run
       letsencrypt-auto again with the "certonly" option. To
       non-interactively renew *all* of your certificates, run
       "letsencrypt-auto renew"
     - Your account credentials have been saved in your Certbot
       configuration directory at /etc/letsencrypt. You should make a
       secure backup of this folder now. This configuration directory will
       also contain certificates and private keys obtained by Certbot so
       making regular backups of this folder is ideal.
    

# 配置nginx

  * 修改nginx配置文件，添加如下信息

    
    
    server {
            listen       443 ssl;
            server_name    mashichao.com;
    
            ssl_certificate      /etc/letsencrypt/live/mashichao.com/fullchain.pem;
            ssl_certificate_key  /etc/letsencrypt/live/mashichao.com/privkey.pem;
    
            ssl_session_cache    shared:SSL:1m;
            ssl_session_timeout  5m;
    
            ssl_ciphers  HIGH:!aNULL:!MD5;
            ssl_prefer_server_ciphers  on;
    
        #静态文件，nginx自己处理
        location /static {
            alias /root/blog/static;
            #过期30天，静态文件不怎么更新，过期可以设大一点，如果频繁更新，则可以设置得小一点。
            expires 30d;
        }
        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:3031;
        }
    
    }
    

其中ssl_certificate指向证书，ssl_certificate_key指向私钥 \- 重启nginx完成


[comment]: <tags> (https,LetsEncrypt,nginx)
[comment]: <description> (使用Let’s Encrypt https的免费证书搭建nginx服务器)
[comment]: <title> (获取https免费证书及配置)
[comment]: <author> (夏洛之枫)