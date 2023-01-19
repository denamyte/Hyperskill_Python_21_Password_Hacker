import itertools
import socket
import string
from sys import argv

SUCCESS_MSG = 'Connection success!'
get_set = lambda: itertools.chain(string.ascii_lowercase, string.digits)


def main():
    ip, port, = argv[1], int(argv[2])
    with socket.socket() as s:
        s.connect((ip, port))
        print(bruteforce(s))


def bruteforce(s: socket.socket):
    for repeat in range(1, 5):
        passwords = (''.join(prod) for prod
                     in itertools.product(get_set(), repeat=repeat))
        for pwd in passwords:
            s.send(pwd.encode())
            if s.recv(100).decode() == SUCCESS_MSG:
                return pwd


if __name__ == '__main__':
    main()
