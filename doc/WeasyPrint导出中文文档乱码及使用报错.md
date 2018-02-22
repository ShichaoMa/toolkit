[comment]: <> (![](http://weasyprint.org/css/img/logo.png))
#### OSError: dlopen() failed to load a library: cairo / cairo-2

是因为没有安装cairo，运行`apt-get install libcairo2-dev`解决

#### OSError: cannot load library pango-1.0: pango-1.0: cannot open shared
object file: No such file or directory. Additionally,
ctypes.util.find_library() did not manage to locate a library called
'pango-1.0

是因为没有安装pango，运行`apt-get install pango1.0-tests`解决

#### 乱码

是因为没有安装中文字体

    
    
    apt-get install xfonts-intl-chinese xfonts-wqy ttf-wqy-zenhei
    apt-get install ttf-wqy-microhei xfonts-intl-chinese-big
    
#### 如何渲染pdf时连同图片一并渲染
网站中的图片链接必须是绝对url，不能是相对url。

参考资料

[DEBIAN 7,PYTHON3.3.2,安装WEASYPRINT](https://8loo.cn/2013/09/12/debian-
7python3-3-2%E5%AE%89%E8%A3%85weasyprint/)


[comment]: <tags> (weasyprint)
[comment]: <description> (WeasyPrint导出中文文档乱码及使用报错)
[comment]: <title> (WeasyPrint导出中文文档乱码及使用报错)
[comment]: <author> (夏洛之枫)