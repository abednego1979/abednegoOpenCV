# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

#photo book tools

from math import *
import numpy as np
import cv2


#row == height == Point.y
#col == width  == Point.x

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
        cv2.imwrite(picName, img)
    elif picName.lower().endswith(".png"):
        cv2.imwrite(picName, img)
    else:
        assert 0,"Output picture name postfix error!"
    return





def foo(picFiles, labeledMatrixPic):
    img = readImage(labeledMatrixPic)
    
    #标记和得到示例图片中各个标定点的坐标位置
    #田字格的9个标定点
    #按下1-9选择当前编辑对象，默认是1
    #选择某个编辑对象后，显示的是标定点周围的区域。并且可以Zoom in或Zoom out，以及上下左右移动图像
    #
    High=img.shape[0]
    Width=img.shape[1]
    #初始化标记点的坐标
    labeledPointPos=[[int(Width/2),int(High/2)] for i in range(9)]
    for i in range(9):
        labeledPointPos[i][0]+=int((int(i%3)-1)*Width/3)
        labeledPointPos[i][1]+=int((int(i/3)-1)*High/3)
    
    curEditPointIndex=0         #当前编辑的标记点的编号（0-8）
    SHOW_RANGE=300          #显示curZoomScale*SHOW_RANGE见方的区域
    step=[1,10,100]
    step_index=2
    
    procImg=img.copy()
    while True:
        #显示labeledPointPos[curEditPointIndex]附近的SHOW_RANGE见方的窗口区域，可以通过asdw移动这个窗口，同时也可以通过fght移动定位的十字
        
        #左上角位置
        pointer1=labeledPointPos[curEditPointIndex].copy()
        pointer1[0]-=int(SHOW_RANGE/2)
        pointer1[1]-=int(SHOW_RANGE/2)        
        #右下角位置
        pointer2=labeledPointPos[curEditPointIndex].copy()
        pointer2[0]+=int(SHOW_RANGE/2)
        pointer2[1]+=int(SHOW_RANGE/2)
    
        if pointer1[0]<0:
            pointer1[0]=0
            pointer2[0]=SHOW_RANGE
        if pointer1[1]<0:
            pointer1[1]=0
            pointer2[1]=SHOW_RANGE
        if pointer2[0]>Width:
            pointer1[0]=Width-SHOW_RANGE
            pointer2[0]=Width
        if pointer2[1]>High:
            pointer1[1]=High-SHOW_RANGE
            pointer2[1]=High
        
        #显示pointer1和pointer2之间的区域
        showImg=procImg[pointer1[1]:pointer2[1], pointer1[0]:pointer2[0], :]
        showImg=showImg.copy()
        #在relativeCrossPos(标记点相对左上角的位置)位置画十字线
        relativeCrossPos=[labeledPointPos[curEditPointIndex][0]-pointer1[0], labeledPointPos[curEditPointIndex][1]-pointer1[1]]
        showImg=cv2.line(showImg,(relativeCrossPos[0]-20,relativeCrossPos[1]),(relativeCrossPos[0]+20,relativeCrossPos[1]),(255,0,0),2)
        showImg=cv2.line(showImg,(relativeCrossPos[0],relativeCrossPos[1]-20),(relativeCrossPos[0],relativeCrossPos[1]+20),(255,0,0),2)
        #将当前步长显示出来
        cv2.putText(showImg,'step:%d' % step[step_index],(relativeCrossPos[0]+5,relativeCrossPos[1]-5),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        #将当前编辑点的编号显示出来
        cv2.putText(showImg,'curEdit:%d' % curEditPointIndex,(relativeCrossPos[0]+5,relativeCrossPos[1]+20),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        
        #显示图像，并让用户进行键盘操作
        #cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.imshow('img',showImg)
        key=cv2.waitKey(0)
        
        if key == ord('w'):  #'w' :标记点上移
            labeledPointPos[curEditPointIndex][1]-=step[step_index]
            labeledPointPos[curEditPointIndex][1]=max(labeledPointPos[curEditPointIndex][1], 0) #不要越界
        elif key == ord('s'):  #'s' :标记点下移
            labeledPointPos[curEditPointIndex][1]+=step[step_index]
            labeledPointPos[curEditPointIndex][1]=min(labeledPointPos[curEditPointIndex][1], High)#不要越界
        elif key == ord('a'):  #'a' :标记点左移
            labeledPointPos[curEditPointIndex][0]-=step[step_index]
            labeledPointPos[curEditPointIndex][0]=max(labeledPointPos[curEditPointIndex][0], 0)#不要越界
        elif key == ord('d'):  #'d' :标记点右移
            labeledPointPos[curEditPointIndex][0]+=step[step_index]
            labeledPointPos[curEditPointIndex][0]=min(labeledPointPos[curEditPointIndex][0], Width)#不要越界
        elif key >= ord('0') and key <= ord('8'):  #'0'-'8' :选择标记点
            curEditPointIndex=key-ord('0')
        elif key == ord('e'):  #'e' :set step
            step_index=(step_index+1)%len(step)
        elif key == ord('y'):  #'y' :结束
            print (labeledPointPos)
            cv2.destroyAllWindows()
            break        
            
    while True:
        x=input("continue to proc?(Y/n)")
        if 'n'==x.lower():
            break
        elif 'y'==x.lower():
            for picFile in picFiles:
                print ("Proc:"+picFile)
                img=readImage(picFile)
                #将9个坐标点围成的4个矩形仿射到4个子图，然后合成为一个图
                #labeledPointPos
                p1=labeledPointPos[0]
                p2=labeledPointPos[2]
                p3=labeledPointPos[6]
                p4=labeledPointPos[8]
                objWidth=768
                objHigh=1024
                pts1=np.float32([p1, p2, p3, p4])
                pts2=np.float32([[0,0], [objWidth, 0], [0, objHigh], [objWidth, objHigh]])
                M = cv2.getPerspectiveTransform(pts1,pts2)
                outImg = cv2.warpPerspective(img,M,(objWidth,objHigh))
                
                writeImage('proc_'+picFile, outImg)
            break
        else:
            pass
    


picFiles=["book003.jpg", "book005.jpg", "book007.jpg"]
labeledMatrixPic='book003.jpg'
foo(picFiles, labeledMatrixPic)
