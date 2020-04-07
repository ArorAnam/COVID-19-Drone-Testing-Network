#!/usr/bin/env python

import socket
import time

#First item is a code A means ok. B means drone not available.
GPS = "A 12.345 12.345"
GPSByte = GPS.encode()
list_of_IDS = ["123456789", "111111111", "000000000"]
TCP_IP = '127.0.0.1'
TCP_PORT = 6792
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response


def ReceievePatientInfo():
    #define local variable for patient listening port
    PatientPort = ''

    print('HOSPIAL:')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT)) #bind server to address and port number
    s.listen(1)

    #Define a function to check IDS
    def IDChecker(y):
        for x in list_of_IDS:
            if (x == y):
                return 1
            #print("not equal", x, "and", list_ofIDS)

        return 0



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
        if PatientInfo:
          ValidID = IDChecker(PatientInfo[1])
          if ValidID == 1:
              print('ID is valid')
              print ("Patient info Recieved: Priority -", PatientInfo[2], ". Lat: ", PatientInfo[3], " Lon: ", PatientInfo[4])
              #Store Patient's Listening property
              PatientPort = PatientInfo[5]
              continue
          else:
              print('ID is not valid')
              continue
        else:
            break


    conn.close()

    s.close()

    return PatientPort
#end of ReceievePatientInfo function


def SendPatientDroneInfo(PatientPort):
    TCP_PORT_PATIENT = int(PatientPort)

    Message = "Hey hi hey hello"
    MessageByte = Message.encode()

    #Contacts Patient
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((TCP_IP, TCP_PORT_PATIENT))
    except IOError:
        print('couldnt connect. Retrying')
        time.sleep(3)
        try:
            s.connect((TCP_IP, TCP_PORT_PATIENT))
        except IOError:
            print('Could not connect. Please Retry later.')
            s.close()
            exit()

    print("\nConnection with patient Established")
    time.sleep(3)

    s.send(MessageByte)
    print("\nDrone Delivery details sent to Patient")

    s.close()

    time.sleep(3)
    print("\nConnection closed with patient")
#end of SendPatientDroneInfo function


#Process calling
PP = ReceievePatientInfo()
SendPatientDroneInfo(PP)
