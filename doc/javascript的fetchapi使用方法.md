[comment]: <> (![](https://gss3.bdstatic.com/-Po3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike80%2C5%2C5%2C80%2C26/sign=ed20149d0b7b020818c437b303b099b6/91ef76c6a7efce1b1e30f4f2ae51f3deb48f65ea.jpg))
### 发送fetch请求

一个基本的fetch请求发送起来非常简单，看下面的一段代码

    
    
    var myImage = document.querySelector('img');
    
    fetch('flowers.jpg').then(function(response) {
      return response.blob();
    }).then(function(myBlob) {
      var objectURL = URL.createObjectURL(myBlob);
      myImage.src = objectURL;
    });
    

在这里，我们通过网络获取图像并将其插入到元素中。
fetch（）最简单的用法是使用一个参数：要获取的资源的路径，并返回包含响应（Response对象）的promise。

这当然只是一个HTTP响应，而不是实际的图像。 为了从响应中提取图像正文内容，我们使用blob（）方法（在Body
mixin中定义，由Request和Response对象实现）。

### 提交请求选项

fetch（）方法可以选择性地接受第二个参数，一个init对象，它允许你控制许多不同的设置：

  * method: 请求方法，例如GET，POST。
  * headers:请求头，包含在一个Headers对象或一个带有ByteString值的对象文本中。
  * body: 任何你想添加到你的请求的主体：这可以是Blob，BufferSource，FormData，URLSearchParams或者USVString对象。请注意，使用GET或HEAD方法的请求不能有一个主体
  * mode: 您希望用于请求的模式，例如cors，no-cors或same-origin。
  * credentials:要用于请求的请求凭证：忽略 same-origin或include。要为当前域自动发送Cookie，必须提供此选项。从Chrome50开始，此属性还需要一个FederatedCredential实例或一个PasswordCredential实例.
  * cache: 要用于请求的缓存模式：default，no-store，reload，no-cache，force-cache或者only-if-cached。
  * redirect: 要使用的重定向模式: follow (自动跟随重定向), error (a如果发生重定向时发生错误中止), or manual (手动重定向). 在Chrome中，Chrome47之前默认情况下是follow，之后的版本默认情况下是manal。
  * referrer: 一个USVString 指定 no-referrer, client, or a URL. 默认是client.
  * referrerPolicy: 指定 referer HTTP header. 可能是 one of no-referrer, no-- referrer-when-downgrade, origin, origin-when-cross-origin, unsafe-url.
  * integrity:包含请求的子资源完整性值（例如，sha256-BpfBw7ivV8q2jLiT13fxDYAe2tJllusRSZ273h2nFSE =）
  * keepalive: keepalive选项可用于允许请求超出页面。使用Keepalive标志提取是Navigator.sendBeacon（）API的替代品。
  * signal: 一个AbortSignal对象实例;允许您与获取请求进行通信，并在需要时通过AbortController中止。

参考资料 [Using Fetch](https://developer.mozilla.org/en-
US/docs/Web/API/Fetch_API/Using_Fetch)

[CORS protocol](https://fetch.spec.whatwg.org/#http-cors-protocol)


[comment]: <tags> (javascript,fetch)
[comment]: <description> (javascript的fetchapi使用方法)
[comment]: <title> (javascript的fetchapi使用方法)
[comment]: <author> (夏洛之枫)