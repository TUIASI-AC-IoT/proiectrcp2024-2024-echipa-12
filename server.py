import socket as sc
import threading
import queue
from transfer_util import util, unpacking_util as up
import transfer_util.sending_util as sending_util
from transfer_util.util import client_ip, client_port

def send():#q, s, socket, address):
    pass

def rcv(q, s, sock, address):
    while True:
        data, addr = sock.recvfrom(1035)
        a = up.unpack(data)
        #print("AM PRIMIT UN MESAJ %s: " % data)
        #print("de la:", addr)

socket = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
socket.bind((util.server_ip, util.server_port))

print("SERVER STARTED!")

q = queue.Queue()
sent = queue.Queue()

sender = threading.Thread(target=sending_util.send, args=((util.client_ip, client_port), socket))#q, sent, socket, (UDP_IP, clport)))
receiver = threading.Thread(target=rcv, args=(q, sent, socket, (util.client_ip, util.client_port)))
sender.start()
receiver.start()
sender.join()
receiver.join()

# while True:
#     #data = ''

#