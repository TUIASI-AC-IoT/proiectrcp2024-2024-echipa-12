import subprocess

import util, os, struct, socket
from encoder import packing

class Packet:
    def __init__(self, typeflag, frameno, cmdid, data):
        self.typeflag = typeflag
        self.frameno = frameno
        self.cmdid = cmdid
        self.data = data

def unpack(packet: bytes, sent:list[Packet], sock:socket.socket, address:tuple[str, int]):
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
        print("AM PRIMIT ACK CMD ", data)
        return data
    elif type_flag == util.FILE_CHUNK:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])
        #TODO: chestie fereastra glisanta
    elif type_flag == util.COMMAND_W_PARAMS:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
        if cmd_id == util.CD:
            if data != "..":
                os.system(f'cd {data}')
                util.path = util.path + data + "\\"
            elif data == ".." and util.path != util.ROOT:
                util.path = os.path.dirname(util.path.removesuffix('\\')) + "\\\""
        elif cmd_id == util.MKDIR:
            os.system(f'mkdir {data}')
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
        sock.sendto(packing(util.ACK, 0, cmd_id, 0), address)
    elif type_flag == util.COMMAND_NO_PARAMS:
        #print(cmd_id)
        if cmd_id == util.LS:
            command = f'DIR /B "{util.path}"'
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            output = result.stdout
            #os.system(f'DIR /B ' + f"\"{util.path}\"")
            #data = output
            #print(output, " ", type(output))
            print("primit comanda, dau ack")
            sock.sendto(packing(util.ACK_COMMAND_W_OUTPUT, 0, cmd_id, output), address)


# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.MKDIR, data="salut"))
# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.CD, data="salut"))
# unpack(im.impachetare(util.COMMAND_NO_PARAMS, comand_id=util.LS))
# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.CD, data=".."))
# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.RM_RMDIR, data="salut"))
