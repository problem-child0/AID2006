from socket import *
from time import *
sockfd=socket()
sockfd.bind(('',8888))
sockfd.listen(5)
# sockfd.setblocking(False)
sockfd.settimeout(3)
while True:
    try:
        print("waiting for connect")
        connfd,addr=sockfd.accept()
        print("Connect from",addr)
    except BlockingIOError as e:
        sleep(2)
        with open("test.log",'a')as f:
            msg="%s:%s\n"%(ctime(),e)
            f.write(msg)
    except timeout as e:
        with open("test.log",'a')as f:
            msg="%s:%s\n"%(ctime(),e)
            f.write(msg)
        #与accept连接无关
    else:
        #与连接有关
        data=connfd.recv(1024).decode()
        print(data)
sockfd.close()