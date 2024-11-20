import socket as sc
import threading as Thread
from time import sleep

from pyexpat.errors import messages

import encoder
import util

global_client_message=""
lock = Thread.Lock()
new_message_event = Thread.Event()

def send_packet(udp_ip,udp_port,scket):
    frame_number=0
    global global_client_message
    while (True ):
        new_message_event.wait()
        with lock:
            if(global_client_message!=""):
                mess = encoder.packing(util.FILE_CHUNK, frame_number, 0, global_client_message)
                scket.sendto(mess, (udp_ip, udp_port))
                frame_number+=1
        sleep(3)

def make_message():
    global global_client_message
    while (True):
        with lock:
            print("Alege un numar corespunzator comenzii dorite:")
            print("1.ls")
            print("2.cd")
            print("3.mkdir")
            print("4.rm/rmdir")
            print("5.move")
            val = input()
            if (val == "1"):
                global_client_message = "ls"
            elif (val == "2"):
                global_client_message = "cd"
            elif (val == "3"):
                global_client_message = "mkdir"
            elif (val == "4"):
                global_client_message= "rmdir"
            elif (val == "5"):
                global_client_message = "move"
            else:
                global_client_message = ""
                print("invalid input")
        new_message_event.set()
        sleep(3)
