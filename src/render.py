import socket
import threading
import protocol
import time


def main():
    while True:
        clientSocket = protocol.receiverSocket(protocol.RENDER_IP, protocol.RENDER_PORT)
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
    clientSocket.close()
    return fileID


#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Attempts to connect to the server
#############################################################################################################
def serverSend(fileID):
    time.sleep(6)  # Necessary !! DO NOT REMOVE
    # send ID to server to get file from
    serverSocket = protocol.senderSocket(protocol.SERVER_IP, protocol.SERVER_PORT_2)
    serverSocket.sendall(fileID.encode())  # send the ID
    done = False

    controllerSend = protocol.senderSocket(protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT)

    state = [True, False]  # Play/Pause  |  stop thread
    control = threading.Thread(target=controlsThread, args=(state,))
    control.start()
    while not done:
        if state[0]:
            time.sleep(.5)
            msg = serverSocket.recv(1024).decode()
            if msg == "done":
                state[1] = True
                controllerSend.sendall(msg.encode())
                break
            else:
                controllerSend.sendall(msg.encode())
    serverSocket.close()
    controllerSend.close()

#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Attempts to connect to the server
#############################################################################################################
def controlsThread(state):
    controls = protocol.receiverSocket(protocol.RENDER_IP, 4818)
    controls.settimeout(1)
    controls.listen()
    while True:
        try:
            connection, ipaddress = controls.accept()
            print("connected to" + str(ipaddress))
            command = connection.recv(1024).decode()
            print('Received the command to: ' + str(command))
            if command == 'pause':
                state[0] = False
                notify = protocol.senderSocket(protocol.SERVER_IP, 4819)
                notify.sendall('pause'.encode())
                notify.close()
            elif command == 'resume':
                state[0] = True
                notify = protocol.senderSocket(protocol.SERVER_IP, 4819)
                notify.sendall('resume'.encode())
            elif command == 'restart':
                notify = protocol.senderSocket(protocol.SERVER_IP, 4819)
                notify.sendall('restart'.encode())

        except TimeoutError:
            if state[1]:
                break
            else:
                continue

    controls.close()


if __name__ == "__main__":
    main()
    print("done")
