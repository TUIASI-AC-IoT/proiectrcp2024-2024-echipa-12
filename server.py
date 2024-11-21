import socket as sc
import unpacking_util as up

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

socket = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
socket.bind((UDP_IP, UDP_PORT))

while True:
    #data = ''
    data, addr = socket.recvfrom(1024)
    up.unpack(data)
    print("AM PRIMIT UN MESAj %s: " % data)
    print("de la:", addr)