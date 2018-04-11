# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01


#scan picture to book tools

from math import *
import numpy as np
import cv2

def readImage(picName):
    img = cv2.imread(picName,cv2.IMREAD_UNCHANGED)
    return img

def showImage(img, showTime=0, style=''):
    if not style:
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow('img',img)
    cv2.waitKey(showTime)
    cv2.destroyAllWindows()
    
def writeImage(picName, img):
    if picName.lower().endswith(".jpg"):
        cv2.imwrite(picName, img, [int( cv2.IMWRITE_JPEG_QUALITY), 95])
    elif picName.lower().endswith(".png"):
        cv2.imwrite(picName, img, [int( cv2.IMWRITE_PNG_COMPRESSION), 9])
    else:
        assert 0,"Output picture name postfix error!"
    return

#扫描后的文档图片，需要
#1.裁剪，这需要鼠标选择有效区域
#2.旋转摆正

picFiles=["feng1.jpg", "feng2.jpg", "feng4.jpg", "IMG_001.jpg", "IMG_002.jpg", "IMG_003.jpg"]
examplePic='feng1.jpg'



def getXYofValidImage(picName):
    img=readImage(picName)

    length_width_ratio=0.75
    
    y=img.shape[0]/2    #纵向
    x=img.shape[1]/2    #横向
    
    step=[1,10,100]
    step_index=2
    
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    while True:
        img_draw=img.copy()
        cv2.rectangle(img_draw, (0, 0), (x, y), (255,255,0), 3)
        cv2.putText(img_draw,'step:%d' % step[step_index],(img.shape[1]/2,img.shape[0]/2),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,0),5)
        
        cv2.imshow('img',img_draw)
        cv2.waitKey(100)
        
        key=cv2.waitKey(0)
        if key == ord('q'):
            break
        if key == ord('a'):
            x-=step[step_index]
            x=max(x,0)
        if key == ord('d'):
            x+=step[step_index]
            x=min(x,img.shape[1])
        if key == ord('w'):
            y-=step[step_index]
            y=max(y,0)
        if key == ord('s'):
            y+=step[step_index]
            y=min(y,img.shape[0])
        if key == ord('e'):
            step_index=(step_index+1)%len(step)
    
    
    #print ("(%d, %d)" % (x,y))
    cv2.destroyAllWindows()
    return (x,y)

def batchProcPic(picList, x, y, prefix='proc_'):
    for picFile in picList:
        print ("Proc:"+picFile)
        img=readImage(picFile)
        outImg=img[:y, :x, :]
        writeImage(prefix+picFile, outImg)
        
    pass


x,y=getXYofValidImage(examplePic)
print ("(%d, %d)" % (x,y))

r=raw_input("batch?(Y/n)")
if 'y'==r.lower():
    batchProcPic(picFiles, x, y)


