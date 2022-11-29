import socket
import threading
import protocol


def main():
    serverSocket = protocol.senderSocket(protocol.SERVER_IP, protocol.SERVER_PORT)
    choice = menu()
    if choice == 1:
        sendListRequest(serverSocket)
        fileName = fileSelection()
        sendFileRequest(fileName)


#############################################################################################################
# Function:            Menu
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Display a menu where the user can decide what to do
#############################################################################################################
def menu():
    while True:  # for error checking
        print("1. Get file names")
        print("2. Request File")
        print("3. Exit")
        try:
            num = int(input("Enter a number: "))
            if num > 0 & num < 4:
                return num
            else:
                print("not valid try again")
                continue
        except ValueError:
            print("Not a number try again.")
            continue


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
    msg = serverSocket.recv(1024)

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
    while True:  # for error checking
        print("1. Get file names")
        print("2. Request File")
        print("3. Exit")
        try:
            num = int(input("Enter fileID to request: "))
            return num
        except ValueError:
            print("Not a number try again.")


#############################################################################################################
# Function:            sendFileRequest
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Asks what file the user wants to stream
#############################################################################################################
def sendFileRequest(fileName):
    renderSocket = protocol.senderSocket(protocol.RENDER_IP, protocol.RENDER_PORT)
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
