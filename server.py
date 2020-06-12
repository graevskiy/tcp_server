import io
import selectors
import socket
import uuid


def server():
    selector = selectors.DefaultSelector()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 25000))
    server_socket.listen(5)
    server_socket.setblocking(False)
    selector.register(server_socket, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                client, address = server_socket.accept()
                client.setblocking(False)
                handler(client)
                # Thread(target=handler, args=(client,)).start()
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt raised")
    finally:
        selector.close()


def handler(client):
    print("Connected to ", client)
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


if __name__ == "__main__":    
    server()