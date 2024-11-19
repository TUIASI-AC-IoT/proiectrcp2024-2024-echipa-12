#package types
ACK = 0b0000_0001
FILE_CHUNK = 0b0000_0010
ACK_COMMAND = 0b0000_0100
ACK_COMMAND_W_OUTPUT = 0b0000_1000
COMMAND_NO_PARAMS = 0b0001_0000
COMMAND_W_PARAMS = 0b0010_0000

#command types
LS       = 0b0000_0001
CD       = 0b0000_0010
MK_MKDIR = 0b0000_0011
RM_RMDIR = 0b0000_0100
MOVE     = 0b0000_0101
