# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 21:35:38 2021

@author: Remon Verbraak

pack and unpack functions for the delta robot
"""


import struct 
import socket 

echo = False

def pack_16int(value):
    """Packs an integer, returns packed_int as byte code"""
    packed_int = struct.pack(">2h", value)
    
    return packed_int

def unpack_16int(value):
    """unpacks a 16 bits integer bytecode into a tuple"""
    unpacked_int = struct.unpack(">2h", value)
    
    return unpacked_int

def pack_array(array):
    """Packs a numpy array into an array of float types and returns packed_data as byte code"""
    byte_code = ">%df" %len(array)
    packed_data  = struct.pack(byte_code,*array) # resultaat: b'\x0f' 
    
    
    if(echo):    
        print(f"Calculated byte code: {byte_code}")
        print(f"packed data:          {packed_data}")
        
    return packed_data

def unpack_array(data):
    "Unpacks an array into a float tuple and returns it"
    
    byte_code = ">%df" %(len(data)/4)
    unpacked_data = struct.unpack(byte_code, data)
    
    if(echo):
        print(f"unpacked data  :     {data}")
        print(f"bytecode       :     {byte_code}")
        print(f"unpacked Result:     {unpacked_data}")
        
    return unpacked_data
    


def pack_string(string):
    "packs a variable lenght of a string"
    
    byte_code = '>%ds' %len(string)
    packed_string = struct.pack(byte_code, string.encode('UTF-8'))
    
    if(echo):    
        print(f"Calculated byte code: {byte_code}")
        print(f"packed string         {packed_string}")
        
    return packed_string


def unpack_string(data):
    "unpacks a variable lenght of a string"
    
    byte_code = ">%ds" %len(data)
    unpacked_data = struct.unpack(byte_code, data)
    if(echo):    
        print(f"unpacked string       {unpacked_data}")
        
    return unpacked_data[0].decode('UTF-16')



def create_socket(serverAdress):
    raise NotImplementedError()    

def connect_socket(serverAdress):
    raise NotImplementedError()
    
def send_packed(message):
    raise NotImplementedError()    
    
def recieve():
    raise NotImplementedError()    
   
    
    