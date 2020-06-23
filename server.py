import socket

from hashlib import md5
from select import select


HOST = '127.0.0.1'
PORT = 25000


class SocketBundle:
    """Class represents server socket 
    (either listening or communicating).
    Stores TCP socket itself, read buffer `buf` and accociated function

    """
    __slots__ = ['sock', 'buf', 'func']

    def __init__(self, sock, buf, func):
        """Initializer

        :param sock: client socket
        :param buf bytes: buffer of read bytes
        :param func function: function which has to be invoked on the socket next        
        """
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


class Server:
    """TCP socket server which handles receiving bytes from clients
    Works in non-blocking mode by using `select` module.

    """
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.wait_to_read = []
        self._bufs_ready_to_file = []

    @property
    def buffers(self):
        return [
            f"MD5 to check: {md5(i).hexdigest()}"
            for i in _bufs_ready_to_file
        ]

    def accept_connection(self, bundle):
        client, address = bundle.sock.accept() #could use self.s_sock instead
        # switch to non blocking mode explicitly
        # by: https://docs.python.org/3/library/socket.html#timeouts-and-the-accept-method
        client.setblocking(False) 
        
        print('Connection from', address)
        self.wait_to_read.append(
                SocketBundle(sock=client, buf=b'', func=self.handle_recv)
            )

    def handle_recv(self, bundle):
        req = bundle.sock.recv(1024)
        print(len(req))

        if req:
            bundle.buf += req
            print(len(bundle.buf))
        else:            
            # bundle is still in the 'to read' list
            # just change function
            bundle.func = self.close_conn

    def close_conn(self, bundle):
        print('closing connection')
        bundle.sock.close()
        
        if bundle in self.wait_to_read:
            self.wait_to_read.remove(bundle)
        if bundle.buf:
            self._bufs_ready_to_file.append(bundle.buf)
        print([
            f"MD5 to check: {md5(i).hexdigest()}"
            for i in self._bufs_ready_to_file
        ])

    def event_loop(self):
        while True:
            try:
                # make timeout to be 0.1 to force loop wait this time
                # in case no sockets are ready (allow to aggregate something)
                socks_read, _, _ = select(self.wait_to_read, [], [], 0.1)

                for bundle in socks_read:
                    print(bundle.sock)
                    bundle.func(bundle)
            except KeyboardInterrupt:
                break

    def run(self):
        self.s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_sock.bind((self.host, self.port))
        self.s_sock.listen()
        # make server_socket non blocking (for `accept` method)
        self.s_sock.setblocking(False)

        self.wait_to_read.append(
            SocketBundle(sock=self.s_sock, buf=b'', func=self.accept_connection)
        )
        self.event_loop()


if __name__ == "__main__":

    s = Server(HOST, PORT)
    s.run()