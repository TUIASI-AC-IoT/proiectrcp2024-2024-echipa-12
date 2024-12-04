import socket as sc
import threading as Thread
import threads
import user_interfacce
import util

scket = sc.socket(sc.AF_INET,
                   sc.SOCK_DGRAM)

scket.bind((util.client_ip, util.client_port))
#q=Queue()

#ui_thread = Thread.Thread(target=threads.make_message, args=())
ui_thread = Thread.Thread(target=user_interfacce.ui, args=())
sender_thread = Thread.Thread(target=threads.send_packet, args=(util.server_ip, util.server_port, scket))
receiver_thread = Thread.Thread(target=threads.receive_packet, args=(util.server_ip, util.server_port, scket))

sender_thread.start()
ui_thread.start()
receiver_thread.start()

sender_thread.join()
ui_thread.join()
receiver_thread.join()






