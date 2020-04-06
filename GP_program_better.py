#!/usr/bin/env python

import socket
import time
from array import *
import math

#First item is a code A means ok. B means drone not available.
GPS = "GP 123456789 H 12.345 12.345"
GPSByte = GPS.encode()
TCP_IP = '127.0.0.1'
TCP_PORT = 6789
TCP_PORT_Hospital = 6795 

#Hash Table using gps coordinates of hospitals as Keys
#Storing actual port number to contact. 
Hospital_Contact_Table = {'12.500000 12.500000':'6795','13.100000 13.200000':'6792'} 

#Array containing Hospital_coordinates
Hospital_coordinates = [[12.500, 12.500],[13.100, 13.200]] 

#Hash table with distance as key and gps as value
distance_HashTable = {}


BUFFER_SIZE = 1024  # Normally 1024, but we want fast response


#Define a function to calculate distance between client and hospitals
#Using Haversine formula which takes earth curvature into account
def CalcDist(x1,x2,y1,y2):
    R = 6371.0 #Radius of earth in km
    
    lat1 = math.radians(x1)
    lat2 = math.radians(x2)
    lon1 = math.radians(y1)
    lon2 = math.radians(y2)
    
    dist_lon = lon2-lon1
    dist_lat = lat2-lat1
    
    #Haversine formula
    a = math.sin(dist_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dist_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = round(R*c)

    return distance
#end of CalcDist function


#define this process as a function
def GPWork():
  weightPriority = 0
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', TCP_PORT)) #bind server to address and port number
  s.listen(1)

  #Request from Patient
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
    
      min_dist = 9999999 #variable to store minimum distance
      x1 = float(PatientInfo[3])
      y1 =  float(PatientInfo[4])
      row_count = 0
      for r in Hospital_coordinates:
          x2 = Hospital_coordinates[row_count][0]
          y2 = Hospital_coordinates[row_count][1]
          row_count += 1 #increment row count
          distance = CalcDist(x1,x2,y1,y2)
          #Store in Hash table with distance as key and gps as value
          distance_HashTable[distance] = "%f %f"%(x2, y2)
          if distance < min_dist:
             min_dist = distance
        

      location_closest = distance_HashTable[min_dist]
      TCP_PORT_Hospital = Hospital_Contact_Table[location_closest]
      Message = "GP 123456789 %s %s %s"%(Priority, PatientInfo[3], PatientInfo[4])
      MessageByte = Message.encode()
      break
	
  conn.close()
  print("\n Sending info to Hospital..\n")
  weightPriority = 0

  s.close()

  TCP_PORT_Hospital = int(TCP_PORT_Hospital)
  # Contacts Hospital
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
      s.connect((TCP_IP, TCP_PORT_Hospital))
  except IOError:
      print('couldnt connect. Retrying')
      time.sleep(3)
      try: 
          s.connect((TCP_IP, TCP_PORT_Hospital))
      except IOError:
          print('Could not connect. Retry later.')
          s.close()
          exit()

  s.send(MessageByte)

  s.close()
  print("\n Connection with Hospital closed")
#end of GPWork Function

print('Verified General Practitioner:')

Work = 'Y'
while Work == 'Y':
  Work = input("\nGP working? Y/N \n")
  if Work != 'Y':
     break
  for count_work in range(0,2): #run loop 2 times
      GPWork()

