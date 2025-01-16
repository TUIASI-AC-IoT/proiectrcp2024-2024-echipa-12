import queue
import socket as sc
import threading as Thread
from transfer_util import threads, util, sending_util
import user_interface
from transfer_util.sliding_window_2 import sw_send

def main():
    scket = sc.socket(sc.AF_INET,
                       sc.SOCK_DGRAM)

    scket.bind((util.client_ip, util.client_port))
    #q=Queue()

    #ui_thread = Thread.Thread(target=threads.make_message, args=())
   # ui_thread = Thread.Thread(target=user_interface.ui, args=())
    sender_thread = Thread.Thread(target=sending_util.send, args=((util.server_ip, util.server_port), scket))
    receiver_thread = Thread.Thread(target=threads.receive_packet, args=(util.server_ip, util.server_port, scket))

    sender_thread.start()
    #ui_thread.start()
    receiver_thread.start()
    user_interface.ui()

    #ui_thread.join()
    print("shutting down...")
    print(util.shutdown_event.is_set())
    sender_thread.join()
    receiver_thread.join()
    scket.close()
    print("Application has been shut down successfully.")

if __name__ == '__main__':
    main()
