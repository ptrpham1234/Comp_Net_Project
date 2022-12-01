import json
import socket
import sys
import threading
import protocol
import time


def main():
    fileList = None
    while True:
        serverSocket = protocol.senderSocket(protocol.SERVER_IP, protocol.SERVER_PORT)

        choice = menu()
        if choice == 1:
            fileList = sendListRequest(serverSocket)
            fileID = fileSelection()
            sendFileRequest(fileID)
            receiveStream()
            print("closing connections...")
            time.sleep(2)
            sys.stdin.flush()
        elif choice == 2:
            printFileList(fileList)
        elif choice == 3:
            printFileList(fileList)
            fileID = fileSelection()
            sendFileRequest(fileID)
            receiveStream()
            print("closing connections...")
            time.sleep(2)
            sys.stdin.flush()
        else:
            break


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
        print("2. Print File List")
        print("3. Request File")
        print("4. Exit")
        try:
            num = int(input("Enter a number: "))
            if num > 0 & num < 5:
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
    serverSocket.sendall(str(protocol.LIST_REQUEST).encode())
    msg = serverSocket.recv(1024).decode()

    print("\nList of files:")
    printFileList(msg)

    serverSocket.close()
    return msg


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
def printFileList(msg):
    try:
        jsonObj = json.loads(msg)
        jsonObj = jsonObj["files"]

        for items in jsonObj:
            print("ID: ", items["id"])
            print("File Name: ", items["filename"])
            print("File Type: ", items["filetype"])
            print("Description", items["description"])
            print()
    except TypeError:
        print(msg)


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
def sendFileRequest(fileID):
    renderSocket = protocol.senderSocket(protocol.RENDER_IP, protocol.RENDER_PORT)
    renderSocket.sendall(str(fileID).encode())
    renderSocket.close()


#############################################################################################################
# Function:            sendFileRequest
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Asks what file the user wants to stream
#############################################################################################################
class KeyboardThread(threading.Thread):
    def __init__(self, event, input_cbk=None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        self.event = event
        super(KeyboardThread, self).__init__(name=name)  # Problem Here: set daemon here
        self.start()

    def run(self):
        while not self.event.is_set():
            self.input_cbk(input())  # Problem Here: wait here forever until user enters something

        print("thread done")



#############################################################################################################
# Function:            sendFileRequest
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Asks what file the user wants to stream
#############################################################################################################
def my_callback(inp):
    print('You entered: ', inp)
    if inp == 'pause':
        notify = protocol.senderSocket(protocol.RENDER_IP, 4818)
        notify.sendall('pause'.encode())
        notify.close()
    elif inp == 'resume':
        notify = protocol.senderSocket(protocol.RENDER_IP, 4818)
        notify.sendall('resume'.encode())
        notify.close()
    elif inp == 'restart':
        notify = protocol.senderSocket(protocol.RENDER_IP, 4818)
        notify.sendall('restart'.encode())
        notify.close()


#############################################################################################################
# Function:            sendFileRequest
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Asks what file the user wants to stream
#############################################################################################################
def receiveStream():
    done = False
    streamSocket = protocol.receiverSocket(protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT)
    streamSocket.listen()
    connection, ipAddress = streamSocket.accept()
    print("Streaming from: " + str(ipAddress))

    event = threading.Event()
    kthread = KeyboardThread(event, my_callback)
    while not done:
        msg = connection.recv(1024).decode()
        if msg != "done":
            print(msg, end="")
        else:
            print("streaming done")
            streamSocket.close()
            done = True

    print("closing Thread")
    event.set()  # close the thread
    kthread.join()  # Problem Here: never joins so never stop but will continue if thread is daemon
    connection.close()
    streamSocket.close()


if __name__ == "__main__":
    main()
