import socket

SERVER_PORT = 4816
RENDER_PORT = 4816
CONTROLLER_PORT = 4816
SERVER_IP = '10.0.0.1'
RENDER_IP = '10.0.0.2'
CONTROLLER_IP = '10.0.0.3'

LIST_REQUEST = 1
FILE_REQUEST = 2
CONN_TERMINATION = 3

PAUSE = 1
CONTINUE = 2
RESTART = 3



#############################################################################################################
# Function:            receiverSocket
# Author:              Peter Pham (pxp180041)
# Date Started:        11/29/2022
#
# Description:
# Creates a socket to receive data from the connection
#############################################################################################################
def receiverSocket(destinationIP, destinationPort):
    try:
        # AF_INET for IPv4          SOCK_DGRAM for UDP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((destinationIP, destinationPort))
        return serverSocket

    except socket.error:
        print("Unable to connect to server")


#############################################################################################################
# Function:            senderSocket
# Author:              Peter Pham (pxp180041)
# Date Started:        11/29/2022
#
# Description:
# Creates a socket to send data
#############################################################################################################
def senderSocket(destinationIP, destinationPort):
    try:
        # AF_INET for IPv4          SOCK_DGRAM for UDP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((destinationIP, destinationPort))
        return serverSocket

    except socket.error:
        print("Unable to connect to server")
