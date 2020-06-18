import io
import socket
import uuid

from collections import defaultdict
from hashlib import md5
from select import select


HOST = '127.0.0.1'
PORT = 25000

wait_to_read = []
wait_to_write = []
bufs = defaultdict(bytes)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.setblocking(False)
    return server_socket


def accept_wrapper(server_socket):
    client, address = server_socket.accept()                    
    print('Connection from', address)

    wait_to_read.append(client)


# for checking purposes only
def send_msg(client):
    req = client.recv(1024)
    if req:
        response = 'Hi there\n'.encode()
        client.send(response)
    else:
        wait_to_read.remove(client)
        client.close()


def handler_wav(client):
    req = client.recv(1024)
    bufs[client.fileno()] += req
    print(len(req))
    if not req:
        print('no req, closing')
        wait_to_read.remove(client)
        hash_sum = md5(bufs[client.fileno()]).hexdigest()
        print('MD5 to check:', hash_sum)
        client.close() # is blocking? need to do smth


def event_loop(server_socket):
    while True:
        socks_read, socks_write, _ = select(wait_to_read, wait_to_write, [])

        for sock in socks_read:
            print(sock)
            if sock is server_socket:
                accept_wrapper(sock)
            else:
                handler_wav(sock)


if __name__ == "__main__":
    s = server()
    wait_to_read.append(s)
    event_loop(s)