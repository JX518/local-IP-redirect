from http.server import HTTPServer, BaseHTTPRequestHandler
from ssl import SSLContext
from socket import socket
import socket as Socket
import ssl
import os
import time

from OpenSSL import crypto

#run IPConfig and obtain the local ip
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
# host = "localhost"
port = 443
#added this for shorter name but also easier searching, because there could be multiple name references to these numbers
#implemented to easier future code maintanence
addr = (host, port)

# print("Hosting on " + str(host) + ", with port " + str(port))

CERT_FILE = folderLocation + "localhost.cert.pem"
KEY_FILE = folderLocation + "localhost.key.pem"
def create_self_signed_cert():
    #key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

     # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "Arizona"
    cert.get_subject().L = "Maricopa"
    cert.get_subject().O = "Home"
    cert.get_subject().OU = "Home"
    cert.get_subject().CN = Socket.gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(CERT_FILE, "wb").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(KEY_FILE, "wb").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

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

create_self_signed_cert()
context.load_cert_chain(folderLocation+"localhost.cert.pem", folderLocation+"localhost.key.pem")

sock = socket()
sock.bind((host, 8000))
server.socket = context.wrap_socket(sock, server_side=False, server_hostname="localhost")
server.serve_forever()
server.close()