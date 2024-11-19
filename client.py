import socket as sc
from time import sleep

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

MESSAGE = b"HEY GEO CE FLACAU"

socket = sc.socket(sc.AF_INET,
                   sc.SOCK_DGRAM)
while(True):
    socket.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sleep(3)
