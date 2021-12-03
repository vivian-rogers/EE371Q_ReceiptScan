#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2
import utils
from procimg import readImg

# Prepare the user !

print("Hello! Prepare your reciept, it will be scanned")
print("Ready? Enter True or False.")
ready = bool(input())
while(ready != True):
    print("How about now?")
    ready = input()



# Prepare the camera

savepath = "./scanframes"
capture = cv2.VideoCapture(0)
endFlag = False

if (capture.isOpened() != True):
    print("Something is broken, cannot access webcam")
    end

# Loop to read from the webcam

while True: 
    ret, frame = capture.read()
    if (ret != True):
        print("Something is broken, cannot read the webcam")
        break
    
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    endFlag, entries, overviewImg = readImg(frame)
    # Display the resulting frame
    cv2.imshow('overview', overviewImg)
    if cv2.waitKey(1) == ord('q') or endFlag:
        img = frame.copy()
        break
# When everything done, release the capture
cv2.imwrite("./imgtest/test.png",img)
capture.release()
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:




