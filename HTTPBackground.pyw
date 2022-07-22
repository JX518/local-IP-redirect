import socketserver
from http.server import SimpleHTTPRequestHandler
import ssl
import time
import os
import sys

sys.stdout = open(os.devnull, "w")
sys.stderr = open(os.devnull, "w")

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

print("Hosting on " + str(host) + ", with port " + str(port))

class HttpServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        file = open(folderLocation + "localhost.html", 'r')
        self.wfile.write(bytes(file.read(), "utf-8"))

httpd = socketserver.TCPServer((host, port), HttpServer)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile=folderLocation+"localhost.pem", keyfile=folderLocation+"localhost.key",server_side=True)
httpd.serve_forever()