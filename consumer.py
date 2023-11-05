import socket, time
import sys

host, port_str = input().split()
port = int(port_str)

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect((host, port))
consumer_id_str = sc.recv(100).decode()
print("Connected, consumer " + consumer_id_str)

try:
    while True:
        sc.send('give me message'.encode())
        msg = sc.recv(100).decode()
        if msg=="EMPTY":
            print("No event in queue")
        else:
            print("Event "+ msg + " is processed in consumer "+ consumer_id_str)
        time.sleep(1)
except KeyboardInterrupt:
    sc.close()
    sys.exit()