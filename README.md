# TCP Server

This is a simple TCP socket server which can only receive binary data.
It does it asynchronously by using `select` module.
It also implement a simple client counterpart which can send files to the server.

No third party libraries needed. 

## Installation

No explicit installation needed. Simply download either `server.py` or `client.py` or both.

## Usage

### create and run server
server.py
```python
s = Server(HOST, PORT)
s.run()
```

it will start listening on a given host/port pair

### create a client
client.py

```python
c = Client(chunk_size=1024)
c.connect(HOST, PORT)
```

where `chunk_size` is a size of chunk being sent to the server at a time.
by default is equal to 1024.

sending a file:
```python
c.send_file(file_name)
```

`file_name` should be a valid path to a file.


## License
[MIT](https://choosealicense.com/licenses/mit/)







