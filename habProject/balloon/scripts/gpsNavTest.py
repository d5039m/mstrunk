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
ser = serial.Serial('/dev/ttyAMA0',9600)

#Read and process GPS data
def processGPS():
    global fixTime,lattitude,longitude,altitude
    command = b'\xB5\x62\x06\x24\x24\x00\xFF\xFF\x06\x03\x00\x00\x00\x00\x10\x27\x00\x00\x05\x00\xFA\x00\xFA\x00\x64\x00\x2C\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\xDC'
    ser.write(command)

    while True:
        gpsLine = ser.readline()
        print gpsLine
        if gpsLine.startswith('$GNGGA'):
            data = gpsLine.split(',')
            fixTime = data[1]
            lattitude = data[2] + data[3]
            longitude = data[4] + data[5]
            altitude = data[9] + data[10]

        #logline = time.strftime("%H:%M:%S")+ '$'+CALLSIGN + ',time:'+fixTime+',lattitude:'+lattitude+',longitude:'+longitude+',altitude:'+altitude

        #logfile.write(logline + '\n')
        #time.sleep(10)

processGPS()
