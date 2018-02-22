## vi conf/hbase-site.xml 
    <configuration>
    <property>
      <name>hbase.cluster.distributed</name>
      <value>true</value>
    </property>
    <property>
      <name>hbase.rootdir</name>
      <value>hdfs://nameNode:9000/hbase</value>
    </property>
    <property>
      <name>hbase.zookeeper.quorum</name>
      <value>nameNode,dataNode1, dataNode2</value>
    </property>
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/home/longen/zookeeper</value>
      </property>
    </configuration>
## vi conf/hbase-env.sh
    export JAVA_HOME=/home/longen/jdk1.8.0_111/ 
    export HBASE_PID_DIR=/home/longen/pids # pid默认在/tmp下面
## vi  conf/regionservers # region
    dataNode1
    dataNode2
## vi conf/backup-masters # 备用master
    dataNode1

[comment]: <tags> (hbase)
[comment]: <description> (hbase集群搭建)
[comment]: <title> (hbase集群搭建)
[comment]: <author> (夏洛之枫)