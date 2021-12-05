# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:50:24 2021

@author: remll
"""

# server 
import socket 

import StructFuncs as struct


pcHostName = socket.gethostname() 
hostIp = socket.gethostbyname(pcHostName) 
hostPort = 2001 
serverAddress = (hostIp, hostPort)      # create (tuple) 
 
print() 
print("pc name:    ", pcHostName) 
print("ip address: ", hostIp) 
print("pc port:    ", hostPort) 
print() 
 
# Create TCP socket, bind it to the server address port & listen for clients 
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpSocket.bind(serverAddress)           # Bind to the port 
tcpSocket.listen(5)                     # Wait for (max 5) connecting clients 
 
while True: 
    print("[*] Started listening on", hostIp, ":", hostPort) 
    # Establish connection with client. 
    client, clientAddress = tcpSocket.accept() 
 
    # clientAddress[0] contains client-ip 
    # clientAddress[1] contains client-port 
    print("[*] Got connection from ", 
          clientAddress[0], ":", clientAddress[1]) 
 
    while True: 
        data = client.recv(1024)
        
        print("[*] Received '", data, "' from the client") 
        print("    Processing data") 
        unpacked_data = struct.unpack_string(data)
        print(f"{unpacked_data}")
        client.send(unpacked_data.encode()) 
        
        
print("    End of server program.") 

