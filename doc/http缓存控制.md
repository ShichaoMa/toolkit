## Last-Modified和If-Modified-Since
- 第一次：客户端请求服务端，服务端返回LastModified: `该资源上次修改的时间`，该时间和资源同时被浏览器缓存下来
- 第二次：客户端请求服务端，带着If-Modified-Since: `该资源上次修改的时间`，
  - 如果该资源修改时间未变，则返回304，浏览器使用本地缓存的资源；
  - 否则返回200，重新获取资源。
## Cache-Control和Etag
- 第一次：客户端请求服务器，服务器返回Etag: `该资源的指纹`和Cache-Control: max-age=60，缓存的最长时间为60秒
- 第二次：
    - 未超过60秒，客户发现本地有，则直接200 from_memory_cache/from_disk_cache
    - 超过了60秒，客户端请求服务端带着 If-None-Match：`该资源的指纹`，
      - 如果资源发生了变化，则200返回资源和新的Etag；
      - 则返回304，浏览器使用本地缓存的资源。
      
注：
- 如果服务器返回Cache-Control:no-cache or max-age=0，会当作cache超时并重新确认cache是否可用。
- 如果服务器返回Cache-Control:no-store，则浏览器永远不会缓存cache，每次都是重新获取。

      
