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
    clientSock = protocol.receiverSocket(protocol.SERVER_IP, protocol.SERVER_PORT)
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

    renderSock = protocol.receiverSocket(protocol.SERVER_IP, protocol.SERVER_PORT_2)
    renderSock.listen()
    connect, addr = renderSock.accept()
    print(f"new connection from: {addr}")
    fileID = int(connect.recv(1024).decode())

    file = fileList.getFileDict(fileID)

    if file:
        state = [True, False, False, False]  # Sending data | restarting | done sending (for Thread) | stop
        control = threading.Thread(target=controlsThread, args=(state,))
        control.start()
        try:
            with open(file["filename"], "r") as returnFile:
                lines = returnFile.readline()
                while lines:
                    time.sleep(.8)
                    while state[0] is False:
                        time.sleep(.8)
                    if state[1]:
                        state[1] = False
                        returnFile.seek(0, 0)
                        lines = returnFile.readline()
                    if state[3]:
                        break
                    connect.sendall(lines.encode())
                    lines = returnFile.readline()
                time.sleep(.8)
                connect.send("done".encode())
        except BrokenPipeError:
            print("Connection lost to Render while streaming")
        state[2] = True
    else:
        connect.send("missing file")
    connect.close()
    renderSock.close()

#############################################################################################################
# Function:            renderConnect
# Author:              Troy Curtsinger (tjc190001)
# Date Started:        11/29/2022
#
# Description:
# creates the render socket and manages the calls to render files
#############################################################################################################
def controlsThread(state):
    controls = protocol.receiverSocket(protocol.SERVER_IP, protocol.PLAY_PAUSE_SERVER)
    controls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #controls.settimeout(1)
    controls.listen()
    while True:
        try:
            connection, ipaddress = controls.accept()
            print("connected to" + str(ipaddress))
            command = connection.recv(1024).decode()
            print('Received the command to: ' + str(command))
            if command == 'pause':
                state[0] = False
            elif command == 'resume':
                state[0] = True
            elif command == 'restart':
                state[1] = True
            elif command == 'stop':
                state[3] = True
        except TimeoutError:
            if state[2]:
                break
            else:
                continue
    controls.close()



if __name__ == "__main__":
    main()
    print("done")
