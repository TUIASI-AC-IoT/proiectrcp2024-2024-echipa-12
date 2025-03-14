import os
import queue
import threading as Thread

server_ip = "localhost"
#server_ip = "192.168.190.252"
server_port = 25565

client_ip = "localhost"
#client_ip = "192.168.190.43"
client_port = 25566

#package types
ACK = 0b0000_0001
FILE_CHUNK = 0b0000_0010
ACK_COMMAND = 0b0000_0100
ACK_COMMAND_W_OUTPUT = 0b0000_1000
COMMAND_NO_PARAMS = 0b0001_0000
COMMAND_W_PARAMS = 0b0010_0000

#command types
CD       = 0b0000_0010 #DATA = folder_name
MKDIR = 0b0000_0011 #DATA = folder_name
RM_RMDIR = 0b0000_0100 #DATA = folder_name/file_name
MOVE     = 0b0000_0101 #DATA = path1, path2
TOUCH     = 0b0000_0110 #DATA = name
CHG_SETTING = 0b0000_1001 # DATA = 'setting@value' @ separator

LS       = 0b0000_0001 #astea au output
DOWNLOAD_REQ = 0b0000_0111 #file_name
UPLOAD_REQ = 0b0000_1000 #data = file_name

path = os.getcwd() + "\\SERVER_FILES\\"
ROOT = os.getcwd() + "\\SERVER_FILES\\"
current_file = None

actionQ = queue.Queue()
ackQ = queue.Queue()
filechunkQ = queue.Queue()
uiupdateQ = queue.Queue()
progressQ = queue.Queue()

sending_buffer = [] #da
file_to_transfer = '' #da
window = []

#SLIDING WINDOW SETTINGS
window_size = 5
packet_data_size = 1024
timeout = 2.5 # secunde
posfirst=0
poslast=posfirst+window_size-1

#OTHER SETTINGS
packet_loss = 70

#pentru primirea fisierelor
rcv_buffer = []
last_frame_bf = -1
rcv_buffer_size = 0
rcv_filename = ''

shutdown_event = Thread.Event()

sending_flag = 0

#TODO: KNOWN ISSUES
# 1. Daca incerc sa sterg fisier nu merge           -rezolvat
# 2. Daca incerc sa sterg folder cu fisiere in el crapa   -rezolvat
# 3. Daca pui space cand dai new folder iti face pana la space (not a bug, a feature :)))  # rezolvare: punem " " la mkdir - rezolvat(cred?)
# 4. Dimensiune maxima fisier pe care il pot trimite ~= 67MB -rezolvat
# 5. TO BE CONTINUED PROBABIL...
#