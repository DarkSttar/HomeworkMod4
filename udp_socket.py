import socket
from threading import Thread
from datetime import datetime
import json
import pathlib
UDP_IP = '127.0.0.1'
UDP_PORT = 5000
DATA_JSON = pathlib.Path('storage/data.json')

def run_server(ip,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server = ip,port
    sock.bind(server)
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

if __name__ == '__main__':
    run_server(UDP_IP,UDP_PORT)
