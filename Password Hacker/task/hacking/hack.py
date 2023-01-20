import itertools
import os
import re
import socket
import string
from sys import argv
from typing import Iterable

SUCCESS_MSG = 'Connection success!'


def pick_up(s: socket.socket):
    for pwd in list_iter():
        s.send(pwd.encode())
        if s.recv(100).decode() == SUCCESS_MSG:
            return pwd


def word_iter(word: str) -> Iterable[str]:
    if re.match(r'\d+$', word):
        return [word]
    else:
        return (''.join(prod) for prod in itertools.product(
                *((sym.lower(), sym.upper()) for sym in word)))


def list_iter() -> Iterable[str]:
    with open(os.path.join(os.getcwd(), 'passwords.txt')) as file:
        lines = file.readlines()
    return itertools.chain(*(word_iter(word[:-1]) for word in lines))


def main():
    ip, port, = argv[1], int(argv[2])
    with socket.socket() as s:
        s.connect((ip, port))
        print(pick_up(s))


if __name__ == '__main__':
    main()
