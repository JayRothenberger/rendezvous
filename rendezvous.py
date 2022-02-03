import socket
import logging as logger
from time import sleep
from time import perf_counter as time

logger.basicConfig(level=logger.INFO)
peers_to_match = set()


def pairs(distinct):
    rax = set()
    distinct = list(distinct)
    for ind in range(0, len(distinct), 2):
        rax.add((distinct[ind], distinct[ind+1]))
    return rax


def main():
    start = time()
    udp_ip = ''
    udp_port = 6969

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    sock.settimeout(5)
    logger.info(f'listening on port: {udp_port}')
    while True:
        try:
            data, (ip, port) = sock.recvfrom(1500)  # buffer size is 1500 bytes
            logger.info(f"received message: {data.decode('ascii')}, {ip}:{port}")
            response = 'none yet'
            sock.sendto(response.encode('ascii'), (ip, udp_port))
            logger.info(f"sending message: {response} to {ip}:{port}")
        except OSError as e:
            pass
            #logger.info(f'{str(e)}, uptime: {time() - start}')
        matches = pairs(peers_to_match)
        for client, server in matches:
            resp_client = f"client:{client[0]}:{client[1]}".encode('ascii')
            sock.sendto(resp_client, client)
            resp_server = f"server:{server[0]}:{server[1]}".encode('ascii')
            sock.sendto(resp_server, server)
            peers_to_match.remove(client)
            peers_to_match.remove(server)
            logger.info(f'connected: {client}, {server}')
        for peer in peers_to_match:
            sock.sendto('none yet'.encode('ascii'), peer)
            logger.info(f'sending wait message: {peer[0]}:{peer[1]}')

if __name__ == "__main__":
	main()
