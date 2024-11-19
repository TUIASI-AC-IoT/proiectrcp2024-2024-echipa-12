import socket as sc
from time import sleep
import codificare
import util
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

MESSAGE = "HEY GEO CE3 FLACAU!"

socket = sc.socket(sc.AF_INET,
                   sc.SOCK_DGRAM)
mess=codificare.impachetare(util.FILE_CHUNK,2,0,MESSAGE)

while(True):
    socket.sendto(mess, (UDP_IP, UDP_PORT))
    sleep(3)
