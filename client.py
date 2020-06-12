import sys
import socket
import time
import wave

from pathlib import Path


def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 25000))
    return s


def client(file):
    s = create_socket()
    try:
        print('sending', file)
        f_size = Path(file).stat().st_size
        print('file size', f_size)
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
    assert len(sys.argv) == 2
    file = sys.argv[1]
    client(file)