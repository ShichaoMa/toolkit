- 在application.rb中添加以下两条配置
```
config.time_zone = 'Beijing' # 只设置这一个就可以
config.active_record.default_timezone = :local # 设置了之后数据库保存的也会本地记录
```
参考：[Rails 中的时区及时间问题](https://ruby-china.org/topics/16187)
[comment]: <tags> (rails)
[comment]: <description> (rails时区配置)
[comment]: <title> (rails时区设置)
[comment]: <author> (夏洛之枫)