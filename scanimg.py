#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2
import utils
import time

from stitch import stitchImg
from procimg import *

# Prepare the user !



def waitTilKey(text,key):
    print(text)
    ready = input()
    while(ready != key):
        print("How about now?")
        ready = input()

print("Hello! Prepare your reciept, it will be scanned")
waitTilKey("Ready? Enter \"1\" for ready.","1")


# Prepare the camera

savepath = "./scanframes"
capture = cv2.VideoCapture(0)
endFlag = False

if (capture.isOpened() != True):
    print("Something is broken, cannot access webcam")
    end

print("Press q when ready to start capturing")
while True: 
    
    ret, frame = capture.read()
    if (ret != True):
        print("Something is broken, cannot read the webcam")
        break
    # Stitch frames if new enough
    # Display the resulting frame
    cv2.imshow('overview', preproc(frame,-2))
    #cv2.imshow('overview', fullscan)
    if cv2.waitKey(1) == ord('q') or endFlag:
        break
    time.sleep(0.1)

# Loop to read from the webcam

imgs = []

fullscan = frame
while True: 
    ret, frame = capture.read()
    if (ret != True):
        print("Something is broken, cannot read the webcam")
        break
    cv2.imshow('overview', preproc(frame,-2))
    
    # Stitch frames if new enough
    fullscan = stitchImg([fullscan,frame])
        #imgs.append(preproc(frame,-2))
    
    # Display the resulting frame
    cv2.imshow('overview', preproc(frame,-2))
    #cv2.imshow('overview', fullscan)
    if cv2.waitKey(1) == ord('q') or endFlag:
        break
    time.sleep(0.5)

cv2.destroyAllWindows()

# When everything done, release the capture
waitTilKey("Ready to stitch image? Enter \"1\" for ready.","1")
capture.release()
fullscan = stitchImg(imgs)
cv2.imshow("stitch",fullscan)
while True:
    if cv2.waitKey(0) == ord('q') or endFlag:
        break


#endFlag, entries, overviewImg = readImg(currentframe, usedframe)

# In[ ]:





# In[ ]:




