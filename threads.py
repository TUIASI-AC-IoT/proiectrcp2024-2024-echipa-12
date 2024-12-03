import socket as sc
import threading as Thread
from time import sleep
from unpacking_util import unpack
from pyexpat.errors import messages

import encoder
import util

#global_client_message=""
lock = Thread.Lock()
new_message_event = Thread.Event()

def send_packet(q,udp_ip,udp_port,scket):
    #frame_number=0
    while (True ):
        message = ""
        new_message_event.wait()
        if (not q.empty()):
            message = q.get()
        with lock:
            if(message!=""):
                msg=message.split("@")
                if(msg[0] == "ls"):
                    #print(util.path)
                    mess = encoder.packing(util.COMMAND_NO_PARAMS, 0, util.LS)
                elif(msg[0] == "cd"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.CD, msg[1])
                elif(msg[0] == "rmdir"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0,command_id=util.RM_RMDIR, data=msg[1])
                elif(msg[0] == "mkdir"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0,command_id=util.MKDIR, data=msg[1])
                print("sending message...")
                scket.sendto(mess, (udp_ip, udp_port))
                message = ""
                #frame_number+=1


def make_message(q):
    #global global_client_message
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
                q.put("ls")
            elif (val == "2"):
                args = input("introduceti nume folder sau .. pt back: ")
                mess="cd@"+args
                q.put(mess)
            elif (val == "3"):
                args = input("introduceti nume folder: ")
                mess = "mkdir@" + args
                q.put(mess)
            elif (val == "4"):
                args = input("introduceti nume folder: ")
                mess = "rmdir@" + args
                q.put(mess)
            elif (val == "5"):
                args = input("introduceti nume folder + locatia (teoretic functional dar ar trebui lucrat sa mearga pt ui): ")
                mess = "move@" + args
                q.put(mess)
            else:
                print("invalid input")
        new_message_event.set()
        sleep(3)

def receive_packet(q, udp_ip, udp_port, scket):
    while (True ):
        pct = scket.recvfrom(1024)
        unpack(pct, None, scket, (udp_ip, udp_port))
