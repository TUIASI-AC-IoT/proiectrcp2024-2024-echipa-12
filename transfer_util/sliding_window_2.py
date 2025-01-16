import os

from transfer_util import encoder
import time
from transfer_util import util as util
import random as rand

#til.timeout = 2

class frame:
    def __init__(self):
        self.sending_time = 0
        self.data = None
        self.rcv_ack = False
        #incercam
        self.frame_no = -1 #va avea aceeasi valoare ca nr frame-ului in buffer

def createBuffer(file_name: str):
    dim = util.packet_data_size  #nr octeti data
    filesize = os.path.getsize(file_name)
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
    #print("dim buffer: ", len(buffer))
    return buffer

def createWindow():
    cnt = 0
    for i in util.sending_buffer:
        frm=frame()
        frm.data=i
        frm.sending_time = 0
        frm.rcv_ack = False
        util.window.append(frm)

# def timeout_fct():  # window -> lista de frame-uri
#     for i in range(util.posfirst,util.poslast):
#         if util.window[i].sending_time + timeout > time.time() and util.window[i].rcv_ack == False:
#             return i  #trebuie retrimis
#     return -1  #nu trebuie retrimis niciun pachet

def timeout_fct():  # window -> lista de frame-uri
    lista=[]
    for i in range(util.posfirst,util.poslast+1):
        if util.window[i].sending_time + util.timeout <= time.time() and util.window[i].rcv_ack == False:
            # print("-----")
            # print(time.time())
            # print(util.window[i].sending_time,"\n")
            # print(util.window[i].sending_time+util.timeout,"\n")
            # print("---------")
            lista.append(i)  #trebuie retrimis
    return lista  #nu trebuie retrimis niciun pachet


def move_list_one_pos_right():
    mutat = 0
    if(util.poslast + 1 != len(util.window)):
        mutat = 1
        util.posfirst +=1
        util.poslast += 1
        #print("s-a mutat")
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

# def sw_send(sock, address: tuple[str, int]):
#     to_elem=timeout_fct()
#     while util.window_size <= util.poslast+1 - util.posfirst or to_elem != -1: #inca mai sunt elemente de parcurs sau avem un element in timeout
#         to_elem = timeout_fct()
#         while to_elem != -1:  #atata timp cat exista o bucata de fisier in timeout va fi retrimisa
#             util.window[to_elem].sending_time = time.time()
#             mess = encoder.packing(util.FILE_CHUNK, to_elem, 0, util.window[to_elem].data)
#             if(rand.randint(0,100)>util.client_pack_loss_percentage):
#                 sock.sendto(mess, address)
#             else:
#                 print("TEAPA, NU S-O TRIMIS")
#             to_elem = timeout_fct()
#             print(to_elem)
#
#         slide_window()  #se muta fereastra daca este nevoie
#
#         if something_to_send() == True:
#             for i in range(util.posfirst, util.poslast+1):  #se cauta elemente care nu au fost trimise inca
#                 if util.window[i].sending_time == 0 and util.window[i].rcv_ack == False:
#                     util.window[i].sending_time = time.time()
#                     mess = encoder.packing(util.FILE_CHUNK, i, 0, util.window[i].data)
#                     if (rand.randint(0, 100) > util.client_pack_loss_percentage):
#                         sock.sendto(mess, address)
#                     else:
#                         print("TEAPA, NU S-O TRIMIS")
#                # time.sleep(1)
#                     #print("se trimite")
#     print("gata trimisul")
#
#



def sw_send(sock, address: tuple[str, int]):
    to_elem=[]
    to_elem=timeout_fct()
    #print(util.window_size, "< ws, ", util.poslast+1 - util.posfirst, "< util.poslast+1 - util.posfirst")
    #print(util.poslast, "< poslast", len(util.sending_buffer)-1)

    #while util.window_size <= util.poslast+1 - util.posfirst or len(to_elem) != 0: #inca mai sunt elemente de parcurs sau avem un element in timeout
    while util.poslast <= len(util.sending_buffer)-1 or len(to_elem) != 0: #inca mai sunt elemente de parcurs sau avem un element in timeout
       # print(to_elem, " ", util.posfirst, " " ,util.poslast)
        if(util.shutdown_event.is_set()):
            print("killing send")
            break
        to_elem = []
        to_elem = timeout_fct()

        if len(to_elem) != 0:  #daca exista o bucata de fisier in timeout va fi retrimisa
            for i in range(0,len(to_elem)):
                #print(to_elem,"\n")
                util.window[to_elem[i]].sending_time = time.time()
                mess = encoder.packing(util.FILE_CHUNK, to_elem[i], 0, util.window[to_elem[i]].data)
                if(rand.randint(1,100)>util.packet_loss):
                    sock.sendto(mess, address)
                    print(f"PACHETUL {to_elem[i]} S-A RETRIMIS(TIMED_OUT)")
                else:
                    print(f"!!!!!!!!!!!!!!PACHETUL {to_elem[i]} NU S-A RETRIMIS(PIERDUT)")

        slide_window()  #se muta fereastra daca este nevoie

        if something_to_send() == True:
            for i in range(util.posfirst, util.poslast+1):  #se cauta elemente care nu au fost trimise inca
                if util.window[i].sending_time == 0 and util.window[i].rcv_ack == False:
                    util.window[i].sending_time = time.time()
                    mess = encoder.packing(util.FILE_CHUNK, i, 0, util.window[i].data)
                    if (rand.randint(1, 100) > util.packet_loss):
                        sock.sendto(mess, address)
                        print(f"PACHETUL {i} S-A TRIMIS")
                    else:
                        print(f"!!!!!!!!!!!!!!PACHETUL {i} S-A PIERDUT")
               # time.sleep(1)
                    #print("se trimite")
        else:
            to_elem = timeout_fct()
            if len(to_elem) == 0:
                break
        to_elem = []
        to_elem = timeout_fct()
    print("gata trimisul")
   