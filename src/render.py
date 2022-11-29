import socket
import threading
import protocol


def main():
	clientSocket = protocol.receiverSocket(protocol.RENDER_IP, protocol.CONTROLLER_PORT)
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
def serverSend(fileID):
	serverSocket = protocol.receiverSocket(protocol.SERVER_IP, protocol.SERVER_PORT)
	serverSocket.sendall(fileID.encode())
	done = False
	controllerSend = protocol.senderSocketUDP(protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT)

	while not done:
		msg = serverSocket.recv(1024)
		if msg.decode() == "done":
			controllerSend.sendall(msg)
		else:
			controllerSend.sendall(msg)



if __name__ == "__main__":
	main()
