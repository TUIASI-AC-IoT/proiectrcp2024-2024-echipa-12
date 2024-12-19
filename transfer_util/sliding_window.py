import encoder
import time

import util

timeout = 10


#==================================
#                  |boolean|boolean|
#|sending_time|pack|rcv_ack| sent  |
#==================================

class frame:
    def __init__(self):
        self.sending_time = 0
        self.data = None
        self.rcv_ack = False


def createBuffer(file_name: str):
    dim = util.packet_data_size  #nr octeti data
    f = open(file_name, "rb")
    chunk = f.read(dim)
    buffer = []
    i = 1
    while chunk:
        pack = encoder.packing(util.FILE_CHUNK, i, 0, chunk)
        buffer.append(pack)
        i += 1
        chunk = f.read(dim)
    f.close()
    return buffer


def timeout_fct(window: list[frame]):  # window -> lista de frame-uri
    for i in window:
        if (i.time + timeout > time.time()):
            return i  #trebuie retrimis
    return -1  #nu trebuie retrimis niciun pachet


def move_list_one_pos_right(sliding_window):
    n = len(sliding_window)
    for i in range(n - 1):
        sliding_window[i] = sliding_window[i + 1]
    return sliding_window


def slide_window(window, buffer, position):
    while window[0].rcv_ack:
        window = move_list_one_pos_right(window)
        if len(buffer) > position + util.window_size:
            window[util.window_size - 1].data = buffer[position]


def sw_send(window, buffer, position, sock, address: tuple[str, int], frame_no):
    var = timeout_fct(window)
    if var != -1:  #daca exista atunci va fi retrimis
        window[var].time = time.time()
        mess = encoder.packing(util.FILE_CHUNK, frame_no, 0, var.data)
        sock.sendto(mess, address)
    slide_window(window, buffer, position)  #se muta fereastra daca este nevoie
    for i in window:  #se cauta elemente care nu au fost trimise inca
        if i.time == 0:
            i.time = time.time()
            mess = encoder.packing(util.FILE_CHUNK, frame_no, 0, var.data)
            sock.sendto(mess, address)

# lista=[0,2,3,4,5,1]
# lista=move_list_one_pos_right(lista)
# lista=move_list_one_pos_right(lista)
# lista=move_list_one_pos_right(lista)
# print(lista)
