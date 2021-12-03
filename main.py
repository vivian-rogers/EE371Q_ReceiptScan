#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2
import utils
import time
import os

from stitch import *
from procimg import *

# Prepare the user !


# will wait until user presses given key
def waitTilKey(text,key):
    print(text)
    ready = input()
    while(ready != key):
        print("How about now?")
        ready = input()


# loads all images from a folder
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img0 = cv2.imread(os.path.join(folder,filename))
        img = preproc(img0,-2.5)
        if img is not None:
            images.append(img)
    return images



print("Hello! Prepare your reciept, it will be scanned")
waitTilKey("Ready? Enter \"1\" for ready.","1")

# load up the images
loadpath = "./imgtest"
imgs = load_images_from_folder(loadpath)

# optionally display the images
for img in imgs:
    resized = resize(img,25)
    cv2.imshow("image",resized)
    cv2.waitKey(0)

# stitch together the images
stitched = RGB(stitchImg_wrong(imgs))
if(type(stitched) == int()):
    print("fail")
else:
    cv2.imshow("stitched",resize(stitched,10))
    #cv2.waitKey(0)

# read the images
text, overviewImg = readImg(stitched)

# display overview
cv2.imshow("overview", resize(overviewImg,50))

print(text)

cv2.waitKey(0)

