# 安装和启动

Elasticsearch 需要至少Java 8以上的版本支持，本教程推荐使用Oracle JDK version 1.8.0_73.Java的安装细节每个平台都不同，在这里我们不打算详细讨论，在Oracle官网上可以找到推荐的安装手册，我只想说的是，在开始安装elasticsearch之前，运行以下命令来检查Java的版本（然后升级或才安装）
`
```
java -version
echo $JAVA_HOME

```
一但我们安装了Java，我们可以就可以下载和安装elasticsearch了，在www.elastic.co/downloads可以得到过往所有版本的二进制文件，每个版本你都可以选择zip，tar或者deb，rpm格式的安装文件.简单点，我们接下来选择tar文件。
通过如下指令我们下载 Elasticsearch 5.0.1 tar

```
curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.0.1.tar.gz
```
然后解压
```
tar -xvf elasticsearch-5.0.1.tar.gz
```
解压完毕后，进入bin目录
```
cd elasticsearch-5.0.1/bin
```
现在我们准备启动我们的单节点集群
```
./elasticsearch
```
如果一切运行正常，你会见到如下信息
```
[2016-09-16T14:17:51,251][INFO ][o.e.n.Node               ] [] initializing ...
[2016-09-16T14:17:51,329][INFO ][o.e.e.NodeEnvironment    ] [6-bjhwl] using [1] data paths, mounts [[/ (/dev/sda1)]], net usable_space [317.7gb], net total_space [453.6gb], spins? [no], types [ext4]
[2016-09-16T14:17:51,330][INFO ][o.e.e.NodeEnvironment    ] [6-bjhwl] heap size [1.9gb], compressed ordinary object pointers [true]
[2016-09-16T14:17:51,333][INFO ][o.e.n.Node               ] [6-bjhwl] node name [6-bjhwl] derived from node ID; set [node.name] to override
[2016-09-16T14:17:51,334][INFO ][o.e.n.Node               ] [6-bjhwl] version[5.0.1], pid[21261], build[f5daa16/2016-09-16T09:12:24.346Z], OS[Linux/4.4.0-36-generic/amd64], JVM[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/1.8.0_60/25.60-b23]
[2016-09-16T14:17:51,967][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [aggs-matrix-stats]
[2016-09-16T14:17:51,967][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [ingest-common]
[2016-09-16T14:17:51,967][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [lang-expression]
[2016-09-16T14:17:51,967][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [lang-groovy]
[2016-09-16T14:17:51,967][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [lang-mustache]
[2016-09-16T14:17:51,967][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [lang-painless]
[2016-09-16T14:17:51,967][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [percolator]
[2016-09-16T14:17:51,968][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [reindex]
[2016-09-16T14:17:51,968][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [transport-netty3]
[2016-09-16T14:17:51,968][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded module [transport-netty4]
[2016-09-16T14:17:51,968][INFO ][o.e.p.PluginsService     ] [6-bjhwl] loaded plugin [mapper-murmur3]
[2016-09-16T14:17:53,521][INFO ][o.e.n.Node               ] [6-bjhwl] initialized
[2016-09-16T14:17:53,521][INFO ][o.e.n.Node               ] [6-bjhwl] starting ...
[2016-09-16T14:17:53,671][INFO ][o.e.t.TransportService   ] [6-bjhwl] publish_address {192.168.8.112:9300}, bound_addresses {{192.168.8.112:9300}
[2016-09-16T14:17:53,676][WARN ][o.e.b.BootstrapCheck     ] [6-bjhwl] max virtual memory areas vm.max_map_count [65530] likely too low, increase to at least [262144]
[2016-09-16T14:17:56,731][INFO ][o.e.h.HttpServer         ] [6-bjhwl] publish_address {192.168.8.112:9200}, bound_addresses {[::1]:9200}, {192.168.8.112:9200}
[2016-09-16T14:17:56,732][INFO ][o.e.g.GatewayService     ] [6-bjhwl] recovered [0] indices into cluster_state
```
抛开多余的细节不看，我们可以发现我们名为"I8hydUG"(可能与你的不同)的节点作为一个单节点集群已经启动。你可以指定结点名称和集群名称
```
 ./elasticsearch -Ecluster.name=my_cluster_name
```

[comment]: <tags> (elasticsearch)
[comment]: <description> (es学习2)
[comment]: <title> (elasticsearch学习之----（2）安装)
[comment]: <author> (夏洛之枫)