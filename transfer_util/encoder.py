import struct

def packing(flag, frame_number=0b0000_0000, command_id=0b0000_0000, data=None):
    if(data==None):
        data_to_pack=struct.pack('!BHB', flag, frame_number, command_id)
    else:
        if type(data) != bytes:
            data_bytes = bytes(data.encode('utf-8'))
        else:
            data_bytes = data
        format_str = f'!BHB{len(data_bytes)}s'
        #print(type(data_bytes))
        data_to_pack = struct.pack(format_str, flag, frame_number, command_id, data_bytes)
    return data_to_pack