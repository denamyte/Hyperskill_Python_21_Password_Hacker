import socket
from sys import argv


def main():
    ip, port, message = argv[1], int(argv[2]), argv[3]
    with socket.socket() as s:
        s.connect((ip, port))
        s.send(message.encode())
        b_resp = s.recv(1024)
        print(b_resp.decode())


if __name__ == '__main__':
    main()
