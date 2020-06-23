import socket

from pathlib import Path


HOST = '127.0.0.1'
PORT = 25000


class Client:
    def __init__(self, chunk_size=1024):
        self.socket = None
        self.file_buf = b''   
        if chunk_size < 1:
            raise ValueError("`chunk_size` should be a positive int")
        self.chunk_size = chunk_size

    def connect(self, host, port):
        # disconnect from existing one if any
        self.disconnect()
        
        self.host = host
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2) # wait at most 2 seconds on connect to server
        try:
            self.socket.connect((self.host, self.port))
        except socket.timeout as e:
            print(f'Connection to {self.host}:{self.port} failed')
            return False
        return True

    def is_valid_file(self, file_name):
        if not Path(file_name).is_file():
            print(f"'{file_name}' is not a valid file")
            return False
        return True

    def send_file(self, file_name):
        if self.is_valid_file(file_name):
            with open(file_name, 'rb') as f:
                self.file_buf = f.read()
        else:
            return False

        if not self.socket: # or self.socket.closed:
            self.connect()

        with self.socket:
            sent = 0
            while sent < len(self.file_buf):
                try:
                    size_chunk = min(self.chunk_size, len(self.file_buf) - sent)
                    self.socket.send(self.file_buf[sent:sent + size_chunk])
                    sent += size_chunk
                except KeyboardInterrupt:
                    print('Interrupted')
                    break

    def disconnect(self):
        if self.socket and self.socket.fileno() > -1:
            self.socket.close()
