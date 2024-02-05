from http.server import HTTPServer,BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import socket
from threading import Thread
from datetime import datetime
import json
import pathlib
import os
UDP_IP = '127.0.0.1'
UDP_PORT = 5000
DATA_JSON = pathlib.Path('storage/data.json')

def handle_data(data):
    # Ваш код обробки даних тут
    print(data)

def run_udp_server(ip,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server = ip,port
    sock.bind(server)
    print("UDP SERVER STARTED")
    try:
        while True:
            json_data = None
            data,address = sock.recvfrom(1024)
            sock.sendto(data, address)
            data_dict = {key: value for key, value in [el.split('=') for el in data.decode().split('&')]}
            json_data = {str(datetime.now()): data_dict}
            
            if json_data:
                try:
                    with open(DATA_JSON, 'r') as file:
                        json_content = json.load(file)
                        json_content.update(json_data)
                        with open(DATA_JSON,'w') as file:
                            json.dump(json_content,file,indent=1)
                except json.decoder.JSONDecodeError:
                    with open(DATA_JSON,'w') as file:
                        json.dump(json_data,file,indent=1)
    except KeyboardInterrupt:
        print(f'Destroy Server')
    finally:
        
        sock.close()


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
        

def run_http_server(server_class=HTTPServer,handler_class=HTTPHandler):
    server_address = ('',8000)
    http = server_class(server_address,handler_class)
    print("HTTP SERVER STARTED")
    try:
        http.serve_forever()
        
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':    
    storage_directory = 'storage'
    os.makedirs(storage_directory, exist_ok=True)

    data_file_path = os.path.join(storage_directory, 'data.json')
    if not os.path.exists(data_file_path):
        with open(data_file_path, 'w') as data_file:
            data_file.write('{}')
    http_server_thread = Thread(target=run_http_server, args=(HTTPServer,HTTPHandler))
    udp_server_thread = Thread(target=run_udp_server,args=(UDP_IP,UDP_PORT,))
    http_server_thread.start()
    udp_server_thread.start()
    http_server_thread.join()
    udp_server_thread.join()