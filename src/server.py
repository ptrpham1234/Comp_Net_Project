import socket
import threading
import protocol
import os.path
import json

fileHolder = {
    "files": [{
            "id": 1,
            "filename": "test.txt",
            "filetype": "text",
            "description": "the test file to be read"
        },
        {
            "id": 2,
            "filename": "notReal.txt",
            "filetype": "text",
            "description": "not a real file"
        },
        {
            "id": 3,
            "filename": "aLie.txt",
            "filetype": "text",
            "description": "also not a real file"
        }
    ]
}

def main():
    clientConnect()
    renderConnect()


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
        msg = json.dumps(fileHolder)
        connect.send(msg)
    connect.close()


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
        if os.path.isfile(request):
            sendRender(connect, fileName)
        else:
            connect.send("missing file")
    connect.close()


#############################################################################################################
# Function:            sendRender
# Author:              Troy Curtsinger (tjc190001)
# Date Started:        11/29/2022
#
# Description:
# handles file rendering
#
# @param    connect      connection         the connection to the renderer
# @param    fileName     string             the name of the requested file (assumed to exist) 
#############################################################################################################
def sendRender(connect, fileName):
    file = open(fileName, "r")
    for line in file:
        connect.send(line)