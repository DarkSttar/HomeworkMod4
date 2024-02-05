from http.server import HTTPServer,BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import socket
from time import sleep

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

def run_udp_client(ip,port,message):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server = ip,port
    data = message.encode()
    sock.sendto(data,server)
    #print(f'Send Data: {data.decode()} to Server')
    response, address = sock.recvfrom(1024)
    #print(f'Responses data: {response.decode()} from address: {address}')
    sock.close()




class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parse_url = urllib.parse.urlparse(self.path)
        if parse_url.path == '/':
            print(f'PATH =======> {parse_url.path}')
            self.send_html_file(pathlib.Path('index.html'))
        elif parse_url.path == '/message':
            self.send_html_file(pathlib.Path('message.html'))
        else:
            if pathlib.Path().joinpath(parse_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html',404)
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        
        data_parse = urllib.parse.unquote_plus(data.decode())
        
        run_udp_client(UDP_IP,UDP_PORT,data_parse)
        self.send_response(302)
        self.send_header('Location','/')
        self.end_headers()
    def send_html_file(self,filename,status=200):
        
        
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            print(filename)
            self.wfile.write(fd.read())
    
    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header('Content-type',mt[0])
        else:
            self.send_header('Content-type','text/plain')
        self.end_headers()
        with open(f'.{self.path}','rb') as file:
            self.wfile.write(file.read())
        

def run(server_class=HTTPServer,handler_class=HTTPHandler):
    server_address = ('',8000)
    http = server_class(server_address,handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
    
if __name__ == '__main__':
    run()
   
   
