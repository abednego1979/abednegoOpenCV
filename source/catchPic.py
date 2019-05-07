# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

#family camera/monitor

import os
import datetime
import time
import sched
import cv2
import threading





__metaclass__ = type

class myCam():
    def __init__(self, dbgFlag=False, savePath="."):
        self.savePath=os.path.join(os.getcwd(), savePath)
        self.capture=cv2.VideoCapture(0)
        self.dbgFlag=dbgFlag
        pass

    def getTimeString(self, x):
        return x.strftime('%Y%m%d_%H%M%S_')+str(x.microsecond)
    
    def savaImage(self, img):
        #这里要考虑区别是否要保存到云端
        fileName=self.getTimeString(datetime.datetime.now())+'.jpg'
        cv2.imwrite(os.path.join(self.savePath, fileName),img)
        print(fileName)
	

    def catchPic(self):
        if self.capture.isOpened():
            if self.dbgFlag:
                pass
            ret,img=self.capture.read()
            self.savaImage(img)
            pass
        
            
        pass

mC=myCam(dbgFlag=True)
while True:
    a=raw_input("Catch?(Enter to catch/q to Quit)")
    if a=="q":
        break
    mC.catchPic()
        
