import socket
import threading
import protocol


def main():
    serverSocket = establishConnection()
    choice = menu()
    if choice == 1:
        sendListRequest(serverSocket)


#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Attempts to connect to the server
#############################################################################################################
def establishConnection():
    try:
        # AF_INET for IPv4          SOCK_DGRAM for UDP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((protocol.SERVER_IP, protocol.SERVER_PORT))
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
    while True:
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

    # TODO: Print files here after knowing the contents sent by the server
    print("List of files")
    for file in msg.split().decode():
        print(file)




if __name__ == "__main__":
    main()
