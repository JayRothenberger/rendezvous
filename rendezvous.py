import socket
import logging
from time import sleep
from time import perf_counter as time

logger = logging.Logger()
logger.setLevel('INFO')


def main():
    start = time()
    udp_ip = ''
    udp_port = 5555

    while True:
        try:
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP

            sock.bind((udp_ip, udp_port))
            logger.info(f'listening on port: {udp_port}')
            sock.settimeout(15)
            data, (ip, port) = sock.recvfrom(1500)  # buffer size is 1024 bytes
            logger.info(f"received message: {data.decode('ascii')}, {ip}:{port}")

            sock2 = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

            sock2.sendto(b"fuck you :)", (ip, port))

        except OSError as e:
            logger.info(f'{str(e)}, uptime: {time() - start}')