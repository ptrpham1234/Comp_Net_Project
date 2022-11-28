import socket
import threading
import protocol
import os.path

def main():
    clientConnect()


#############################################################################################################
# Function:            clientConnect
# Author:              Troy Curtsinger (tjc190001)
# Date Started:        11/29/2022
#
# Description:
# creates the client socket and manages the list call
#############################################################################################################
def clientConnect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSock:
        socket.bind((protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT))
        clientSock.listen()
    connect, addr = clientSock.accept()
    with connect:
        print(f"new connection from: {addr}")
        connect.recv(1024)
        msg = "test.txt notReal.txt aLie.txt\n"
        connect.send(msg)

#############################################################################################################
# Function:            renderConnect
# Author:              Troy Curtsinger (tjc190001)
# Date Started:        11/29/2022
#
# Description:
# creates the render socket and manages the calls to render files
#############################################################################################################
def renderConnect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as renderSock:
        socket.bind((protocol.RENDER_IP, protocol.RENDER_PORT))
        renderSock.listen()
    connect, addr = renderSock.accept()
    with connect:
        print(f"new connection from: {addr}")
        request = connect.recv(1024)
        os.path.isfile(request)
        msg = "i'm not a file, you shouldnt see me"
        connect.send(msg)


        