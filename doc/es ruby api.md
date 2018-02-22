## 安装es ruby api
```
gem install elasticsearch
```

## 创建链接
```
client = Elasticsearch::Client.new host: '192.168.200.107'
```

## 查看集群的健康情况
```
>> client.cluster.health
=> {"cluster_name"=>"elasticsearch", "status"=>"yellow", "timed_out"=>false, "number_of_nodes"=>3, "number_of_data_nodes"=>3, "active_primary_shards"=>31, "active_shards"=>31, "relocating_shards"=>0, "initializing_shards"=>0, "unassigned_shards"=>31, "delayed_unassigned_shards"=>0, "number_of_pending_tasks"=>0, "number_of_in_flight_fetch"=>0, "task_max_waiting_in_queue_millis"=>0, "active_shards_percent_as_number"=>50.0}
```
## 查看指定索引，指定类型，指定id的值
```
>> client.search index: "customer", type: "external", id: 1
=> {"took"=>1, "timed_out"=>false, "_shards"=>{"total"=>5, "successful"=>5, "failed"=>0}, "hits"=>{"total"=>1, "max_score"=>1.0, "hits"=>[{"_index"=>"customer", "_type"=>"external", "_id"=>"1", "_score"=>1.0, "_source"=>{"name"=>"John Doe"}}]}}
```
## 插入一个元素
```
>> client.index index: "customer", type: "external", id: 2, body: {name: "wangchuan"}
=> {"_index"=>"customer", "_type"=>"external", "_id"=>"2", "_version"=>1, "result"=>"created", "_shards"=>{"total"=>2, "successful"=>1, "failed"=>0}, "created"=>true}
```
##  查询一个数据
```
>> client.search index: "customer", body:  {"query":{"match":{"name":{"query":"wangchuan"}}}}
=> {"took"=>2, "timed_out"=>false, "_shards"=>{"total"=>5, "successful"=>5, "failed"=>0}, "hits"=>{"total"=>1, "max_score"=>0.2876821, "hits"=>[{"_index"=>"customer", "_type"=>"external", "_id"=>"2", "_score"=>0.2876821, "_source"=>{"name"=>"wangchuan"}}]}}
```

[comment]: <tags> (elasticsearch,ruby)
[comment]: <description> (es的ruby api)
[comment]: <title> (es ruby api)
[comment]: <author> (夏洛之枫)