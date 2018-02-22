## 修改配置文件
```
vi config/elasticsearch.yml

node.name: nameNode

network.host: 192.168.200.107

discovery.zen.ping.unicast.hosts: ["nameNode"]

```

## 启动各个节点
```
bin/elasticsearch
```

参考资料

[Elasticsearch 集群搭建实战笔记](http://www.bkjia.com/Linux/1125376.html)
[comment]: <tags> (elasticsearch)
[comment]: <description> (es配置方法)
[comment]: <title> (elasticsearch cluster配置)
[comment]: <author> (夏洛之枫)