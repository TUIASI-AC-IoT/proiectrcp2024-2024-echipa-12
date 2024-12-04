import subprocess
import time

import util, os, struct, socket
from encoder import packing
from util import ackQ, filechunkQ, uiupdateQ

def unpack(packet: bytes, sock:socket.socket, address:tuple[str, int]):
    type_flag = packet[0]
    frame_no = struct.unpack('!H', packet[1:3])[0]
    cmd_id = struct.unpack('!c', packet[3:4])[0][0]
    if type_flag == util.ACK:
        data = None
        print("AM PRIMIT ACK")

    elif type_flag == util.ACK_COMMAND:
        data = None
        print("AM PRIMIT ACK CMD!")

    elif type_flag == util.ACK_COMMAND_W_OUTPUT:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
        uiupdateQ.put(data)
        #print("AM PRIMIT ACK CMD ", data)

    elif type_flag == util.FILE_CHUNK:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])
        sock.sendto(packing(util.ACK, frame_no, 0, None), address)
        #TODO: chestie fereastra glisanta

    elif type_flag == util.COMMAND_W_PARAMS:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
        if cmd_id == util.CD:
            if data != "..":
                util.path = util.path + data + "\\"
                print(util.path)
            elif data == ".." and util.path != util.ROOT:
                util.path = util.path.rstrip("\\")
                util.path = os.path.dirname(util.path) + "\\"
        elif cmd_id == util.MKDIR:
            os.system(f'mkdir {util.path + data}')
        elif cmd_id == util.RM_RMDIR:
            if os.path.isdir(util.path + data):
                os.removedirs(util.path + data)
            else:
                os.remove(util.path + data)
        elif cmd_id == util.MOVE:
            data.split(' ')
            os.system(f'move f"\"{util.path + data[0]}\"" f"\"{util.ROOT + data[1]}\""')
        elif cmd_id == util.TOUCH:
            with open(util.path + data, 'w') as file:
                pass
        sock.sendto(packing(util.ACK, 0, cmd_id, None), address) # Trimite ACK pt comanda
    elif type_flag == util.COMMAND_NO_PARAMS:
        if cmd_id == util.LS:
            #command = f'DIR /B {util.path}'

            #aflam foldere din directorul curent
            folder_command = f'for /f "tokens=*" %i in (\'dir /b /a:d "{util.path}"\') do @echo Folder: %i'
            folder_result = subprocess.run(folder_command, shell=True, text=True, capture_output=True)
            #aflam fisiere din directorul curent
            file_command = f'for /f "tokens=*" %i in (\'dir /b /a:-d "{util.path}"\') do @echo File: %i'
            file_result = subprocess.run(file_command, shell=True, text=True, capture_output=True)

            #combinam totul
            output = folder_result.stdout + file_result.stdout

            print("primit comanda, dau ack")
            print('out', output , "pth", util.path)
            sock.sendto(packing(util.ACK_COMMAND_W_OUTPUT, 0, cmd_id, output), address)
            #trimite ACK pt comanda cu output
    return None