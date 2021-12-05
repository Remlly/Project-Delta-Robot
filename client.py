# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 21:25:37 2021
@author: remlly
"""

# client 
import socket 
import numpy as np 


import StructFuncs as struct


hostIp = '192.168.178.30'              # Use ip address from the server 
hostPort = 2001                        # Use pc port from the server 
serverAddress = (hostIp, hostPort)     # create (tuple) 


string = "hello world!"
packed_data = struct.pack_string(string)

while True:                            # Repeat until message == quit 
 
    print()
    print("ip address: ", hostIp) 
    print("pc poort:   ", hostPort) 
    print() 
 
    # Create TCP socket & connect to host 
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcpSocket.connect(serverAddress) 
 
    # Repeat until message == close or message == quit 
    while True: 
        while True:                    # Repeat until message != "" 
            message = input("=>_") 
            if message != "": 
                break 
            
        if (message == "send"):
            message = packed_data[0]
        messageLength = tcpSocket.send(message) 
        print() 
 
        print("Number of bytes sent: ", messageLength) 
 
        serverReply = tcpSocket.recv(1024).decode() 
        print("Answer from server:", serverReply) 
        print() 
 
        if message == "close" or message == "quit": 
            break 
 
    tcpSocket.close()                  # the complete tcpSocket is deleted 
    print("connection closed") 
 
    if message == "quit": 
        break 
 
print("server quitted & end of client program reached") 
# end of client program 