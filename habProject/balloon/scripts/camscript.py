import time
import picamera
import os 
import logging

def checkDirectories(): 
    #Check to see if a pictures directory exists for today
    dirName = "/var/hab/images/images"+time.strftime("-%y-%m-%d")
    dirExists = os.path.isdir(dirName)
    if dirExists == False:
        print("Directory doesn't exist so creating it now")
        os.mkdir(dirName)	
    print "Camera output ->  " + dirName

def cameraLoop():
    checkDirectories()
    camera = picamera.PiCamera()
    while True:   
        camera.capture("/var/hab/images/images"+time.strftime("-%y-%m-%d")+"/image"+time.strftime("%H:%M:%S")+".jpg")
        time.sleep(150)
	
