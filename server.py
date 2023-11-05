import socket, sys, time
from threading import Thread
from queue import Queue


def producer_worker():
    connection_pro, address_pro = sc_pro.accept()
    print("[Producer connected]")
    try:
        while True:
            msg = connection_pro.recv(100).decode()
            for i in msg:
                queue_events.put(i)
            if msg:
                print("[Events created]")
                print("[Remain events: " + str(queue_events.qsize()) + "]")
    except socket.error:
        connection_pro.close()
        sys.exit()

def consumer_worker(consumer_id):
    try:
        connection_con, address_con = sc_con.accept()
        list_consumers.append(connection_con)
        consumer_id_str = str(consumer_id)
        print("[consumer "+consumer_id_str+" connected]")
        print("["+str(len(list_consumers))+" consumers online]")
        connection_con.send(consumer_id_str.encode())
            
        while True:
            if not queue_events.empty():
                msg = queue_events.get()
                connection_con.send(msg.encode())
                print("[Remain events: " + str(queue_events.qsize()) + "]")
            else:
                connection_con.send("EMPTY".encode())
            time.sleep(1)
                
    except socket.error:
        print("[Consumer "+consumer_id_str+" disconnected]")
        list_consumers.remove(connection_con)
        print("["+str(len(list_consumers))+" consumers online]")
        connection_con.close()
        

if __name__ == '__main__':
    try:
        queue_events = Queue()
        host, port_pro_str, port_con_str = input().split()
        port_pro = int(port_pro_str)
        port_con = int(port_con_str)
                
        sc_pro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc_pro.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        sc_pro.bind((host, port_pro))
        sc_pro.listen(5)
                
        sc_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc_con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sc_con.bind((host, port_con))
        sc_con.listen(socket.SOMAXCONN-10)
            
        producer_thread = Thread(target=producer_worker)
        producer_thread.start()
            
        consumer_id = 0
        list_consumers = list()
        i = 0
        while i < socket.SOMAXCONN-10:
                consumer_id += 1
                i += 1
                worker_thread = Thread(target=consumer_worker, args=(consumer_id,))
                worker_thread.start()
    except KeyboardInterrupt:
        list_consumers.clear()
        sc_pro.close()
        sc_con.close()
        sys.exit(0)
