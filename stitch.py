#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2
import utils
import imutils

from procimg import *




def stitchImg_wrong(imglist):
    #stitcher = cv2.Stitcher_create(mode=0)
    stitcher = cv2.Stitcher_create(mode=1)
    (status, img) = stitcher.stitch(imglist)
    
    #turn the black boundary white
    # decided to invert colors, this is legacy code
    """black_pixels = np.where(
        (img[:, :, 0] == 0) & 
        (img[:, :, 1] == 0) & 
        (img[:, :, 2] == 0)
    )

    # set those pixels to white
    img[black_pixels] = [255, 255, 255]
    """
    if(status == 0):
        # add a boundary so the edge finder doesn't bug
        size = 200
        img = cv2.copyMakeBorder(img, size, size, size, size, cv2.BORDER_CONSTANT, None, [0,0,0])
        return greyImg(img)
    else:
        print("You broke it... Here is debugging, try again")
        return status

def stitchImg(imgs):
    # insert preprocessing here
    

    #imglist = []
    #imglist.append(im0)
    #imglist.append(imd)
    #stitcher = cv2.createStitcher()
    # match keypoints using SIFT
    #siftImg = cv2.SIFT()
    siftImg = cv2.xfeatures2d.SIFT_create()
    
    kps = []
    desc = []
    for img in imgs:
        keypoint, description = siftImg.detectAndCompute(img,None)
        kps.append(keypoint)
        desc.append(description)
        kp_img = cv2.drawKeypoints(img,keypoint,None)
        cv2.imshow("keypoints",resize(kp_img,40))
        cv2.waitKey(0)


    # determine how matchy they are
    # if high, do not want -- redundant info
    # if low, do not want -- not enough info
    
    ### determine score here
    score = 0
    contFlag = True
    if(score > 0.5 and score < 0.9):
        ### do stuff to concatenate images
        return img[0], contFlag
    else:
        return img[0], contFlag

