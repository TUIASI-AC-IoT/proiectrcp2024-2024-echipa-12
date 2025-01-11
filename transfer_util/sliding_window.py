from pkg_resources import non_empty_lines

from transfer_util import encoder
import time
from transfer_util import util
from transfer_util.util import sending_buffer, window_size

timeout = 10


#==================================
#             |    | boolean |
#|sending_time|data| rcv_ack |
#==================================

class frame:
    def __init__(self):
        self.sending_time = 0
        self.data = None
        self.rcv_ack = False
        #incercam
        self.frame_no = -1 #va avea aceeasi valoare ca nr frame-ului in buffer

def createBuffer(file_name: str):
    dim = util.packet_data_size  #nr octeti data
    f = open(file_name, "rb")
    chunk = f.read(dim)
    buffer = []
    i = 0
    while chunk:
        #pack = encoder.packing(util.FILE_CHUNK, i, 0, chunk)
        buffer.append(chunk)
        i += 1
        chunk = f.read(dim)
    f.close()
    return buffer

def createWindow():
    # while len(util.sending_buffer) < util.packet_data_size:
    #     util.sending_buffer
    cnt = 0
    for i in util.sending_buffer:
        if cnt == util.window_size:
            break
        frame_elem = frame()
        frame_elem.data = i
        frame_elem.frame_no = cnt
        util.window.append(frame_elem)
        cnt += 1

def timeout_fct(window: list[frame]):  # window -> lista de frame-uri
    if window!=None:
        for i in window:
            if i.sending_time + timeout > time.time() and i.rcv_ack == False:
                return i  #trebuie retrimis
    return -1  #nu trebuie retrimis niciun pachet


def move_list_one_pos_right(sliding_window):
    n = len(sliding_window)
    for i in range(n - 1):
        sliding_window[i] = sliding_window[i + 1]
    return sliding_window


def slide_window(window, buffer, position):
    if window!=None:
        while window[0].rcv_ack:
            window = move_list_one_pos_right(window)
            if len(buffer) > position + util.window_size:
                window[util.window_size - 1].frame_no = position
                window[util.window_size - 1].data = buffer[position]


def sw_send(window, buffer, position, sock, address: tuple[str, int]):
    while position + util.window_size <= len(buffer):
        # print(util.window, "\n", util.sending_buffer)
        var = timeout_fct(window)

        while var != -1:  #atata timp cat exista o bucata de fisier in timeout va fi retrimisa
            if(var!=None):
                var.sending_time = time.time()
                mess = encoder.packing(util.FILE_CHUNK, var.frame_no, 0, var.data)
                sock.sendto(mess+b'fisier', address)
                var = timeout_fct(window)
                print('retrimis')
        slide_window(window, buffer, position)  #se muta fereastra daca este nevoie
        if window!=None:
            for i in window:  #se cauta elemente care nu au fost trimise inca
                if i.sending_time == 0 and i.data!=None:
                    i.sending_time = time.time()
                    mess = encoder.packing(util.FILE_CHUNK, i.frame_no, 0, i.data)
                    sock.sendto(mess+b'fisier', address)
                    print('trimis pt ca fereastra')

