import socket
import logging as logger
from time import sleep
from time import perf_counter as time
# logger with level info to print to console
logger.basicConfig(level=logger.INFO)
peers_to_match = set()


# returns pairs of distinct elements in iterable that can be casted to list 'distinct' as a set of tuples
def pairs(distinct):
    rax = set()
    distinct = list(distinct)
    if len(distinct) > 1:
        for ind in range(0, len(distinct), 2):
            rax.add((distinct[ind], distinct[ind + 1]))
    return rax


# main function that opens the udp socket server on port 6969
def main():
    start = time()
    match_map = dict()
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
            if data.decode('ascii').startswith('client'):
                if (ip, port) in match_map.keys():
                    sock.sendto(match_map[(ip, port)], (ip, port))
                    continue
            else:
                if (ip, port) in match_map.keys():
                    logger.info(f'{ip}:{port} has left their connection')
                    partner_ip = match_map[(ip, port)].decode('ascii').split(':')[1]
                    partner_port = int(match_map[(ip, port)].decode('ascii').split(':')[2])
                    match_map.pop((ip, port))
                    logger.info(f'removing map entry for partner: {partner_ip}:{partner_port}')
                    match_map.pop((partner_ip, partner_port))
                    sock.sendto(f'you have left the session'.encode('ascii'), (ip, port))
                continue
            d_string = data.decode('ascii')
            m, m_port = tuple(d_string.split(':'))
            logger.info(f"received message: '{data.decode('ascii')}', {ip}:{port}")
            response = 'none yet'
            sock.sendto(response.encode('ascii'), (ip, port))

            logger.info(f"sending message: {response} to {ip}:{port}")
            peers_to_match.add((ip, int(port), int(m_port)))
        except OSError as e:
            pass
            # logger.info(f'{str(e)}, uptime: {time() - start}')
        matches = pairs(peers_to_match)
        if matches:
            for client, server in matches:
                resp_client = f"client:{server[0]}:{server[1]}:{server[2]}".encode('ascii')
                resp_server = f"server:{client[0]}:{client[1]}:{client[2]}".encode('ascii')

                peers_to_match.remove(client)
                peers_to_match.remove(server)

                match_map[client] = resp_client
                match_map[server] = resp_server

                sock.sendto(resp_client, client)
                sock.sendto(resp_server, server)

                logger.info(f'connected: {client}, {server}')
        for peer in peers_to_match:
            sock.sendto('none yet'.encode('ascii'), peer)
            logger.info(f'sending wait message: {peer[0]}:{peer[1]}')


if __name__ == "__main__":
    main()
