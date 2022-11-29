import socket
import threading
import protocol


def main():
    clientSocket = establishConnection(protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT)
    fileName = clientConnect(clientSocket)
    serverSend(fileName)




#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Attempts to connect to the server
#############################################################################################################
def establishConnection(destinationIP, destinationPort):
    try:
        # AF_INET for IPv4          SOCK_DGRAM for UDP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((destinationIP, destinationPort))
        return serverSocket

    except socket.error:
        print("Unable to connect to server")

#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Attempts to connect to the server
#############################################################################################################
def clientConnect(clientSocket):
    clientSocket.listen()
    connection, ipaddress = clientSocket.accept()
    print("received connection from: " + str(ipaddress))
    return connection.recv(1024).decode()


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



if __name__ == "__main__":
    main()
