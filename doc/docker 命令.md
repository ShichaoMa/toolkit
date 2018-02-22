[Docker容器内不能联网的6种解决方案](http://blog.csdn.net/yangzhenping/article/details/43567155)
```
sudo docker network create simple-network
```
- 根据dockerfile生成镜像
```
sudo docker build -f scrapydockerfile_python3 -t jinanlongen/jay_cluster:py3 .
```
- 上传镜像
```
docker push jinanlongen/jay_cluster:py3
```
- 重新标记镜像
```
docker tag 192.168.200.150/longen/jay:latest cnaafhvk/jay
```
- 显示退出的镜像id
```
docker ps -q -f status=exited
```
[comment]: <tags> (docker)
[comment]: <description> (docker常用命令汇总)
[comment]: <title> (docker 命令)
[comment]: <author> (夏洛之枫)