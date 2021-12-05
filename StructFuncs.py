# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 21:35:38 2021

@author: Remon Verbraak

pack and unpack functions for the delta robot
"""


import struct 
import socket 

echo = True


def pack_array(array):
    """Packs a numpy array into an array of float types and returns packed_data[0], byte_code[1] as tuple"""
    byte_code = "<%df" %len(array)
    packed_data  = struct.pack(byte_code,*array) # resultaat: b'\x0f' 
    
    
    if(echo):    
        print(f"Calculated byte code: {byte_code}")
        print(f"packed data:          {packed_data}")
        
    return packed_data, byte_code

def unpack_array(data):
    "Unpacks an array into a float tuple and returns it"
    
    byte_code = "<%df" %(len(data)/4)
    unpacked_data = struct.unpack(byte_code, data)
    
    if(echo):
        print(f"unpacked data  :     {data}")
        print(f"bytecode       :     {byte_code}")
        print(f"unpacked Result:     {unpacked_data}")
        
    return unpacked_data
    


def pack_string(string):
    "packs a variable lenght of a string"
    
    byte_code = '<%ds' %len(string)
    packed_string = struct.pack(byte_code, string.encode('UTF-8'))
    
    if(echo):    
        print(f"Calculated byte code: {byte_code}")
        print(f"packed string         {packed_string}")
        
    return packed_string, byte_code


def unpack_string(data):
    "unpacks a variable lenght of a string"
    
    decoded_data = data.decode('UTF-8')
    if(echo):    
        print(f"unpacked string       {decoded_data}")
        
    return decoded_data



def create_socket(serverAdress):
    raise NotImplementedError()    

def connect_socket(serverAdress):
    raise NotImplementedError()
    
def send_packed(message):
    raise NotImplementedError()    
    
def recieve():
    raise NotImplementedError()    
   
    
    