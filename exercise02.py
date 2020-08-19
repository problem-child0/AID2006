"""
    基于select方法的IO多路复用网络并发
"""
from select import select
from socket import *

HOST = ""
PORT = 8888
ADDR = (HOST, PORT)
sockfd = socket()
sockfd.bind(ADDR)
sockfd.listen(5)
sockfd.setblocking(False)
rlist = [sockfd]
wlist = []
xlist = []
while True:
    # 开始监控IO
    rs, ws, xs = select(rlist, wlist, xlist)
    for r in rs:
        if r is sockfd:
            connfd, addr = rs[0].accept()
            print("Connect from", addr)
            connfd.setblocking(False)
            rlist.append(connfd)
        else:
            data=r.recv(1024).decode()
            if not data:
                rlist.remove(r)
                r.close()
                continue
            print("收到：",data)
            # r.send(b'ok')
            wlist.append(r)
    for w in ws:
        w.send(b"ok")
        wlist.remove(w)