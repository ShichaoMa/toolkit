## 下载解压jdk1.8 hadoop3.0
## 配置
### 修改host文件
```   
vi etc/hosts添加
192.168.200.107 nameNode

vi ~/.profile
export PATH=$PATH:/home/longen/jdk1.8.0_111/bin

vi etc/hadoop/core-site.xml
<configuration>
<property>
        <name>hadoop.tmp.dir</name>
        <value>/home/longen/tmp</value>
        <description>Abase for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://nameNode:9000</value>
    </property>
    <property>
        <name>io.file.buffer.size</name>
        <value>4096</value>
    </property>
</configuration>

vi etc/hadoop/hdfs-site.xml
<configuration>
 <property>
        <name>dfs.nameservices</name>
        <value>hadoop-cluster1</value>
    </property>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>nameNode:50090</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/longen/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/longen/dfs/data</value>
    </property>
    <property>
        <name>dfs.replication</name>
        <value>2</value>
    </property>
    <property>
        <name>dfs.webhdfs.enabled</name>
        <value>true</value>
    </property>
</configuration>

vi etc/hadoop/yarn-site.xml
<configuration>

<!-- Site specific YARN configuration properties -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>nameNode:8032</value>
    </property>
    <property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>nameNode:8030</value>
    </property>
    <property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>nameNode:8031</value>
    </property>
    <property>
        <name>yarn.resourcemanager.admin.address</name>
        <value>nameNode:8033</value>
    </property>
    <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>nameNode:8088</value>
    </property>
</configuration>

vi etc/hadoop/mapred-site.xml

<configuration>  
    <property>  
        <name>mapreduce.framework.name</name>  
        <value>yarn</value>  
    </property>  
    <property>  
        <name>mapreduce.jobtracker.http.address</name>  
        <value>nameNode:50030</value>  
    </property>  
    <property>  
        <name>mapreduce.jobhistory.address</name>  
        <value>nameNode:10020</value>  
    </property>  
    <property>  
        <name>mapreduce.jobhistory.webapp.address</name>  
        <value>nameNode:19888</value>  
    </property>  
</configuration> 

vi etc/hadoop/hadoop-env.sh

export JAVA_HOME=/home/longen/jdk1.8.0_111

vi etc/hadoop/yarn-env.sh

export JAVA_HOME=/home/longen/jdk1.8.0_111

```
## 创建目录

```
mkdir ~/tmp
mkdir -p dfs/data
mkdir -p dfs/name
mkdir  -p /etc/pdsh
vi /etc/pdsh/rcmd_default
添加 ssh
```

## 在nameNode的机器上

```
vi etc/hadoop/workers
192.168.200.122

```

## 将两台机器免登陆密钥互换

## 格式化namenode

    bin/hdfs namenode -format

## 启动

    sbin/start-yarn.sh
    sbin/start-dfs.sh

## web地址
        
    Daemon      	                Web Interface   	Notes
    NameNode	                http://nn_host:port/	Default HTTP port is 9870.
    ResourceManager         	http://rm_host:port/	Default HTTP port is 8088.
    MapReduce JobHistory Server	http://jhs_host:port/	Default HTTP port is 19888.
    
## 问题

#### Hadoop中Datanode警告server.common.Storage: Failed to add storage directory 
- 错误原因

目前没有再次去实验，可能与多次使用格式化命令有关：

    bin/hdfs namenode -format
- 解决方案
删除datanode的存储目录，再重建目录格式化。
步骤：
  - 停止namenode：
	sbin/stop-dfs.sh
  - 从错误信息：[DISK]file:/home/softwares/hadoop-2.7.3/data/tmp/dfs/data/中，
找到datanode目录：/hadoop-2.7.3/data/tmp/dfs/data

  - 直接删除/hadoop-2.7.3/中的data下的所有目录

  - 重新新建目录后，重新格式化HDFS：
	bin/hdfs namenode -format

  - 重新启动HDFS
	sbin/start-dfs.sh


参考资料

[Hadoop中Datanode警告server.common.Storage: Failed to add storage directory](http://blog.csdn.net/Magggggic/article/details/52503502)


[comment]: <tags> (hadoop)
[comment]: <description> (hadoop集群搭建)
[comment]: <title> (hadoop搭建)
[comment]: <author> (夏洛之枫)