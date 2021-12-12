# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:50:24 2021

@author: remll
"""

# server 
import socket 

import StructFuncs as struct
import numpy as np

pcHostName = socket.gethostname() 
hostIp = socket.gethostbyname(pcHostName) 
hostPort = 2000 
serverAddress = (hostIp, hostPort)      # create (tuple) 
 

block_values = np.array([1,2,3,4,5,])
packed_values = struct.pack_array(block_values)

start_packaging = False

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
        unpacked_data = struct.unpack_16int(data)
        
        if(unpacked_data == 10):
            print("waiting for end affector to move")
            start_packaging = True
        
        if(start_packaging[0] == True & unpacked_data == 20):
            print("starting packaging")
            
        
        
        #print("[*] Received '", data, "' from the client") 
        #print("    Processing data") 
        #unpacked_data = struct.unpack_array(data)
        #packed_Data = struct.pack_array(np.asarray(unpacked_data[0]))
        
        
        
print("    End of server program.") 

