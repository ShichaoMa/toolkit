[comment]: <> (![](https://serverdensity-wpengine.netdna-ssl.com/wp-content/themes/blog.new/images/random/mongodb.png))
## 查找返回指定字段

    
    
    >> list = col.find({"parent_asin": "B00UB2D5GS"}, projection: {"price": 1, _id: 0})
    


[comment]: <tags> (mongodb,ruby)
[comment]: <description> (monogdb ruby api)
[comment]: <title> (mongodb ruby api)
[comment]: <author> (夏洛之枫)