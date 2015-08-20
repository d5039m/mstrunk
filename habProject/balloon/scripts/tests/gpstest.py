#!/usr/bin/env python

#When run this script should:
# 1. open a serial connection to the UBLOX gps
# 2. Set UBLOX to airborne mode and check for ACK back
# 3. Disable all NMEA sentences apart from GGA
# 4. read and print out 1 gps sentence to console per second
# Therefore should see a stream of GGA sentences

import serial
import time

def millis():
        return int(round(time.time() * 1000))

#calcuate expected UBX ACK packet and parse UBX response from GPS
def getUBX_ACK(MSG):
        b = 0
        ackByteID = 0
        ackPacket = [0 for x in range(10)]
        startTime = millis()

        print "Reading ACK response: "
        
        #construct the expected ACK packet
        ackPacket[0] = int('0xB5', 16) #header
        ackPacket[1] = int('0x62', 16) #header
        ackPacket[2] = int('0x05', 16) #class
        ackPacket[3] = int('0x01', 16) #id
        ackPacket[4] = int('0x02', 16) #length
        ackPacket[5] = int('0x00', 16)
        ackPacket[6] = MSG[2] #ACK class
        ackPacket[7] = MSG[3] #ACK id
        ackPacket[8] = 0 #CK_A
        ackPacket[9] = 0 #CK_B

        #calculate the checksums
        for i in range(2,8):
                ackPacket[8] = ackPacket[8] + ackPacket[i]
                ackPacket[9] = ackPacket[9] + ackPacket[8]

        #print expected packet
        #print "Expected ACK Response: "
        #for byt in ackPacket:
        #        print byt
                
        print "Waiting for UBX ACK reply:"
        while 1:
                #test for success
                if ackByteID > 9 :
                        #all packets are in order
                        print "(SUCCESS!)"
                        return True

                #timeout if no valid response in 3 secs
                if millis() - startTime > 3000:
                        print "(FAILED!)"
                        return False
                #make sure data is availible to read
                if ser.inWaiting() > 0:
                        b = ser.read(1)
                        #check that bytes arrive in the sequence as per expected ACK packet
                        if ord(b) == ackPacket[ackByteID]:
                                ackByteID += 1
                                print ord(b)
                        else:
                                ackByteID = 0 #reset and look again, invalid order
###############
# MAIN PROGRAM
###############

ser = serial.Serial('/dev/ttyAMA0',9600)

gpsInNavMode = False

#Set to airborne mode and wait for response
while not gpsInNavMode:
    print "Sending UBX Navmode Command: "
    setNav = bytearray.fromhex("B5 62 06 24 24 00 FF FF 06 03 00 00 00 00 10 27 00 00 05 00 FA 00 FA 00 64 00 2C 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 16 DC")
    ser.write(setNav)
    ser.write("\r\n")
    print 'UBX command sent'
    gpsInNavMode = getUBX_ACK(setNav);
    
print 'Disabling non GGA NMEA sentences from UBLOX'
ser.write("$PUBX,40,GLL,1,1,0,0*5C\r\n")
ser.write("$PUBX,40,GSA,1,1,0,0*4E\r\n")
ser.write("$PUBX,40,RMC,1,1,0,0*47\r\n")
ser.write("$PUBX,40,GSV,1,1,0,0*59\r\n")
ser.write("$PUBX,40,VTG,1,1,0,0*5E\r\n")   

while True:
    gpsLine = ser.readline()
    print gpsLine
    time.sleep(1)

processGPS()
