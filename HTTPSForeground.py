from http.server import HTTPServer, BaseHTTPRequestHandler
from ssl import SSLContext
from socket import socket
import ssl
import os
import time

folderLocation = "C:\\Users\\xujus\\Desktop\\localhost\\"

os.system("cmd /c \"ipconfig > " + folderLocation + "txt.txt\"")
time.sleep(5)
ip = open(folderLocation + "txt.txt", 'r')
IPConfig = ip.read()
configSplit = IPConfig.split("\n")

num = 0
for i in configSplit:
    if "Wireless LAN adapter Wi-Fi:" in i:
        break
    num = num + 1
    
for i in range(num, len(configSplit)):
    if "IPv4 Address" in configSplit[i]:
        num = i
        break

host = configSplit[num].split(":")[1].replace(" ", "")
port = 443
#added this for shorter name but also easier searching, because there could be multiple name references to these numbers
#implemented to easier future code maintanence
addr = (host, port)

# print("Hosting on " + str(host) + ", with port " + str(port))

class HttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        file = open(folderLocation + "localhost.html", 'r')
        self.wfile.write(bytes(file.read(), "utf-8"))

server = HTTPServer(addr, HttpServer)

#need an instance of SSL
context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname=True
context.verify_mode=ssl.CERT_REQUIRED
#context.load_verify_locations(folderLocation + "localhost.pem")

sock = socket()
SSLSock = context.wrap_socket(sock)
server.socket = SSLSock
SSLSock.connect(addr)
server.serve_forever()
server.close()