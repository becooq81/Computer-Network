import socket, time
import sys

host, port_str = input().split()
port = int(port_str)

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect((host, port))
print("Connected, producer")

try:
    while True:
        events = input()
        print(str(len(events)) + " events are created")
        sc.send(events.encode())
except KeyboardInterrupt:
    sc.close()
    sys.exit()