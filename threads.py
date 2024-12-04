import socket as sc
import threading as Thread
import time
from time import sleep
from unpacking_util import unpack
import encoder, queue
import util
from util import actionQ

lock = Thread.Lock()
new_message_event = Thread.Event()

def send_packet(udp_ip, udp_port, scket):
    #frame_number=0

    scket.sendto(encoder.packing(util.COMMAND_NO_PARAMS, 0, util.LS), (udp_ip, udp_port))
    print("a fost primu ls")
    while (True ):
        message = ""
        #new_message_event.wait()
        #print(actionQ.get())
        if not util.actionQ.qsize()!=0:
            message = util.actionQ.get()
            print(message)
        with lock:
            if(message!=""):
                msg=message.split("@")
                print('mesaj', msg)
                if(msg[0] == "ls"):
                    #print(util.path)
                    mess = encoder.packing(util.COMMAND_NO_PARAMS, 0, util.LS)
                elif(msg[0] == "cd"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.CD, msg[1])
                    #scket.sendto(mess, (udp_ip, udp_port))
                    #mess = encoder.packing(util.COMMAND_NO_PARAMS, 0, util.LS)
                elif(msg[0] == "rmdir"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0,command_id=util.RM_RMDIR, data=msg[1])
                elif(msg[0] == "mkdir"):
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0,command_id=util.MKDIR, data=msg[1])
                print("sending message...")
                print("am trimis mesajul", mess)
                scket.sendto(mess, (udp_ip, udp_port))
                message = ""
                #frame_number+=1


def make_message():
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
                util.actionQ.put("ls")
            elif (val == "2"):
                args = input("introduceti nume folder sau .. pt back: ")
                mess="cd@"+args
                util.actionQ.put(mess)
            elif (val == "3"):
                args = input("introduceti nume folder: ")
                mess = "mkdir@" + args
                util.actionQ.put(mess)
            elif (val == "4"):
                args = input("introduceti nume folder: ")
                mess = "rmdir@" + args
                util.actionQ.put(mess)
            elif (val == "5"):
                args = input("introduceti nume folder + locatia (teoretic functional dar ar trebui lucrat sa mearga pt ui): ")
                mess = "move@" + args
                util.actionQ.put(mess)
            else:
                print("invalid input")
        #new_message_event.set()
        sleep(3)

def receive_packet(udp_ip, udp_port, scket:sc.socket):
    while True:
        pct, addr = scket.recvfrom(1024)
        a = unpack(pct, scket, (udp_ip, udp_port))
