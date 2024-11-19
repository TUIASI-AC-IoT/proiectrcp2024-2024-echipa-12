from _ctypes import sizeof
import struct
import util
def impachetare(flag,frame_number=0b0000_0000,comand_id=0b0000_0000,data=None):
    if(data==None):
        data_to_pack=struct.pack('BBB',flag,frame_number,comand_id)
        #print(data_to_pack)
    else:
        data_bytes = bytes(data.encode('utf-8'))
        format_str = f'BBB{len(data_bytes)}s'
        data_to_pack = struct.pack(format_str, flag, frame_number, comand_id,data_bytes)
        #print(data_to_pack)
    return data_to_pack

impachetare(util.ACK,253,3,"cd ceva")


