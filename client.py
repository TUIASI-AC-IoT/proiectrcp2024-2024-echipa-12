import socket as sc
import threading as Thread
from queue import Queue
import threads
import util

scket = sc.socket(sc.AF_INET,
                   sc.SOCK_DGRAM)

q=Queue()

ui_thread = Thread.Thread(target=threads.make_message, args=(q, ))
sender_thread = Thread.Thread(target=threads.send_packet, args=(q, util.server_ip, util.server_port, scket))
receiver_thread = Thread.Thread(target=threads.receive_packet, args=(q, util.server_ip, util.server_port, scket))

sender_thread.start()
ui_thread.start()
sender_thread.join()
ui_thread.join()






