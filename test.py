from procimg import *

import cv2

def show(img):
    while True:
        cv2.namedWindow("test", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions
        cv2.resizeWindow("test", 1500, 800)
        cv2.imshow("test",img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyWindow("test")
            break

img_pre = cv2.imread("./oldimgs/IMG_20211130_200856.jpg")
img = preproc(img_pre,-1)
entries, overviewImg = readImg(img)

#img = cv2.resize(img_pre, (1500, 1000)) 

show(overviewImg)

b5 = blurImg(img,5)
show(b5)
b10 = blurImg(img,10)
show(b10)
b20 = blurImg(img,20)
show(b20)

