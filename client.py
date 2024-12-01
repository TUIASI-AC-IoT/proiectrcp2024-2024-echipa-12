import socket as sc
import threading as Thread
from queue import Queue
from time import sleep
import threads

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
scket = sc.socket(sc.AF_INET,
                   sc.SOCK_DGRAM)

q=Queue()

rcv_thread = Thread.Thread(target=threads.make_message, args=(q,))
sender_thread = Thread.Thread(target=threads.send_packet, args=(q,UDP_IP,UDP_PORT,scket))
sender_thread.start()
rcv_thread.start()
sender_thread.join()
rcv_thread.join()






