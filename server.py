import socket


# 创建一个socket套接字，该套接字还没有建立连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定监听端口
server.bind(('172.20.31.117', 3044))
# 开始监听，并设置最大连接数
server.listen(5)
# 获取未建立连接的服务端的IP和端口信息
print(server.getsockname())
# 下面注释掉的是获取未建立连接的服务端套接字的远程IP和端口信息，执行下面语句会报错，原因就是现在还没有远程客户端程序连接
# print(server.getpeername())

print(u'waiting for connect...')
# 等待连接，一旦有客户端连接后，返回一个建立了连接后的套接字和连接的客户端的IP和端口元组
connect, (host, port) = server.accept()
# 现在建立连接就可以获取这两个信息了，注意server和connect套接字的区别，一个是未建立连接的套接字，一个是已经和客户端建立了连接的套接字
peer_name = connect.getpeername()
sock_name = connect.getsockname()
print(u'the client %s:%s has connected.' % (host, port))
print('The peer name is %s and sock name is %s' % (peer_name, sock_name))

# 接受客户端的数据
data = connect.recv(1024)
# 发送数据给客户端告诉他接收到了
connect.sendall(b'your words has received.')
print(b'the client say:' + data)

# 结束socket
server.close()
