import socket
import threading
import protocol


def main():
    clientSocket = protocol.receiverSocket(protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT)
    fileID = clientConnect(clientSocket)
    serverSend(fileID)


#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Receive the file id to stream from the user and then close the connection
#############################################################################################################
def clientConnect(clientSocket):
    clientSocket.listen()
    connection, ipaddress = clientSocket.accept()
    print("received connection from: " + str(ipaddress))
    fileID = connection.recv(1024).decode()
    connection.close()
    return fileID


#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Attempts to connect to the server
#############################################################################################################
def serverSend(fileName):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((protocol.SERVER_IP, protocol.SERVER_PORT))
    serverSocket.sendall(fileName)


#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Attempts to connect to the server
#############################################################################################################
def streamReceive():
    pass


if __name__ == "__main__":
    main()
