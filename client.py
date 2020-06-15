import sys
import socket
import time

from pathlib import Path


def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 25000))
    return s


def client(s, file, timeout=0):
    try:
        print('sending', file)
        f_size = Path(file).stat().st_size
        print('file size', f_size)
        print('going to sleep...')
        
        for i in range(timeout):
            print(timeout-i)
            time.sleep(1)            

        print('woke up!')
        s.sendall(str(f_size).encode('utf-8'))
        with open(file, 'rb') as f:
            s.sendall(f.read())
        print('sent, waiting response')
        resp = s.recv(1024)
        print(resp)
    finally:
        print('close connection')
        s.close()


if __name__ == "__main__":

    assert len(sys.argv) == 3
    
    file = sys.argv[1]
    timeout = int(sys.argv[2])
    
    socket = create_socket()
    client(socket, file, timeout)