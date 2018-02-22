[comment]: <> (![](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1517415066652&di=05f3dca3a9ddeffce449815573d6f0fa&imgtype=0&src=http%3A%2F%2Fwww.a166.com%2Fupload%2F2017-04%2F10%2Fnginxfanxiangdaili-83bce.png))
## nginx不管怎么修改配置，页面都是默认页面welcome to nginx的解决办法

### 现象描述：

在`/etc/nginx/nginx.conf`中无论怎么配置http，server项，页面都是默认的，而且启动nginx不报错，随意输入网址也不报错（都是welcome
to nginx）

### 分析：

注意`/etc/nginx/nginx.conf的http`中有没有`include /etc/nginx/sites-enabled/*;`这句话

如果有，那么再检查一下语句中的位置，是否有default这个文件，打开看看，原来这里已经有server,location这些定义，而在`/etc/nginx/nginx.conf`中定义的这些信息却不能覆盖先前的。

### 解决方案：

  * 第一种：注释掉这行，使其采用nginx.conf中的配置。
  * 第二种：直接修改default中的内容

参考资料[Welcome to nginx!怎么解决？](https://zhidao.baidu.com/question/509695082.html)

## nginx静态资源文件无法访问，403 forbidden错误

主要是nginx用户没有权限问题，将nginx.conf中的user改为root即可

参考资料[nginx静态资源文件无法访问，403 forbidden错误](http://ngcsnow.iteye.com/blog/2117975)


[comment]: <tags> (nginx)
[comment]: <description> (nginx配置相关问题)
[comment]: <title> (nginx相关)
[comment]: <author> (夏洛之枫)