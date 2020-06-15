import io
import socket
import uuid

from select import select

HOST = '127.0.0.1'
PORT = 25000

wait_to_read = []
wait_to_write = []


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    return server_socket


def accept_wrapper(server_socket):
    client, address = server_socket.accept()                    
    print('Connection from', address)

    wait_to_read.append(client)


# for checking purposes only
def send_msg(client):           
    req = client.recv(4096)
    if req:
        response = 'Hi there\n'.encode()
        client.send(response)
    else:
        wait_to_read.remove(client)
        client.close()


def handler_wav(client):
    with open(str(uuid.uuid4()) + '.wav', 'wb') as f:
        n = 0
        while True:            
            req = client.recv(4096)
            n += len(req)
            print(n, len(req))
            f.write(req)
            if len(req) < 4096:
                break
    wait_to_read.remove(client)
    client.send(b'All done')
    client.close()        
    print('Closed connection')


def event_loop(server_socket):
    while True:
        socks_read, socks_write, _ = select(wait_to_read, wait_to_write, [])

        for sock in socks_read:
            print(sock)
            if sock is server_socket:
                accept_wrapper(sock)
            else:
                # send_msg(sock)
                handler_wav(sock)


if __name__ == "__main__":
    s = server()
    wait_to_read.append(s)
    event_loop(s)