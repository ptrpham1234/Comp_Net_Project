import socket
import threading
import time

import protocol
import os.path
import json
import time
from files import Files


def main():
    fileLists = Files()
    clientConnect(fileLists.getList())


#############################################################################################################
# Function:            clientConnect
# Author:              Troy Curtsinger (tjc190001)
# Date Started:        11/29/2022
#
# Description:
# creates the client socket and manages the list call
#############################################################################################################
def clientConnect(fileHolder):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSock:
        clientSock.bind((protocol.SERVER_IP, protocol.SERVER_PORT))
        clientSock.listen()
        connect, addr = clientSock.accept()

        print(f"new connection from: {addr}")
        connect.recv(1024)
        msg = str(json.dumps(fileHolder))
        connect.send(msg.encode())
        connect.close()
        clientSock.close()
    time.sleep(1)
    renderConnect(Files())


#############################################################################################################
# Function:            renderConnect
# Author:              Troy Curtsinger (tjc190001)
# Date Started:        11/29/2022
#
# Description:
# creates the render socket and manages the calls to render files
#############################################################################################################
def renderConnect(fileList):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as renderSock:
        renderSock.bind((protocol.SERVER_IP, protocol.SERVER_PORT_2))
        renderSock.listen()
        connect, addr = renderSock.accept()
        print(f"new connection from: {addr}")
        fileID = int(connect.recv(1024).decode())

        file = fileList.getFileDict(fileID)

        if file:
            state = [True,False] #Sending data | restarting
            print('hi2')
            control = threading.Thread(target=controlsThread,args=(state,))
            control.start()
            try:
                with open(file["filename"], "r") as returnFile:
                    print('hi')
                    lines = returnFile.readline()
                    while(lines):
                        time.sleep(.8)
                        while(state[0] is False):
                            time.sleep(.8)
                        if(state[1]):
                            state[1] = False
                            returnFile.seek(0,0)
                            lines = returnFile.readline()
                        connect.sendall(lines.encode())
                        lines = returnFile.readline()
                    connect.sendall("done".encode())
            except BrokenPipeError:
                print("Connection lost to Render while streaming")
        else:
            connect.send("missing file")
        connect.close()


def controlsThread(state):
    controls = protocol.receiverSocket(protocol.SERVER_IP,4819)
    controls.listen()
    while(True):
        connection, ipaddress = controls.accept()
        print("connected to" + str(ipaddress))
        command = connection.recv(1024).decode()
        print('Recieved the command to: '+str(command))
        if command == 'pause':
            state[0] = False
        elif command == 'resume':
            state[0] = True
        elif command == 'restart':
            state[1] = True



if __name__ == "__main__":
    main()
