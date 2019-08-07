import socket


# 创建一个socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 主动去连接本机IP和端口号为6688的进程，localhost等效于127.0.0.1，也就是去连接本机端口为6688的进程
client.connect(('172.20.31.117', 3044))

# 接受控制台的输入
data = input()
# 对数据进行编码格式转换，不然报错
data = data.encode('utf-8')
# 发送数据
client.sendall(data)
# 接收服务端的反馈数据
rec_data = client.recv(1024)
print(b'form server receive:' + rec_data)

client.close()
