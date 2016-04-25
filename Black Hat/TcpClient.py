import socket

target_host = "www.sina.com"
target_port = 80

#建立一个socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#连接客户端
client.connect((target_host, target_port))

#发送数据
client.send("GET / HTTP/1.1\r\nHost: sina.com\r\n\r\n")

#接收数据
response = client.recv(4096)

print response