#!/usr/bin/env python

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 6789
BUFFER_SIZE = 1024


#Below are the test cases
#Simply comment out the ones not being used

#Test case 1 - Valid ID
GPS = "P 35 TF 98.800 98.800" 

#Test case 2 - Not Valid ID
#GPS = "100000000 98.765 98.765" 

print('CLIENT:')

GPSByte = GPS.encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((TCP_IP, TCP_PORT))
except IOError:
    print('couldnt connect. Retrying')
    time.sleep(3)
    try: 

        s.connect((TCP_IP, TCP_PORT))
    except IOError:
        print('Could not connect. Retry later.')
        s.close()
        exit()

s.send(GPSByte)

s.close()
print('\n Connection closed')