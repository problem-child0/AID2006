from socket import *

s = socket()
s.bind(('', 8888))
s.listen()

c, abbr = s.accept()
data = c.recv(1024 * 10).decode()
print(data)
html = "HTTP/1.1 200 OK\r\n"
html += "Content-Type:text/html\r\n"
html += "\r\n"
with open("python.html")as f:
    html += f.read()

c.send(html.encode())
c.close()
s.close()
