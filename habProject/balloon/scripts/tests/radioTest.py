#!/usr/bin/env python

import serial
import time

print 'Opening serial port to radio, 300bps, 8bit, no parity, two stop'
ser = serial.Serial('/dev/ttyAMA0',300, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO)

try:
    while True:
        print("Sending Radio Beacon message")
        ser.write("RADIO BEACON TEST")
	time.sleep(1)
        
except KeyboardInterupt:
    print "Program shutdown from keyboard"
	
finally:
    ser.close()     
