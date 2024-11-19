import socket as sc

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

socket = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
socket.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = socket.recvfrom(1024)
    print("AM PRIMIT UN MESAj %s: " % data)
    print("de la:", addr)