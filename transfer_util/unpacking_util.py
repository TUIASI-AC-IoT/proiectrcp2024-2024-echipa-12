import subprocess
import os, struct, socket
import time
import shutil
import transfer_util.util as util
from transfer_util.encoder import packing
from transfer_util.util import uiupdateQ, actionQ, file_buffer, current_file, file_to_transfer
from transfer_util.sliding_window_2 import createBuffer, createWindow


def unpack(packet: bytes, sock:socket.socket, address:tuple[str, int]):
    type_flag = packet[0]
    frame_no = struct.unpack('!I', packet[1:5])[0]
    cmd_id = struct.unpack('!c', packet[5:6])[0][0]
    #print("fn= ",frame_no)
    #print("fn= ", cmd_id)
    #print("fn= ", type_flag)
    if type_flag == util.ACK:
        data = None
        util.window[frame_no].rcv_ack = True
        #print("AM PRIMIT ACK")
        # TODO: chestie fereastra glisanta
        # TODO: util.current_file !!grija sa inchizi fisierul cand primesti ultimul ack
    elif type_flag == util.FILE_CHUNK:
        data = struct.unpack(f'{len(packet) - 6}s', packet[6:])
        actionQ.put(f'a@f@{frame_no}') # send ack

        # creare buffer cu elementele transmise prin fereastra glisanta
        if(frame_no>=util.last_frame_bf+1 and frame_no<=util.last_frame_bf+util.window_size):
            util.rcv_buffer[frame_no] = data
        while(util.last_frame_bf<util.rcv_buffer_size and util.rcv_buffer[util.last_frame_bf+1] is not None ):
             #todo: and util.last_frame_bf+util.window_size<=numarul de elemente din bufferul trimis
            util.last_frame_bf+=1
        #print(f"\n\n\n{frame_no, util.last_frame_bf, util.rcv_buffer_size}\n\n\n")
        if util.rcv_buffer_size == util.last_frame_bf:
         #   print("\n\n\t\t\t\tam scris\n\n")
            with open(os.path.join(util.path, util.rcv_filename), 'wb') as file:
                for i in util.rcv_buffer:
                    file.write(i[0])
                    #print(i[0])
                    #print(type(i[0]))
                #file.write('\0')
                file.close()
            print("am scris")
        #---------

        # if frame_no == util.current_frame + 1:
        #     with open(util.path + data, 'ab') as file:
        #         pass
        #util.file_buffer = createBuffer(data)
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
        data = struct.unpack(f'{len(packet) - 6}s', packet[6:])[0].decode('utf-8')
        uiupdateQ.put(data)
        print("AM PRIMIT ACK CMD:\n", data ,"\n")


    elif type_flag == util.COMMAND_W_PARAMS:
        data = struct.unpack(f'{len(packet) - 6}s', packet[6:])[0].decode('utf-8')
        if cmd_id == util.CD:
            if data != "..":
                util.path = util.path + data + "\\"
                print("path: ", util.path)
            elif data == ".." and util.path != util.ROOT:
                util.path = util.path.rstrip("\\")
                util.path = os.path.dirname(util.path) + "\\"
        elif cmd_id == util.MKDIR:
            print(data)
            os.system(f'mkdir \"{util.path + data}\"')
        elif cmd_id == util.RM_RMDIR:
            print("\n\n\n\n\nrm_rmdir:", os.path.join(util.path, data))
            full_path = os.path.join(util.path, data)
            if os.path.isfile(full_path):  # Check if it's a file
                os.remove(full_path)
            elif os.path.isdir(full_path):  # Check if it's a directory
                if not os.listdir(full_path):  # Check if the directory is empty
                    os.rmdir(full_path)
                else:
                    shutil.rmtree(full_path)
            #if os.path.isdir(os.path.join(util.path, data)):
            #if os.path.isdir(util.path + data):
            #    shutil.rmtree(util.path + data)
               # os.removedirs(util.path + data)
                #os.system(f'rmdir "{util.path + data}" /s /q')
            else:
                print('fiser')
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
            filename, filesize = data.split('@')
            util.rcv_buffer=[None]*(int(filesize)) #TODO:FOARTE IMPORTANT: in loc de 40 o sa se puna nr de frame-uri ce vor veni
            util.last_frame_bf = -1
            util.rcv_buffer_size = int(filesize)-1
            util.rcv_filename = filename

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
            # print("ls primit\n", output)
            # trimite ACK pt comanda cu output
            #sock.sendto(packing(util.ACK_COMMAND_W_OUTPUT, 0, cmd_id, output), address)
            actionQ.put(f'a@co@{cmd_id}@{output}')

    return None
