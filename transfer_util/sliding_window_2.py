from transfer_util import encoder
import time
from transfer_util import util


timeout = 10

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
    print("dim buffer: ", len(buffer))
    return buffer

def createWindow():
    cnt = 0
    for i in util.sending_buffer:
        frm=frame()
        frm.data=i;
        frm.sending_time = 0
        frm.rcv_ack = False
        util.window.append(frm)

def timeout_fct():  # window -> lista de frame-uri
    for i in range(util.posfirst,util.poslast):
        if util.window[i].sending_time + timeout > time.time():
            return i  #trebuie retrimis
            print("?")
    return -1  #nu trebuie retrimis niciun pachet


def move_list_one_pos_right():
    mutat = 0
    if(util.poslast + 1 != len(util.window)):
        mutat = 1
        util.posfirst +=1
        util.poslast += 1
        print("s-a mutat")
    elif util.posfirst < util.poslast:
        util.posfirst += 1
    return mutat #mutat=0 -> nu se mai poate muta fereastra


def slide_window():
    if util.window!=None:
        while util.window[util.posfirst].rcv_ack:
            if (move_list_one_pos_right() == 0): #daca nu s-a facut nicio schimbare atunci
                break #iesim din while
            # print("ultima pozitie fereastra: ", util.poslast)
            # print("prima pozitie fereastra: ", util.posfirst)
            # util.posfirst += 1
            # util.poslast += 1

def something_to_send():
    for i in range(util.posfirst,util.poslast+1):
        if util.window[i].rcv_ack == False or util.window[i].sending_time == 0:
            return True
    return False

def sw_send(sock, address: tuple[str, int]):
    to_elem=timeout_fct()
    while util.window_size <= util.poslast+1 - util.posfirst or to_elem != -1: #inca mai sunt elemente de parcurs sau avem un element in timeout
        while to_elem != -1:  #atata timp cat exista o bucata de fisier in timeout va fi retrimisa
            util.window[to_elem].sending_time = time.time()
            mess = encoder.packing(util.FILE_CHUNK, to_elem, 0, util.window[to_elem].data)
            sock.sendto(mess+b'fisier', address)
            to_elem = timeout_fct()
            print("se trimite")
        slide_window()  #se muta fereastra daca este nevoie

        if something_to_send() == True:
            for i in range(util.posfirst, util.poslast+1):  #se cauta elemente care nu au fost trimise inca
                # print("i= ", i)
                # print("posfirst= ", util.posfirst)
                # print("poslast= ", util.poslast)
                if util.window[i].sending_time == 0 and util.window[i].rcv_ack == False:
                    util.window[i].sending_time = time.time()
                    mess = encoder.packing(util.FILE_CHUNK, i, 0, util.window[i].data)
                    sock.sendto(mess+b'fisier', address)
               # time.sleep(1)
                    print("se trimite")
    print("gata trimisul!")