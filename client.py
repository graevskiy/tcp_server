# import pyaudio

import sys
import socket
import time

from pathlib import Path


# chunk = 1024  # Record in chunks of 1024 samples
# sample_format = pyaudio.paInt16  # 16 bits per sample
# channels = 2
# fs = 44100  # Record at 44100 samples per second


def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 25000))
    return s


def client(s, file, timeout=0):
    try:
        print('file to send:', file)
        f_size = Path(file).stat().st_size
        print('file size:', f_size)        

        print('countdown')        
        for i in range(timeout):
            print(timeout-i)
            time.sleep(1)

        with open(file, 'rb') as f:
            buf = f.read()
        
        print('sending')
        s.send(buf[0:len(buf)//2])
        time.sleep(0.5)
        s.send(buf[len(buf)//2:])
        
    finally:
        print('close connection')
        s.close()


def run_client(socket):
    assert len(sys.argv) == 4
    file = sys.argv[2]
    timeout = int(sys.argv[3])
    
    client(socket, file, timeout)


def run_client_rec(socket):
    client_recording(socket)


def client_recording(socket):
    pass
    # p = pyaudio.PyAudio()  # Create an interface to PortAudio

    # stream = p.open(format=sample_format,
    #                 channels=channels,
    #                 rate=fs,
    #                 frames_per_buffer=chunk,
    #                 input=True)

    # print('Get prepared!')
    # for i in range(3):
    #     time.sleep(1)
    #     print(3 - i)

    # print('Start Recording')

    # # recording 5 seconds
    # n = 0
    # with open('aaa.wav', 'wb') as f:
    #     for i in range(0, int(fs / chunk * 5)):
    #         if i % 1024 == 0:
    #             n += 1
    #             print(n)
    #         data = stream.read(chunk)
    #         f.write(data)
    #         socket.send(data)


    # stream.stop_stream()
    # p.terminate()
    # print('Finished recording')
    # socket.close()

if __name__ == "__main__":
    
    assert len(sys.argv) >= 2

    runner_dict = {
        'client': run_client,
        'client_rec': run_client_rec
    }

    assert sys.argv[1] in runner_dict

    socket = create_socket()
    runner_dict[sys.argv[1]](socket)
    
