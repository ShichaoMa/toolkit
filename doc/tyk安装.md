# 使用docker部署
## Set up hosts entries
    sudo vi /etc/hosts
    # 添加如下内容
    127.0.0.1    www.tyk-portal-test.com
## Get the quick start compose files
    git clone https://github.com/lonelycode/tyk_quickstart.git
    cd tyk_quickstart
## Add dashboard license
    vi tyk_analytics.conf
    # 修改如下内容
    {
    ...
    "mongo_url": "mongodb://mongo:27017/tyk_analytics",
    "license_key": "LICENSEKEY",
    "page_size": 10,
    ...
    }
licensekey可以从这个页面得到[Tyk On-Premises – FREE Community Edition License](https://tyk.io/product/tyk-professional-edition-free-trial/)
## Bootstrap dashboard and portal
    # docker-compose如果运行没成功考虑是版本问题，需要重装
    docker-compose up -d --force-recreate
        # 如果上一条命令被墙了，可以给其加个代理
        sudo vi /lib/systemd/system/docker.service
        # 在[service]加上
        Environment="HTTP_PROXY=http://192.168.200.90:8123"
        sudo systemctl daemon-reload
        sudo systemctl restart docker
    
    ./setup.sh
## Log in
The setup script will provide login details for your Dashboard – go ahead and log in.
[comment]: <tags> (tyk,apigateway)
[comment]: <description> (Tyk is an open source API Gateway that is fast, scalable and modern. Out of the box, Tyk offers an API Management Platform with an API Gateway, API Analytics, Developer Portal and API Management Dashboard.)
[comment]: <title> (tyk安装)
[comment]: <author> (夏洛之枫)