#!/usr/bin/env python

import serial
import time
from multiprocessing import Process
import camscript

CALLSIGN = 'MATBAL'
FIX = False
fixTime = ''
lattitude = ''
longitude = ''
altitude = ''
logName = 'balloonLog'+time.strftime("-%y-%m-%d-%H:%M:%S")+'.txt'
logfile = open(logName,'w',1)
ser = serial.Serial('/dev/ttyAMA0',9600)

print "-----------------------------------------------------"
print "                HAB SOFTWARE V0.1                    "
print "\n\n\n\n "
print "-----------------------------------------------------"
print "initialising"
print "Telemetry output ->  " + logName
 

#Start camera process
def initCamera():
    print 'Starting camera subprocess'
    p = Process(target=camscript.cameraLoop)
    p.start()
    p.join

#Read and process GPS data
def initGPS():
    global FIX
    while not FIX:
        gpsLine = ser.readline()
        if gpsLine.startswith('$GNRMC'):
             print gpsLine
             data = gpsLine.split(',')
             active = data[2]
             if active.startswith('A'):
                 FIX = True
                 print 'Acquired GPS FIX'

def parseGPS(gpsLine):
    global fixTime,lattitude,longitude,altitude
    
    if gpsLine.startswith('$GNGGA'):
        data = gpsLine.split(',')
        fixTime = data[1]
        lattitude = data[2] + data[3]
        longitude = data[4] + data[5]
        altitude = data[9] + data[10]
        logline = time.strftime("%H:%M:%S")+ '$'+CALLSIGN + ',time:'+fixTime+',lattitude:'+lattitude+',longitude:'+longitude+',altitude:'+altitude
        logfile.write(logline + '\n')
        print logline

initCamera()
initGPS()

while True:
    dataLine = ser.readline()
    parseGPS(dataLine)
    
