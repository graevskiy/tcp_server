import io
import selectors
import socket
import uuid

from select import select

HOST = '127.0.0.1'
PORT = 25000

wait_read = []
wait_write = []

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    return server_socket


def accept_wrapper(server_socket):

    print('Before .accept()')
    client, address = server_socket.accept()                    
    print('Connection from', address)

    wait_read.append(client)


def send_msg(client):
           
    print('Before .recv()')
    req = client.recv(4096)
    if req:
        response = 'Hi there\n'.encode()
        client.send(response)
    else:
        client.close()


def handler_wav(client):
    filesize = client.recv(2048)        
    with open(str(uuid.uuid4()) + '.wav', 'wb') as f:
        while True:
            req = client.recv(int(filesize))
            if not req:
                break
            f.write(req)
            client.sendall(b'Received')                
        client.close()
        print('Closed connection')


def event_loop(server_socket):
    while True:
        socks_read, socks_write, _ = select(wait_read, wait_write, [])

        for sock in socks_read:
            if sock is server_socket:
                accept_wrapper(sock)
            else:
                send_msg(sock)


if __name__ == "__main__":    
    s = server()
    wait_read.append(s)
    event_loop(s)