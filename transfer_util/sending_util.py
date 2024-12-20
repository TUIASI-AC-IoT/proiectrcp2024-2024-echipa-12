import queue
import threading
from socket import socket
from time import sleep

import transfer_util.encoder as encoder
import transfer_util.util as util
from transfer_util.sliding_window import sw_send
from transfer_util.util import actionQ


def send(address:[str, int], scket:socket) -> None:
    while True:
        message = ""
        try:
            message = util.actionQ.get()
        except queue.Empty:
            #print("Queue is empty")
            message = ""
        #message = actionQ.get()
        if message != "":
            msg = message.split("@")
            #msg[0] va fi tipul pachetului:
            #         - f = file
            #         - a = ack
            #         - c = command

            if msg[0] == "f":
                #TODO: here lays the sliding window for file transfer
                fereastra = threading.Thread(target=sw_send, args=(util.window,util.sending_buffer,util.window_position,scket,address))
                fereastra.start()
                mess = ''
                fereastra.join()
            elif msg[0] == "a":
                ack_type = msg[1]
                if ack_type == "c": #command
                    mess = encoder.packing(util.ACK_COMMAND, 0, int(msg[2]))
                elif ack_type == "co": #command with output
                    mess = encoder.packing(util.ACK_COMMAND_W_OUTPUT, 0, int(msg[2]), msg[3])
                elif ack_type == "f": #file chunk
                   # mess = encoder.packing(util.ACK_COMMAND, int(msg[2]), 0, None)
                    mess = ''
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
                    mess = encoder.packing(util.COMMAND_W_PARAMS, 0, util.UPLOAD_REQ, data)
                # print("sending message...")
                # print("am trimis mesajul", mess)
                # scket.sendto(mess, address)

            # elif (msg[0] == "ack"):
            #     mess = encoder.packing(ACK_COMMAND, 0, command_id=util.ACK, data=msg[1])
            if mess != "":
                print("sending message...")
                print("am trimis mesajul", mess)
                scket.sendto(mess, address)