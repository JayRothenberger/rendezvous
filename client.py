import socket
import time
from random import randrange as random

peer_ip, peer_port, peer_private = None, None, None

role = None

server_ip, server_port = '74.208.187.224', 6969
my_port = random(6000, 7000)
print(f'my port is: {my_port}')

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind(('', my_port))
print(f'bound socket to: {my_port}')


def send(message, ip, port):
    print(f'sending "{message}" to {ip}:{port}')
    sock.sendto(message.encode('ascii'), (ip, port))


def get_peer_info():
    send(f"client:{my_port}", server_ip, server_port)
    return sock.recvfrom(1500)


def greet_peer():
    send(f'greetings, {role}', peer_ip, peer_port)
    send(f'greetings, {role}', peer_ip, peer_private)
    return sock.recvfrom(1500)


sock.settimeout(5)

while True:
    try:
        if peer_ip is None:
            response, (addr, p) = get_peer_info()
            resp_str = response.decode('ascii')
        else:
            response, (addr, p) = greet_peer()
            resp_str = response.decode('ascii')
            if addr == peer_ip:
                print(f'got message from {addr}:{p}!')
                continue

        time.sleep(1)

        print(f'response from {addr}:{p} : "{resp_str}"')

        if resp_str.startswith('client') or resp_str.startswith('server'):
            role, peer_ip, peer_port, peer_private = tuple(response.decode('ascii').split(':'))
            peer_port = int(peer_port)
            peer_private = int(peer_private)
            sock.bind((peer_ip, my_port))
            sock.settimeout(1)
    except OSError as e:
        print('reset')
