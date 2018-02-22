uwsgi下的web页面发送包含较大请求体的post请求时出现ERR_CONTENT_LENGTH_MISMATCH
nginx中的错误如下：
```
2018/02/22 01:02:46 [error] 31556#31556: *7657 readv() failed (104: Connection reset by peer) while reading upstream, client: 112.231.57.20, server: localhost, request: "POST /modify HTTP/1.1", upstream: "uwsgi://127.0.0.1:3031", host: "mashichao.com", referrer: "http://mashichao.com/?path=/me?code=QQLB8Z"
```
uwsgi中没有发现错误
其实是因为请求过大，导致request头没有被uwsgi读完导致的，调整uwsgi的buffer-size参数就可以，默认是4096，调整到65535。

参考资料[Nginx uwsgi (104: Connection reset by peer) while reading response header from upstream](https://stackoverflow.com/questions/22697584/nginx-uwsgi-104-connection-reset-by-peer-while-reading-response-header-from-u)
[comment]: <tags> (uwsgi)
[comment]: <description> (uwsgi web程序ERR_CONTENT_LENGTH_MISMATCH)
[comment]: <title> (uwsgi相关问题)
[comment]: <author> (夏洛之枫)