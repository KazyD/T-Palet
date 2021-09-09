import sys
import socket

def main(host, port):
    for i in range(10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(('Hello i=%d' % i).encode())
        data = s.recv(1024)
        s.close()
        print('received: [%s]\n' % (data.decode()))

if __name__ == '__main__':
    main('127.0.0.1', 5000)
