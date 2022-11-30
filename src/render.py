import socket
import threading
import protocol
import time


def main():
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
	time.sleep(5)  # Necessary !! DO NOT REMOVE
	# send ID to server to get file from
	serverSocket = protocol.senderSocket(protocol.SERVER_IP, protocol.SERVER_PORT_2)
	serverSocket.sendall(fileID.encode())  # send the ID
	done = False

	controllerSend = protocol.senderSocket(protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT)

	while not done:
		time.sleep(.5)
		msg = serverSocket.recv(1024)
		print(msg.decode())
		controllerSend.sendall(msg)


if __name__ == "__main__":
	main()
