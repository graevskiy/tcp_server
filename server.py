import io
import socket

from hashlib import md5
from select import select


HOST = '127.0.0.1'
PORT = 25000

wait_to_read = []
bufs_ready_to_file = []


class SocketBundle:
    __slots__ = ['sock', 'buf', 'func']

    def __init__(self, sock, buf, func):
        self.sock = sock
        self.buf = buf
        self.func = func

    def fileno(self):
        return self.sock.fileno()

    @property
    def md5(self):
        return md5(self.buf).hexdigest()

    def __str__(self):
        return f"sock={self.fileno()}, buf={len(self.buf)}, func={self.func}"


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    # make server_socket non blocking (for `accept` below)
    server_socket.setblocking(False)
    print(server_socket)
    return server_socket


def accept_wrapper(bundle):
    client, address = bundle.sock.accept()
    # switch to non blocking mode explicitly
    # by: https://docs.python.org/3/library/socket.html#timeouts-and-the-accept-method
    client.setblocking(False) 
    
    print('Connection from', address)
    wait_to_read.append(SocketBundle(client, bytes(), handler_wav))



def handler_wav(bundle):
    print(bundle)

    req = bundle.sock.recv(1024)

    bundle.buf += req
    print(len(req))

    if not req:
        print('no req')
        hash_sum = bundle.md5
        print('MD5 to check:', hash_sum)

        # bundle is still in the 'to read' list
        # just change function
        bundle.func = close_conn       


def close_conn(bundle):
    print('close connection')
    # bundle.sock.close()
    wait_to_read.remove(bundle)
    bufs_ready_to_file.append(bundle.buf)
    print([
        f"MD5 to check: {md5(i).hexdigest()}"
        for i in bufs_ready_to_file
    ])


def event_loop():
    while True:
        try:
            # make timeout to be 0.1 to force loop wait this time
            # in case no sockets are ready (allow to aggregate something)
            socks_read, _, _ = select(wait_to_read, [], [], 0.1)

            for bundle in socks_read:
                print(bundle.sock)
                bundle.func(bundle)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    s = server()
    wait_to_read.append(SocketBundle(s, bytes(), accept_wrapper))
    event_loop()