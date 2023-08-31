# import socket module
from socket import *
# In order to terminate the program
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
serverSocket.bind(("10.31.157.64", 12345))
serverSocket.listen()

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(4096).decode()
        print("Received message:")
        print()
        print(message)
        message = message.split()
        if len(message) < 1:
            print("<Empty Message>")
            print()
            connectionSocket.close()
            continue
        filename = message[1]
        with open(filename[1:]) as f:
            outputdata = f.readlines()
        # Send one HTTP header line into socket
        
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("\r\n".encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError as e:
        print("IOError: " + str(e))
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404\r\n".encode())
        # Close client socket
        connectionSocket.close()
serverSocket.close()
sys.exit()
