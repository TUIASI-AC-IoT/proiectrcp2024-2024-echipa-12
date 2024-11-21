import socket as sc
import threading as Thread
from time import sleep

from openpyxl.styles.builtins import comma
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
                msg = global_client_message.split("@")
                if(msg[0] == "ls"):
                    mess = encoder.packing(util.COMMAND_NO_PARAMS, 0, util.LS)
                elif(msg[0] == "cd"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.CD, msg[1])
                elif(msg[0] == "rmdir"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0,command_id=util.RM_RMDIR, data=msg[1])
                elif(msg[0] == "mkdir"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0,command_id=util.MKDIR, data=msg[1])
                print("sending message...")
                scket.sendto(mess, (udp_ip, udp_port))
                global_client_message = ''
                #frame_number+=1


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
                args = input("introduceti nume folder sau .. pt back: ")
                global_client_message = "cd@"+args
            elif (val == "3"):
                args = input("introduceti nume folder: ")
                global_client_message = "mkdir@"+args
            elif (val == "4"):
                args = input("introduceti nume folder: ")
                global_client_message= "rmdir@" + args
            elif (val == "5"):
                args = input("introduceti nume folder + locatia (teoretic functional dar ar trebui lucrat sa mearga pt ui): ")
                global_client_message = "move@"+args
            else:
                global_client_message = ""
                print("invalid input")
        new_message_event.set()
        sleep(3)
