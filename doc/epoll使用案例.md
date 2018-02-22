[comment]: <> (![](https://motorimpex.com.ua/files/brands/Epoll.jpg))
### 状态触发

    
    
    import socket, select
    
    EOL1 = b'\n\n'
    EOL2 = b'\n\r\n'
    response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
    response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
    response += b'Hello, world!'
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', 8080))
    serversocket.listen(1)
    serversocket.setblocking(0)
    
    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN)
    
    try:
       connections = {}; requests = {}; responses = {}
       while True:
          events = epoll.poll(1)
          for fileno, event in events:
             if fileno == serversocket.fileno():
                connection, address = serversocket.accept()
                connection.setblocking(0)
                epoll.register(connection.fileno(), select.EPOLLIN)
                connections[connection.fileno()] = connection
                requests[connection.fileno()] = b''
                responses[connection.fileno()] = response
             elif event & select.EPOLLIN:
                requests[fileno] += connections[fileno].recv(1024)
                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                   epoll.modify(fileno, select.EPOLLOUT)
                   print('-'*40 + '\n' + requests[fileno].decode()[:-2])
             elif event & select.EPOLLOUT:
                byteswritten = connections[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][byteswritten:]
                if len(responses[fileno]) == 0:
                   epoll.modify(fileno, 0)
                   connections[fileno].shutdown(socket.SHUT_RDWR)
             elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
    finally:
       epoll.unregister(serversocket.fileno())
       epoll.close()
       serversocket.close()
    

边沿触发

    
    
    import socket, select
    
    EOL1 = b'\n\n'
    EOL2 = b'\n\r\n'
    response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
    response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
    response += b'Hello, world!'
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', 8080))
    serversocket.listen(1)
    serversocket.setblocking(0)
    
    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)
    
    try:
       connections = {}; requests = {}; responses = {}
       while True:
          events = epoll.poll(1)
          for fileno, event in events:
             if fileno == serversocket.fileno():
                try:
                   while True:
                      connection, address = serversocket.accept()
                      connection.setblocking(0)
                      epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
                      connections[connection.fileno()] = connection
                      requests[connection.fileno()] = b''
                      responses[connection.fileno()] = response
                except socket.error:
                   pass
             elif event & select.EPOLLIN:
                try:
                   while True:
                      requests[fileno] += connections[fileno].recv(1024)
                except socket.error:
                   pass
                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                   epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
                   print('-'*40 + '\n' + requests[fileno].decode()[:-2])
             elif event & select.EPOLLOUT:
                try:
                   while len(responses[fileno]) > 0:
                      byteswritten = connections[fileno].send(responses[fileno])
                      responses[fileno] = responses[fileno][byteswritten:]
                except socket.error:
                   pass
                if len(responses[fileno]) == 0:
                   epoll.modify(fileno, select.EPOLLET)
                   connections[fileno].shutdown(socket.SHUT_RDWR)
             elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
    finally:
       epoll.unregister(serversocket.fileno())
       epoll.close()
       serversocket.close()
    

参考资料：[python下使用epoll](http://blog.csdn.net/hehe123456ZXC/article/details/52526670)


[comment]: <tags> (epoll)
[comment]: <description> (python下使用epoll)
[comment]: <title> (epoll使用案例)
[comment]: <author> (夏洛之枫)