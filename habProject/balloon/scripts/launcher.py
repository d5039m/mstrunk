#!/usr/bin/env python 
import os
from time import sleep
from multiprocessing import Process

#My modules
import camscript
import gpsscript
#This process should only ever be run as a script and not imported.
#1. Load any configuration
#2. Set up GPS receiver
#3. Start Camera Thread
#4. Start GPS Thread
#5. Main processing thread

def loadConfig():
    pass

def initGPS():
    pass

def startCamera():
    p = Process(target=camscript.cameraLoop)
    p.start()
    p.join

    i = 1
    while True:
        print i
        i = i + 1
        sleep(1)

def startGPS():
    pass




print 'Raspberry Pi Flight Computer Version 0.0.1'
print '=========================================='

loadConfig()
initGPS()
startCamera()

	
