import queue
import threading
from socket import socket
from time import sleep

import transfer_util.encoder as encoder
import transfer_util.util as util
from transfer_util import threads
from transfer_util.sliding_window_2 import sw_send
from transfer_util.util import actionQ


def send(address:[str, int], scket:socket) -> None:
    while True:
        if util.shutdown_event.is_set():
            print("oprim send")
            break
        message = ""
        try:
            message = util.actionQ.get(timeout=1.0)#timeout=1.0
        except queue.Empty:
            #print("Queue is empty")
            message = ""
            continue
       # except tu

        #message = actionQ.get()
        if message != "":
            msg = message.split("@")
            #print(msg)
            #msg[0] va fi tipul pachetului:
            #         - f = file
            #         - a = ack
            #         - c = command

            if msg[0] == "f":
                fereastra = threading.Thread(target=sw_send, args=(scket,address), daemon=True)
                fereastra.start()
                # print("pun in coada")
                # util.slideQ.put(1)
                mess = ''
                #print("fereastra e gata!")
            elif msg[0] == "a":
                ack_type = msg[1]
                if ack_type == "c": #command
                    mess = encoder.packing(util.ACK_COMMAND, 0, int(msg[2]))
                elif ack_type == "co": #command with output
                    mess = encoder.packing(util.ACK_COMMAND_W_OUTPUT, 0, int(msg[2]), msg[3])
                elif ack_type == "f": #file chunk
                    mess = encoder.packing(util.ACK, int(msg[2]), 0, None)
                    # mess = ''
                # print("sending message...")
                # print("am trimis mesajul", mess)
                # scket.sendto(mess, address)
            elif msg[0] == "c":
                cmd = msg[1]
                data = msg[2] if len(msg) > 2 else None
                if cmd == "ls":
                    mess = encoder.packing(util.COMMAND_NO_PARAMS, 0, util.LS)
                elif cmd == "cd":
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.CD, data)
                elif cmd == "rmdir":
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.RM_RMDIR, data)
                elif cmd == "mkdir":
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.MKDIR, data)
                elif cmd == "up":
                    data = f'{msg[2]}@{msg[3]}'#FILENAME, SIZE
                    #print(data)
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.UPLOAD_REQ, data)
                elif cmd == "down":
                    data = msg[2] #filename
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.DOWNLOAD_REQ, data)
                elif cmd == "cs":
                    data = f'{msg[2]}@{msg[3]}'
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.CHG_SETTING, data)
                    #print("cs")
                # print("sending message...")
                # print("am trimis mesajul", mess)
                # scket.sendto(mess, address)

            # elif (msg[0] == "ack"):
            #     mess = encoder.packing(ACK_COMMAND, 0, command_id=util.ACK, data=msg[1])
            if mess != "":
               # print("sending message...")
               # print("am trimis mesajul", mess)
                scket.sendto(mess, address)