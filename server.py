import socket as sc
import threading
import queue
import unpacking_util as up

def send():#q, s, socket, address):
    pass

def rcv(q, s, socket, address):
    while True:
        data, addr = socket.recvfrom(1024)
        up.unpack(data, None, socket, address)
        print("AM PRIMIT UN MESAJ %s: " % data)
        print("de la:", addr)


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

clip = "127.0.0.1"
clport = 5005

socket = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
socket.bind((UDP_IP, UDP_PORT))

print("SERVER STARTED!")

q = queue.Queue()
sent = queue.Queue()

sender = threading.Thread(target=send, args=())#q, sent, socket, (UDP_IP, clport)))
receiver = threading.Thread(target=rcv, args=(q, sent, socket, (UDP_IP, clport)))
sender.start()
receiver.start()
sender.join()
receiver.join()

# while True:
#     #data = ''

#