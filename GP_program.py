#!/usr/bin/env python

import socket
import time

#First item is a code A means ok. B means drone not available.
GPS = "GP 123456789 H 12.345 12.345"
GPSByte = GPS.encode()
TCP_IP = '127.0.0.1'
TCP_PORT = 6789
TCP_PORT_Hospital1 = 6795 
TCP_PORT_Hospital2 = 6792
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

weightPriority = 0

print('Verified General Practitioner:')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT)) #bind server to address and port number
s.listen(1)

#First Patient
conn, addr = s.accept()
print("Connection address:", addr)
while 1:
    try:
        data = conn.recv(BUFFER_SIZE)
    except ConnectionResetError:
        print("Issue reading in data.")
        continue

    dataDecoded = data.decode()
    PatientInfo = dataDecoded.split()
    
    print ("Patient info Recieved: Age -", PatientInfo[1])
    if int(PatientInfo[1]) >= 60:
        weightPriority += 20
    else:
        weightPriority += 10
    	
    if PatientInfo[2] == "CFTA":
    	weightPriority += 30
    	print ("\n Symptoms: Cough, Fever, Tiredness, difficult breathing")
    else:
    	weightPriority += 10
    	print ("\n Symptoms: Tiredness, Fever")
    	
    if weightPriority > 20:
    	Priority = "H"
    	print ("\n Priority: High")
    else: 
    	Priority = "M"  
    	print ("\n Priority: Medium")
    	
    GPS1 = "GP 123456789 %s %s %s"%(Priority, PatientInfo[3], PatientInfo[4])
    GPSByte1 = GPS1.encode()
    break
	
conn.close()
print("\n Connection with patient closed \n")
weightPriority = 0

#Second Patient
s.listen(1)
conn, addr = s.accept()
print("Connection address:", addr)
while 1:
    try:
        data = conn.recv(BUFFER_SIZE)
    except ConnectionResetError:
        print("Issue reading in data.")
        continue

    dataDecoded = data.decode()
    PatientInfo = dataDecoded.split()
    
    print ("Patient info Recieved: Age -", PatientInfo[1])
    if int(PatientInfo[1]) >= 60:
       weightPriority += 20
    else:
       weightPriority += 10
    	
    if PatientInfo[2] == "CFTA":
    	weightPriority += 30
    	print ("\n Symptoms: Cough, Fever, Tiredness, difficult breathing")
    else:
    	weightPriority += 10
    	print ("\n Symptoms: Tiredness, Fever")
    	
    if weightPriority > 20:
    	Priority = "H"
    	print ("\n Priority: High")
    else: 
    	Priority = "M"  
    	print ("\n Priority: Medium")
    	
    GPS2 = "GP 123456789 %s %s %s"%(Priority, PatientInfo[3], PatientInfo[4])
    GPSByte2 = GPS2.encode()
    break
	
conn.close()
print("\n Connection with patient closed")

s.close()

# Contacts first Hospital
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((TCP_IP, TCP_PORT_Hospital1))
except IOError:
    print('couldnt connect. Retrying')
    time.sleep(3)
    try: 
        s.connect((TCP_IP, TCP_PORT_Hospital1))
    except IOError:
        print('Could not connect. Retry later.')
        s.close()
        exit()

s.send(GPSByte1)

s.close()
print("\n Connection with Hospital closed")


# Contacts Second Hospital
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((TCP_IP, TCP_PORT_Hospital2))
except IOError:
    print('couldnt connect. Retrying')
    time.sleep(3)
    try: 
        s.connect((TCP_IP, TCP_PORT_Hospital2))
    except IOError:
        print('Could not connect. Retry later.')
        s.close()
        exit()

s.send(GPSByte2)

s.close()
print("\n Connection with Hospital closed")