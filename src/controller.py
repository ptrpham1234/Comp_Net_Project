import json
import socket
import threading
import protocol


def main():
	serverSocket = protocol.senderSocket(protocol.SERVER_IP, protocol.SERVER_PORT)
	choice = menu()
	if choice == 1:
		sendListRequest(serverSocket)
		fileID = fileSelection()
		sendFileRequest(fileID)
		receiveStream()


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
	serverSocket.sendall(str(protocol.LIST_REQUEST).encode())
	msg = serverSocket.recv(1024)

	print("List of files:")
	print(json.loads(msg))


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
	renderSocket.sendall(fileID)
	renderSocket.close()


#############################################################################################################
# Function:            sendFileRequest
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Asks what file the user wants to stream
#############################################################################################################
def receiveStream():
	streamSocket = protocol.receiverSocket(protocol.CONTROLLER_IP, protocol.CONTROLLER_PORT)
	done = False

	while not done:
		msg = streamSocket.recv(1024).decode()
		if msg != "done":
			print(msg)
		else:
			streamSocket.close()
			done = True


if __name__ == "__main__":
	main()
