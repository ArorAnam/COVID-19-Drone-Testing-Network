#!/usr/bin/env python

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 6789
BUFFER_SIZE = 1024
TCP_Listening_PORT = 6794


def SendPatientData():
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
    print("\n Connection with General Practitioner closed")
#end of Patient send Function

#now wait for message from the Hospital
def ReceiveDroneInfo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', TCP_Listening_PORT))  #bind server to address and property
    s.listen(1)

    #Feedback from Hospital
    conn, addr = s.accept()
    print("\nConnection address:", addr)
    while 1:
        try:
            droneETA = conn.recv(BUFFER_SIZE)
        except ConnectionResetError:
            print("\nIssue reading in data")
            continue

        EtaDecoded = droneETA.decode()
        DroneInfo = EtaDecoded.split()

        print("\nConnection Established with Hospital")
        time.sleep(3)
        print("\nMessage :: ", EtaDecoded)
        break

    conn.close()
    print("\nConnection with hospital closed")
    s.close()

Name = input("\nEnter Patient Name :: ")
SendPatientData()
ReceiveDroneInfo()
print('\n Connection closed')
