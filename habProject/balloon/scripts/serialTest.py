#!/usr/bin/env python

import serial
import time
from multiprocessing import Process
import camscript

CALLSIGN = 'MATBAL'

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
def processGPS():
    global fixTime,lattitude,longitude,altitude
    while True:
        gpsLine = ser.readline()
        if gpsLine.startswith('$GNGGA'):
            data = gpsLine.split(',')
            fixTime = data[1]
            lattitude = data[2] + data[3]
            longitude = data[4] + data[5]
            #print 'FixQuality:'+ data[6]
            #print 'Satelites:' + data[7]
            #print 'Horizontal Dilution:'+ data[8]
            altitude = data[9] + data[10]
            #print 'Height of Geoid:'+ data[11] + data[12]

        logline = time.strftime("%H:%M:%S")+ '$'+CALLSIGN + ',time:'+fixTime+',lattitude:'+lattitude+',longitude:'+longitude+',altitude:'+altitude
#        print logline

        logfile.write(logline + '\n')
        time.sleep(10)

initCamera()
processGPS()
