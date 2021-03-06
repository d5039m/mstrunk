#!/usr/bin/env python

import serial
import time
from multiprocessing import Process
import camscript
import RPi.GPIO as GPIO
import crcmod
import logging

logName = '/var/hab/logs/balloonLog'+time.strftime("-%y-%m-%d-%H:%M:%S")+'.txt'
logging.basicConfig(filename=logName ,format='%(asctime)s %(message)s',level=logging.DEBUG)

CALLSIGN = 'MATBAL'

gpsData = {'fixTime':'','lattitude':'','longitude':'','altitude':''}
FIX = False
gpslog  = open('/var/hab/gps/gpsdata'+time.strftime("-%y-%m-%d-%H:%M:%S")+'.txt','w',1)
gpsInNavMode = False

crc16f = crcmod.predefined.mkCrcFun('crc-ccitt-false') # function for CRC-CCITT checksum
transmitCounter = 1

print "-----------------------------------------------------"
print "                HAB SOFTWARE V0.1                    "
print "-----------------------------------------------------"
print "initialising flight software"
print "Telemetry output ->  " + logName
logging.info("Initialising - CALLSIGN:" + CALLSIGN)
def millis():
        return int(round(time.time() * 1000))

#calcuate expected UBX ACK packet and parse UBX response from GPS
def getUBX_ACK(MSG):
        b = 0
        ackByteID = 0
        ackPacket = [0 for x in range(10)]
        startTime = millis()

        print "Reading ACK response: "
	logging.info("Reading ACK response: ")
        
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
        logging.info("Waiting for UBX ACK reply:")
 
        while 1:
                #test for success
                if ackByteID > 9 :
                        #all packets are in order
                        print "(SUCCESS!)"
			logging.info("(SUCCESS!)")
                        return True

                #timeout if no valid response in 3 secs
                if millis() - startTime > 3000:
                        print "(FAILED!)"
			logging.warning('(FAILED!)')
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

def initBoard():
    print 'Setting gpio pins'
    logging.info('initialising gpio pins')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, False)

#Start camera subprocess
def initCamera():
    print 'Starting camera subprocess \n'
    logging.info('starting camera subprocess')
    p = Process(target=camscript.cameraLoop)
    p.start()
    p.join
    
def transmitData(dataLine):
    radio = serial.Serial('/dev/ttyAMA0',300, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO)
    #radio.write(dataLine + "\n")
    radio.close()

#Read and process GPS data
def initGPS():
    global gpsInNavMode
    
    #Set to airborne mode and wait for response
    while not gpsInNavMode:
        print "Sending UBX Navmode Command: "
        setNav = bytearray.fromhex("B5 62 06 24 24 00 FF FF 06 03 00 00 00 00 10 27 00 00 05 00 FA 00 FA 00 64 00 2C 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 16 DC")
        logging.info('Sending UBX Navmode command:'+ setNav)
        ser.write(setNav)
        ser.write("\r\n")
        print 'UBX command sent'
        logging.info('UBX command send')
        gpsInNavMode = getUBX_ACK(setNav);
    
    print 'Disabling non GGA NMEA sentences from UBLOX'
    logging.info('Disabling non GGA NMEA sentences')
    ser.write("$PUBX,40,GLL,0,0,0,0*5C\r\n")
    ser.write("$PUBX,40,GSA,0,0,0,0*4E\r\n")
    ser.write("$PUBX,40,RMC,0,0,0,0*47\r\n")
    ser.write("$PUBX,40,GSV,0,0,0,0*59\r\n")
    ser.write("$PUBX,40,VTG,0,0,0,0*5E\r\n")                 

#Extract data from GGA lines. These contain all the info we need for a basic fix
def parseGPS(gpsLine):
    global FIX
    if gpsLine.startswith('$GNGGA'):
        data = gpsLine.split(',')
        gpsData['fixTime'] = data[1]
        gpsData['lattitude'] = data[2] + data[3]
        gpsData['longitude'] = data[4] + data[5]
        gpsData['numsats'] = data[7]
        gpsData['altitude'] = data[9] + data[10]

        if not FIX:
            if int(gpsData['numsats']) > 3:
                FIX = True
                GPIO.output(18, True)
                print 'Acquired GPS FIX'
                logging.info('Acquired GPS Fix')  

def buildTelemetry():
    string = str(CALLSIGN + ',' + gpsData['fixTime'] + ',' + str(transmitCounter) + ',' +gpsData['lattitude'] + ',' + gpsData['longitude'] + ',' + gpsData['altitude']) # the data string
    csum = str(hex(crc16f(string))).upper()[2:] # running the CRC-CCITT checksum
    csum = csum.zfill(4) # creating the checksum data
    telem = str("$$" + string + "*" + csum)
    logging.info(telem)
    return telem

#Main program
ser = serial.Serial('/dev/ttyAMA0',9600)
initBoard()
initCamera()
initGPS()
ser.close()
try:
    while True:
        gps = serial.Serial('/dev/ttyAMA0',9600) 
        dataLine = gps.readline()
        gpslog.write(dataLine)
        print 'GPSDATA:' + dataLine.rstrip('\n')
        parseGPS(dataLine)
        gps.close()

        telemString = buildTelemetry()

        print 'Fake Radio Transmission ' + telemString
        transmitCounter += 1
        transmitData(' ')
        
except KeyboardInterrupt:
    print 'Keyboard Interrupt'
 
#Ensure that all GPIO channels used are reset    
finally:
    GPIO.cleanup()
