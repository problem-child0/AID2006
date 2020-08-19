"""
    基于select方法的IO多路复用网络并发
"""
from select import *
from socket import *

HOST = ""
PORT = 8888
ADDR = (HOST, PORT)
sockfd = socket()
sockfd.bind(ADDR)
sockfd.listen(5)
sockfd.setblocking(False)
p = poll()
p.register(sockfd, POLLIN)
map = {sockfd.fileno(): sockfd}
while True:
    # 开始监控IO
    events = p.poll()
    for fd, event in events:
        if fd == sockfd.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            connfd.setblocking(False)
            p.register(connfd, POLLIN)
            map[connfd.fileno()] = connfd
        else:
            data = map[fd].recv(1024).decode()
            if not data:
                p.unregister(fd)
                map[fd].close()
                del map[fd]
                continue
            print("收到：", data)
            map[fd].send(b'ok')
