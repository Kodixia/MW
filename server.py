import socket
import threading
from Utileries import *
import os
import subprocess

HEADER = 64
PORT = 5555
SERVER_IP = "192.168.0.8"
ADDR = (SERVER_IP,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "Disco!"
NAME = "Master"

def start(connection):
    sendMsg(connection,NAME)
    print(f"[ESTABLISHED] Connection established on {SERVER_IP}:{PORT}")
    connections = reciveMsg(connection)
    msg = input(connections)
    sendMsg(connection,msg)    
    shellMaster(connection,ADDR)

connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(f"[CONNECTING] Conecting to the server...")
connection.connect(ADDR)
start(connection)
connection.close()