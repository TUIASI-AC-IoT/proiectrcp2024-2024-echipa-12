import struct
import util
import os
import impachetare as im


def unpack(packet: bytes):
    type_flag = packet[0]
    frame_no = struct.unpack('!H', packet[1:3])[0]
    # print(util.path, type(util.path))
    cmd_id = struct.unpack('!c', packet[3:4])[0][0]
    if type_flag == util.ACK:
        data = None
        #TODO: ACK LOGIC GOES HERE
    elif type_flag == util.ACK_COMMAND:
        data = None
    elif type_flag == util.ACK_COMMAND_W_OUTPUT:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
    elif type_flag == util.FILE_CHUNK:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])
    elif type_flag == util.COMMAND_W_PARAMS:
        data = struct.unpack(f'{len(packet) - 4}s', packet[4:])[0].decode('utf-8')
        if cmd_id == util.CD:
            if data != "..":
                os.system(f'cd {data}')
                util.path = util.path + data + "\\"
            elif data == ".." and util.path != util.ROOT:
                util.path = os.path.dirname(util.path.removesuffix('\\')) + "\\"
        elif cmd_id == util.MKDIR:
            os.system(f'mkdir {data}')
        elif cmd_id == util.RM_RMDIR:
            if os.path.isdir(util.path + data):
                os.removedirs(util.path + data)
            else:
                os.remove(util.path + data)
        elif cmd_id == util.MOVE:
            data.split(' ')
            os.system(f'move {util.path + data[0]} {util.ROOT + data[1]}')
        elif cmd_id == util.TOUCH:
            with open(util.path + data, 'w') as file:
                pass
    elif type_flag == util.COMMAND_NO_PARAMS:
        #print(cmd_id)
        if cmd_id == util.LS:
            output = os.system(f'DIR /B ' + util.path)
            print(output)


# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.MKDIR, data="salut"))
# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.CD, data="salut"))
# unpack(im.impachetare(util.COMMAND_NO_PARAMS, comand_id=util.LS))
# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.CD, data=".."))
# unpack(im.impachetare(util.COMMAND_W_PARAMS, comand_id=util.RM_RMDIR, data="salut"))
