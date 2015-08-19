#!/usr/bin/env python

import serial
import time
from multiprocessing import Process
import camscript
import RPi.GPIO as GPIO
import gpsutil
import crcmod

CALLSIGN = 'MATBAL'
FIX = False
fixTime = ''
lattitude = ''
longitude = ''
altitude = ''
logName = '/var/hab/logs/balloonLog'+time.strftime("-%y-%m-%d-%H:%M:%S")+'.txt'
logfile = open(logName,'w',1)
gpsInNavMode = False

crc16f = crcmod.predefined.mkCrcFun('crc-ccitt-false') # function for CRC-CCITT checksum
transmitCounter = 1

print "-----------------------------------------------------"
print "                HAB SOFTWARE V0.1                    "
print "\n\n\n "
print "-----------------------------------------------------"
print "initialising"
print "Telemetry output ->  " + logName
 
def initBoard():
    global GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, False)

#Start camera subprocess
def initCamera():
    print 'Starting camera subprocess'
    p = Process(target=camscript.cameraLoop)
    p.start()
    p.join
    
 def transmitData(dataLine):
     global transmitCounter
     radio = serial.Serial('/dev/ttyAMA0',300, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO)
     radio.write(dataLine)
     transmitCounter++
     radio.close()

#Read and process GPS data
def initGPS():
    global FIX, gpsInNavMode
    ser = serial.Serial('/dev/ttyAMA0',9600)
    #Set to airborne mode and wait for response
    while not gpsInNavMode:
        gpsutil.setUbloxNavMode(ser)
        gpsInNavMode = gpsutil.getUBX_ACK(ser, setNav);
    
    #Wait for fix before continuing
    while not FIX:
        gpsLine = ser.readline()
        if gpsLine.startswith('$GNRMC'):
             print gpsLine
             data = gpsLine.split(',')
             active = data[2]
             if active.startswith('A'):
                 FIX = True
                 GPIO.output(18, True)
                 print 'Acquired GPS FIX'
                 logfile.write('Acquired GPS FIX' + '\n')

    ser.close()

#Extract data from GGA lines. These contain all the info we need for a basic fix
def parseGPS(gpsLine):
    global fixTime,lattitude,longitude,altitude
    
    if gpsLine.startswith('$GNGGA'):
        data = gpsLine.split(',')
        fixTime = data[1]
        lattitude = data[2] + data[3]
        longitude = data[4] + data[5]
        altitude = data[9] + data[10]
        #logline = time.strftime("%H:%M:%S")+ '$'+CALLSIGN + ',time:'+fixTime+',lattitude:'+lattitude+',longitude:'+longitude+',altitude:'+altitude
        #logfile.write(logline + '\n')
        #print logline
        #return logline

def buildTelemetry():
    string = str(CALLSIGN + ',' + fixTime + ',' + str(transmitCounter) + ',' +latitude + ',' + longitude + ',' + altitude) # the data string
    csum = str(hex(crc16f(string))).upper()[2:] # running the CRC-CCITT checksum
    csum = csum.zfill(4) # creating the checksum data
    telem = str("$$" + string + "*" + csum + "\n")
    logfile.write(telem + '\n')
    return telem

#Main program
initBoard()
initCamera()
initGPS()

try:
    i = 1
    while True:
        telemetry = ''
        #Read 4 GPS lines for every radio transmission line
        if i % 5 == 0:
            print 'Fake Radio Transmission'
            buildTelemetry()
            #transmitData()
        else:
            gps = serial.Serial('/dev/ttyAMA0',9600)
            dataLine = gps.readline()
            parseGPS(dataLine)
            gps.close()
        time.sleep(1)
        i++

except KeyboardInterrupt:
    print 'Keyboard Interrupt'
    logfile.write('KEYBOARD INTERRUPT + '\n')
 
#Ensure that all GPIO channels used are reset    
finally:
    logfile.write('Cleaning GPIO pins + '\n')
    GPIO.cleanup()
