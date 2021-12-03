#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2
from imutils.perspective import four_point_transform
import utils
import pytesseract

def resizePix(img,pix0,pix1):
    dim = (int(pix0), int(pix1))
    return  cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def resizeH(img,pix0):
    scaling = pix0/img.shape[0]
    width = int(img.shape[1] * scaling)
    height = pix0
    dim = (width, height)
    
    return  cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def resize(img,scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    return  cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def readImg(rawframe): #post-process and get text from img
    nx = rawframe.shape[1]; ny = rawframe.shape[0]
    scale = 0.18
    
    # initialize parameters to return
   
    blur_img, edges = postproc(rawframe)

    # generate contours on image
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=3)
    edges = resizePix(edges,nx,ny)
    


    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contoured_img = rawframe.copy()
    cv2.drawContours(image=contoured_img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    print("Looping through contours to find the one that can be approximated by a rectangle")
    for edge in contours:

        #approximate the contour
        perim = cv2.arcLength(edge, True)
        approx = cv2.approxPolyDP(edge, 0.05 * perim, True)

        #Area = cv2.contourArea(contour)
        #print("Area = "+str(Area))
        # if it has 4 corners, bingo!
        if(len(approx) == 4):
            doc_edge = approx
            break
    
    outline_rcpt = rawframe.copy() 
    cv2.drawContours(image=outline_rcpt, contours=[doc_edge], contourIdx=-1, color=(0, 255, 0), thickness=4, lineType=cv2.LINE_AA)

    # final step, transform the reciept to upright
    warp_rcpt = four_point_transform(rawframe, doc_edge.reshape(4, 2))
    #proc_rcpt = warp_rcpt
    proc_rcpt = pretextproc(warp_rcpt)
    

    # put together a nice overview with a given height
    height = 1500
    rs_warp_rcpt = resizeH(warp_rcpt,height)
    cv2.imshow("rcpt",rs_warp_rcpt)
    outline_rcpt = resizeH(outline_rcpt,height)
    edges = RGB(resizeH(edges,height))
    rawframe = resizeH(rawframe,height)
    ov_proc_rcpt = resizeH(proc_rcpt,height)
    

     

    overviewImg = cv2.hconcat([rawframe,edges,outline_rcpt,rs_warp_rcpt,ov_proc_rcpt])
    print("Generating text from image")
    text = pytesseract.image_to_string(proc_rcpt)
    #file = open("receiptscan.txt", "a") 
    #print(text)
    #file.write(text)
    #file.write("\n")
    

    return text, overviewImg

def pretextproc(orig_rcpt):
    #blur = 3
    
    kernel = np.ones((4,4),np.uint8)
    orig_rcpt = greyImg(orig_rcpt)
    
    rcpt = cv2.adaptiveThreshold(orig_rcpt, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 5)
    #rcpt = cv2.morphologyEx(rcpt, cv2.MORPH_OPEN, kernel)
    rcpt = cv2.morphologyEx(rcpt, cv2.MORPH_CLOSE, kernel)
    #blurimg = greyImg(blurImg(rcpt,blur))
    return RGB(rcpt)

def postproc(rawframe):
    nx = rawframe.shape[1]; ny = rawframe.shape[0]
    blur = 31 # arbitrary blur value, in pixels. needs to be odd
    threshold1 = 10; threshold2 = 50 # upper and lower thresholds for canny edge detection
    scaling = 0.2 # 
    
    #start post-processing stitched image
    #preresize_blur = blurImg(rawframe,11) # get rid of some of the noise outside the img, don't change text
    blur_img = blurImg(resizePix(rawframe,nx*scaling,ny*scaling),blur)
    edges = edgeDetect(blur_img, threshold1, threshold2)
    
    # resize image back to full
    #blur_img = resizePix(blur_img,nx,ny)
    #edges = resizePix(edges,nx,ny)
    return blur_img, edges



def sq(img): # squares and rounds image
    return np.square(img)

def preproc(img,C):
    blur = 101
    #grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #hsv = cv2.cvtColor(blurImg(img,blur), cv2.COLOR_BGR2HSV)
    (H, S, V) = cv2.split(hsv)
    S = blurImg(S,blur)
    #thresh = cv2.adaptiveThreshold(V, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_TOZERO, 11, 5)
    thresh = cv2.adaptiveThreshold(V, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 8)
    addS = thresh.astype(np.float32) + C*S.astype(np.float32) 
    
    #show(finalimg)
    #print("type of final = ",type(thresh))

    #thresh = cv2.adaptiveThreshold(img, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    bmax = 255; bmin = 1
    finalimg = np.clip(255*(addS - bmin)/(bmax - bmin), 0,255)
   # finalimg = cv2.adaptiveThreshold(
    return RGB(finalimg.astype(np.uint8))
    #return RGB(finalimg.astype(np.uint8))

def RGB(img):
    return cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

def greyImg(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blurImg(img, rad):
    return cv2.GaussianBlur(img,(rad,rad),0)

def edgeDetect(img,t1,t2):
    #return cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=rad)
    return cv2.Canny(image=img, threshold1=t1, threshold2=t2)

# In[ ]:
def show(img):
    while True:
        cv2.namedWindow("test", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions
        cv2.resizeWindow("test", 1500, 800)
        cv2.imshow("test",img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyWindow("test")
            break




