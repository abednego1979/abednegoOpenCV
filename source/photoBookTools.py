# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01


#photo book tools

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


def revolveImage(img, angle):
    if not angle:
        return img
    else:
        height,width=img.shape[:2]
        #旋转后的尺寸
        heightNew=int(width*fabs(sin(radians(angle)))+height*fabs(cos(radians(angle))))
        widthNew=int(height*fabs(sin(radians(angle)))+width*fabs(cos(radians(angle))))        

        matRotation=cv2.getRotationMatrix2D((width/2,height/2),angle,1)
        
        matRotation[0,2] +=(widthNew-width)/2  #重点在这步，目前不懂为什么加这步
        matRotation[1,2] +=(heightNew-height)/2  #重点在这步
        
        imgRotation=cv2.warpAffine(img,matRotation,(widthNew,heightNew),borderValue=(255,255,255))
        
        return imgRotation

#图像缩放
def zoomImage(img, scale=1.0):
    if type(scale)==type(1.0):
        return cv2.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_CUBIC)
    else:
        return cv2.resize(img, (scale[1], scale[0]), interpolation=cv2.INTER_CUBIC)

#图像锐化
def sharpImage(img, kernel=np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])):
    return cv2.filter2D(img, -1, kernel)

#对一个图像，通过画框的方式，人工圈定一个区域，并取得这个区域的坐标范围。为后继的切割等操作提供参数
def getRealImageRange(img, unSelFieldColour='GRAY', showScale=1.0, preAngle=0):
    procImg=img.copy()
    
    #先按照设定的角度旋转图像
    procImg = revolveImage(procImg, preAngle)
    
    
    maxRect_High=procImg.shape[0]
    maxRect_Wide=procImg.shape[1]
    selRect_up=int(maxRect_High/4)
    selRect_down=int(3*maxRect_High/4)
    selRect_left=int(maxRect_Wide/4)
    selRect_right=int(3*maxRect_Wide/4)
    step=max(int(min(maxRect_High, maxRect_Wide)/200)*2, 2)
    halfStep=int(step/2)
    
    picRevolve=0    #图像旋转角度
    
    unSelColourDic={'RED':[0,0,1], 'YELLOW':[0,1,0], 'BLUE':[1,0,0], 'WHITE':[1,1,1], 'BLACK':[0,0,0]}

    while True:
        #先按照设定的角度旋转图像
        tempProcImg = revolveImage(procImg, picRevolve)
        
        #防止由于旋转而导致选择框出界
        maxRect_High=tempProcImg.shape[0]
        maxRect_Wide=tempProcImg.shape[1]        
        selRect_down=min(selRect_down, tempProcImg.shape[0])
        selRect_right=min(selRect_right, tempProcImg.shape[1])
        selRect_up=min(selRect_up, selRect_down)
        selRect_left=min(selRect_left, selRect_right)
        
        
        if unSelFieldColour in unSelColourDic.keys():
            colourImg=np.zeros(tempProcImg.shape, np.uint8)
            for index,i in enumerate(unSelColourDic[unSelFieldColour]):
                if i:
                    colourImg[...,index]=np.ones(tempProcImg.shape[:2])*255
                else:
                    colourImg[...,index]=np.zeros(tempProcImg.shape[:2])
            showImg=colourImg
        elif unSelFieldColour=='GRAY':
            grayImg = cv2.cvtColor(tempProcImg,cv2.COLOR_BGR2GRAY)
        
            #由于灰度图是降维的，这里要合并图像所以要升维，将灰度图变为彩色图
            grayImg = grayImg[..., np.newaxis]
            grayImg=np.concatenate((grayImg,grayImg,grayImg), axis=2)
            
            showImg=grayImg
        else:
            assert 0, "input unSelFieldColour is error"
        
        #替换区域为原彩色图
        showImg[selRect_up:selRect_down,selRect_left:selRect_right,:] = tempProcImg[selRect_up:selRect_down,selRect_left:selRect_right,:]
        box=np.array([[selRect_left, selRect_down], [selRect_left, selRect_up], [selRect_right, selRect_up], [selRect_right, selRect_down]])
        cv2.drawContours(showImg, [box], 0, (255, 0, 0), 2)
        
        #show grayImg        
        #根据键盘输入决定选择框的
        if 0.0==showScale:
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.imshow('image',showImg)
        else:
            cv2.imshow('image',zoomImage(showImg, scale=showScale))
        key=cv2.waitKey(0)
        
        if key == ord('w'):  #'w' move up the select rect
            if selRect_up >= step:
                selRect_up-=step
                selRect_down-=step
            else:
                selRect_down-=selRect_up
                selRect_up=0
            pass
        elif key == ord('s'):  #'s' move down the select rect
            if selRect_down+step <= maxRect_High:
                selRect_up+=step
                selRect_down+=step
            else:
                selRect_up+=(maxRect_High-selRect_down)
                selRect_down=maxRect_High
            pass
        elif key == ord('a'):  #'s' move left the select rect
            if selRect_left >= step:
                selRect_left-=step
                selRect_right-=step
            else:
                selRect_right-=selRect_left
                selRect_left=0
            pass
        elif key == ord('d'):  #'s' move right the select rect
            if selRect_right+step <= maxRect_Wide:
                selRect_left+=step
                selRect_right+=step
            else:
                selRect_left+=(maxRect_Wide-selRect_right)
                selRect_right=maxRect_Wide
            pass
        elif key == ord(','):  #',' zoom out (smaller) the select rect, up and down
            selRect_up = selRect_up+halfStep if (selRect_down-selRect_up)>step else selRect_up
            selRect_down = selRect_down-halfStep if (selRect_down-selRect_up)>step else selRect_down
            pass
        elif key == ord('.'):  #'.' zoom in (bigger) the select rect, up and down
            selRect_up=max(0, selRect_up-halfStep)
            selRect_down=min(maxRect_High, selRect_down+halfStep)
            pass
        elif key == ord('n'):  #',' zoom out (smaller) the select rect, left and right
            selRect_left = selRect_left+halfStep if (selRect_right-selRect_left)>step else selRect_up
            selRect_right = selRect_right-halfStep if (selRect_right-selRect_left)>step else selRect_right                       
            pass
        elif key == ord('m'):  #',' zoom out (smaller) the select rect, left and right
            selRect_left=max(0, selRect_left-halfStep)
            selRect_right=min(maxRect_Wide, selRect_right+halfStep)            
            pass
        elif key == ord('i'):  #'i' to turn left the picture
            picRevolve-=0.1
            pass
        elif key == ord('o'):  #'o' to turn right the picture
            picRevolve+=0.1
            pass
        elif key == ord('y'):  #'y' to ok
            cv2.destroyAllWindows()
            break
        else:
            pass
        
        #print ([picRevolve, selRect_up, selRect_down-selRect_up, selRect_left, selRect_right-selRect_left])
        
    return (picRevolve+preAngle, selRect_up, selRect_down, selRect_left, selRect_right)

#选择图像的一部分
def selImagePart(img, angle, rect):
    #对图像转过angle角度
    tempProcImg = revolveImage(img, angle)
    objImg = tempProcImg[rect[0]:rect[1], rect[2]:rect[3], :]
    return objImg
    




def foo(fileList, examplePic):
    img=readImage(examplePic)
    
    
    if 1:
        #奇数页(2.7755575615628914e-17, 555, 3845, 285, 2745)
        #偶数页(1.0999999999999999, 600, 3890, 390, 2850)
        selRect=(1.0999999999999999, 600, 3890, 390, 2850)
    else:
        selRect=getRealImageRange(img, unSelFieldColour='GRAY', showScale=0.0, preAngle=0)
    print (selRect)
    
    while True:
        x=input("continue to proc?(Y/n)")
        if 'n'==x.lower():
            break
        elif 'y'==x.lower():
            for picFile in picFiles:
                print ("Proc:"+picFile)
                img=readImage(picFile)
                outImg=sharpImage(selImagePart(img, selRect[0], selRect[1:]))
                outImg=zoomImage(outImg, scale=(2048,1536))
                outImg = cv2.cvtColor(outImg,cv2.COLOR_BGR2GRAY)
                writeImage('proc_'+picFile, outImg)
            break
        else:
            pass
        
picFiles=["02.jpg", "04.jpg", "06.jpg", "08.jpg"]
examplePic='026.jpg'        
foo(picFiles, examplePic)
