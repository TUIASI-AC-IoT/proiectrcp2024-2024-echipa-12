from _ctypes import sizeof
import struct
import util
def packing(flag, frame_number=0b0000_0000, command_id=0b0000_0000, data=None):
    if(data==None):
        data_to_pack=struct.pack('!BhB', flag, frame_number, command_id)
    else:
        data_bytes = bytes(data.encode('utf-8'))
        format_str = f'!BhB{len(data_bytes)}s'
        data_to_pack = struct.pack(format_str, flag, frame_number, command_id, data_bytes)
    return data_to_pack



