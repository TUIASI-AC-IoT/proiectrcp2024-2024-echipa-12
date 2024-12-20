import subprocess
import os, struct, socket

import transfer_util.util as util
from transfer_util.encoder import packing
from transfer_util.util import uiupdateQ, actionQ, file_buffer, current_file, file_to_transfer
from transfer_util.sliding_window import createBuffer, createWindow


def unpack(packet: bytes, sock:socket.socket, address:tuple[str, int]):
    type_flag = packet[0]
    frame_no = struct.unpack('!H', packet[1:3])[0]
    cmd_id = struct.unpack('!c', packet[3:4])[0][0]
    if type_flag == util.ACK:
        data = None
        #print("AM PRIMIT ACK")
        # TODO: chestie fereastra glisanta
        # TODO: util.current_file !!grija sa inchizi fisierul cand primesti ultimul ack
    elif type_flag == util.ACK_COMMAND:
        data = None
        # TODO: vedem daca dam resend la comenzi
        # if cmd_id == util.UPLOAD_REQ:
        #     util.upload_flag = True
        #print("AM PRIMIT ACK CMD!")
        if cmd_id == util.UPLOAD_REQ:
            util.window_position = 0
            util.sending_buffer = createBuffer(util.file_to_transfer)
            createWindow()
            actionQ.put('f')
    elif type_flag == util.ACK_COMMAND_W_OUTPUT:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
        uiupdateQ.put(data)
        print("AM PRIMIT ACK CMD:\n", data ,"\n")

    elif type_flag == util.FILE_CHUNK:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])
        actionQ.put(f'a@f@{frame_no}') # send ack
        # TODO: chestie fereastra glisanta
        # if frame_no == util.current_frame + 1:
        #     with open(util.path + data, 'ab') as file:
        #         pass
        #util.file_buffer = createBuffer(data)
    elif type_flag == util.COMMAND_W_PARAMS:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
        if cmd_id == util.CD:
            if data != "..":
                util.path = util.path + data + "\\"
                print("path: ", util.path)
            elif data == ".." and util.path != util.ROOT:
                util.path = util.path.rstrip("\\")
                util.path = os.path.dirname(util.path) + "\\"
        elif cmd_id == util.MKDIR:
            os.system(f'mkdir {util.path + data}')
        elif cmd_id == util.RM_RMDIR:
            if os.path.isdir(util.path + data):
                os.removedirs(util.path + data)
                #os.system(f'rmdir "{util.path + data}" /s /q')
            else:
                os.remove(util.path + data)
        elif cmd_id == util.MOVE:
            data.split(' ')
            os.system(f'move f"\"{util.path + data[0]}\"" f"\"{util.ROOT + data[1]}\""')
        elif cmd_id == util.TOUCH:
            with open(util.path + data, 'w') as file:
                pass
        elif cmd_id == util.DOWNLOAD_REQ:
            with open(util.path + data, 'w') as file:
                pass
            util.current_frame = 0
            # TODO: send to sliding window
            pass
        elif cmd_id == util.UPLOAD_REQ:
            #TODO: send to sliding window
          #  util.current_file = open(util.path + data, 'rb')
            print("=======================")
            print(data)
           # util.current_file = open(data, 'wb')
           # sock.sendto(packing(util.ACK, 0, cmd_id, None), address)  # Trimite ACK pt comanda
        actionQ.put(f'a@c@{cmd_id}')
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
            print("ls primit\n", output)
            # trimite ACK pt comanda cu output
            #sock.sendto(packing(util.ACK_COMMAND_W_OUTPUT, 0, cmd_id, output), address)
            actionQ.put(f'a@co@{cmd_id}@{output}')
    return None