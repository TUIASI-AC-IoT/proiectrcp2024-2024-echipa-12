import os
import queue

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

timeout = 2.5 # secunde
packetloss = 20 # %

class FileChunk:
    def __init__(self, frame_no, data):
        self.frame_no = frame_no
        self.data = data

class Ack:
    def __init__(self, ack_type, cmd_id, data=None):
        self.ack_type = ack_type
        self.cmd_id = cmd_id
        self.data = data

file_buffer = []
current_frame = 0
sending_buffer = []
file_to_transfer = ''
upload_flag = False
sent = []
window_position = 0
window = []

#semaphore for sliding window
smphr_sending_file=False

#SLIDING WINDOW SETTINGS
window_size = 5
packet_data_size = 1024
timeout_duration = 1 #secunde


#OTHER SETTINGS
packet_loss = .2



#TODO: KNOWN ISSUES
# 1. Daca incerc sa sterg fisier nu merge
# 2. Daca incerc sa sterg folder cu fisiere in el crapa
# 3. Daca pui space cand dai new folder iti face pana la space (not a bug, a feature :)))  # rezolvare: punem " " la mkdir
# 4. TO BE CONTINUED PROBABIL...