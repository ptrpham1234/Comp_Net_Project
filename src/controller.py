import socket
import threading
import protocol


def main():
    serverSocket = establishConnection(protocol.SERVER_IP, protocol.SERVER_PORT)
    choice = menu()
    if choice == 1:
        sendListRequest(serverSocket)
        fileName = fileSelection()
        sendFileRequest(fileName)


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
        serverSocket.connect((destinationIP, destinationPort))
        return serverSocket

    except socket.error:
        print("Unable to connect to server")


#############################################################################################################
# Function:            Menu
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Display a menu where the user can decide what to do
#############################################################################################################
def menu():
    while True: # for error checking
        print("1. Get file names")
        print("2. Request File")
        print("3. Exit")
        try:
            num = int(input("Enter a number: "))
            if num > 0 & num < 4:
                return num
        except ValueError:
            print("Not a number try again.")


#############################################################################################################
# Function:            sendRequest
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Looks at the user choice and send the appropriate message to the server
#
# @param    choice      int         contains what the user wants to do
# @param    serverSocket    socket  contains the socket needed to send the request
#############################################################################################################
def sendListRequest(serverSocket):

    serverSocket.sendall(protocol.LIST_REQUEST)
    serverSocket.listen()
    connectSocket, addr = serverSocket.accept()

    msg = connectSocket.recv(1024)

    print("List of files:")
    with open("file.txt", "wb") as file:
        for rcvFile in msg.split():
            file.write(rcvFile)

    with open("file.txt", "rb") as file:
        for line in file.readline():
            print(line)


#############################################################################################################
# Function:            fileSelection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Asks what file the user wants to stream
#############################################################################################################
def fileSelection():
    return input("Enter file to request")


#############################################################################################################
# Function:            sendFileRequest
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Asks what file the user wants to stream
#############################################################################################################
def sendFileRequest(fileName):
    renderSocket = establishConnection(protocol.RENDER_IP, protocol.RENDER_PORT)
    renderSocket.sendall(fileName)
    done = False

    while not done:
        renderSocket.listen()
        connectSocket, addr = renderSocket.accept()

        msg = connectSocket.recv(1024)
        if msg.decode() == "done":
            done = True
        else:
            print(msg.decode())





if __name__ == "__main__":
    main()
