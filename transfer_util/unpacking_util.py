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
    #---
    print(util.rcv_buffer)
    #---
    frame_no = struct.unpack('!H', packet[1:3])[0]
    cmd_id = struct.unpack('!c', packet[3:4])[0][0]
    if type_flag == util.ACK:
        data = None
        print("---------------------")
        #print(util.window[frame_no].sending_time)
        #print(time.time())
        print(util.window[frame_no].rcv_ack)
        print("---------------------")
        util.window[frame_no].rcv_ack = True
        #print("AM PRIMIT ACK")
        # TODO: chestie fereastra glisanta
        # TODO: util.current_file !!grija sa inchizi fisierul cand primesti ultimul ack
    elif type_flag == util.FILE_CHUNK:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])
        actionQ.put(f'a@f@{frame_no}') # send ack
        # TODO: test------------------------
        if(frame_no==len(util.rcv_buffer)):
            util.rcv_buffer.append(data)
            print("HAAAAAAAAA")
        else:
            while(len(util.rcv_buffer) in util.buf_list_frame[:][1]): #TODO: de verificat aici
                poz = util.buf_list_frame.index(len(util.rcv_buffer))
                util.rcv_buffer.append(util.buf_list_frame[poz][0])
                util.rcv_buffer.append(data)
                print("aici?")
            else:
                elem=[data,frame_no]
                util.buf_list_frame.append(elem)
                print("sau aici?")

        #todo:test------------------------------
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
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
        uiupdateQ.put(data)
        print("AM PRIMIT ACK CMD:\n", data ,"\n")


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
            print("=")
            #todo: se poate incerca testarea lucrurilor ce urmeaza aici
          #   util.rcv_buffer.clear() #curatarea bufferului pentru primire text
          #   util.last_rcv=-1
          #   util.buf_list_frame.clear()
          #   print("REQ MADE")# pana aici
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