from socket import *
from select import *
import re


class WebServer:
    def __init__(self, host='', port=80, html=None):
        self.host = host
        self.port = port
        self.html = html  # 网页的根目录
        self.create_socket()
        self.bind()
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    def start(self):
        self.sock.listen(5)
        print("Listen the port %d..." % self.port)
        self.rlist.append(self.sock)
        while True:
            # 开始监控IO
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sock:
                    connfd, addr = rs[0].accept()
                    print("Connect from", addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    try:
                        # 收到http请求
                        self.handle(r)
                    except:
                        r.close()
                        self.rlist.remove(r)
    def handle(self, connfd):
        request = connfd.recv(1024).decode()
        print(request)
        pattern = "[A-Z]+\s+(?P<info>/\S)"
        result = re.match(pattern, request)
        if request:
            info = result.group('info')
            print('请求内容:', info)
            self.send_html(connfd, info)
        else:
            connfd.close()
            self.rlist.remove(connfd)
            return

    def send_html(self, connfd, info):
        if info=='/':
            filename=self.html+"/index.html"
        else:
            filename=self.html+info
        try:
            f=open(filename,'rb')
        except:
            response="HTTP/1.1 404 Not Found\r\n"
            response+= "Content-Type:text/html\r\n"
            response+= "\r\n"
            response+="<h1>Sorry...<\h1>"
            response=response.encode()
        else:
            data=f.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n"%len(data)
            response += "\r\n"
            response =response.encode()+f.read()
        finally:
            connfd.send(response)

if __name__ == '__main__':
    httpd = WebServer(host='', port=8880, html="/home/tarena/下载/newwork/info/static")
    httpd.start()
