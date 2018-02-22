# 定义api
    curl -i -X POST \
      --url http://192.168.200.37:8001/apis/ \
      --data 'name=es-indices-api' \
      --data 'hosts=es.com' \
      --data 'upstream_url=http://192.168.200.90:9200/_cat/indices'
# 访问api
    curl -i -X GET \
      --url http://192.168.200.37:8000/ \
      --header 'Host: es.com'
      
# 启用plugins
    curl -i -X POST \
      --url http://localhost:8001/apis/es-indices-api/plugins/ \
      --data 'name=key-auth'
#创建consumer
    curl -i -X POST \
      --url http://localhost:8001/consumers/ \
      --data "username=Jason"
#指定consumer key
    curl -i -X POST \
      --url http://localhost:8001/consumers/Jason/key-auth/ \
      --data 'key=ENTER_KEY_HERE'
# 通过key 访问api
    curl -i -X GET \
      --url http://localhost:8000/ \
      --header 'Host: es.com' \
      --header "apikey: ENTER_KEY_HERE"
# 增加速率限制plugins
    curl -X POST http://localhost:8001/apis/es-indices-api/plugins \
        --data "name=rate-limiting" \
        --data "config.second=5" \
        --data "config.hour=10000"
# 增加datalog plugins
    curl -X POST http://localhost:8001/apis/plugins \
        --data "name=datadog" \
        --data "config.host=127.0.0.1" \
        --data "config.port=8125" \
        --data "config.timeout=1000"
# 增加galileo plugins
    curl -X POST http://localhost:8001/plugins/ \
        --data "name=galileo" \
        --data "config.service_token=966bbac007bf11e7a47fb3f5df052576" \
        --data "config.environment=default-environment"
# 增加file-log plugins
    curl -X POST http://localhost:8001/plugins \
        --data "name=file-log" \
        --data "config.path=/home/ubuntu/logs/file.log"
# 增加http-log plugins
    curl -X POST http://localhost:8001/plugins \
        --data "name=http-log" \
        --data "config.http_endpoint=http://192.168.200.58:5000/" \
        --data "config.method=POST" \
        --data "config.timeout=1000" \
        --data "config.keepalive=1000"
# 显示所有plugins
    curl -X GET http://localhost:8001/plugins/
# 删除plugins 最后是plugin的id
    curl -X DELETE http://localhost:8001/plugins/bba2a3b5-6a24-4f74-b8cd-f154d9aac88d
[comment]: <tags> (kong,apigateway)
[comment]: <description> (kong api网关的的相关命令)
[comment]: <title> (kong相关命令)
[comment]: <author> (夏洛之枫)