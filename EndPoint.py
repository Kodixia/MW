from Utileries import *
import socket
import threading

HEADER = 64
PORT = 5555
SERVER_IP = ""
ADDR = (SERVER_IP,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "Disco!"
MASTER_NAME = "Master"
master_ip = None
master_conn = None
slaveList = {}


def startServer():
    global master_ip
    global master_conn
    global slaveList
    endP.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{PORT}")
    while True:
        conn,addr = endP.accept()
        name = reciveMsg(conn)
        print(f"[NEW CONNECTION] Connected {name} with the address {addr}")
        if (name == MASTER_NAME):
            master_ip = addr
            master_conn = conn
            masterThread = threading.Thread(target=showSlaves)
            masterThread.start()
        else:
            slaveList[addr] = conn
            


def showSlaves():
    global slaveList
    connections = "Connections:"
    for address  in slaveList:
        connections += "\n" + str(address)
    connections += "\nConnect to?: "
    sendMsg(master_conn,connections)
    msg = reciveMsg(master_conn)
    new_conn = None
    for addr in slaveList:
        if(msg == addr[0]):
            new_conn = slaveList[addr]
            print(f"[ESTABLISHED] Established connection between Master and Slave {addr}")
    if (new_conn != "exit" or new_conn != "cancel" or new_conn != None):
        sendToMaster(new_conn,master_conn)


def sendToMaster(slaveConn,masterConn):
    masterSender = threading.Thread(target=sender,args=(masterConn,slaveConn))
    slaveSender = threading.Thread(target=sender,args=(slaveConn,masterConn))
    masterSender.start()
    slaveSender.start()
    sendMsg(slaveConn,"Confirmed")

def sender(conn1,conn2):
    while True:
        msg = reciveMsg(conn1)
        #if msg[0:9] == "download ":
         #   sendMsg(conn2,msg)
          #  reciveFile(conn2,msg[9:])
           # sendFile(conn1,msg[9:])
        #else:
        sendMsg(conn2,msg)

endP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
endP.bind(ADDR)
print(f"[STARTING] Starting the server...")
startServer()
