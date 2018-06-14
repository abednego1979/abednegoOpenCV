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
import Queue




__metaclass__ = type

class myCam():
    MIN_CAP_NUM=1
    MIN_CAP_INC=0.1
    
    def __init__(self, dbgFlag=False, savePath=".", capNum=self.MIN_CAP_NUM, capInc=self.MIN_CAP_INC):
        self.savePath=os.path.join(os.getcwd(), savePath)
        self.capNum=max(int(capNum), self.MIN_CAP_NUM)
        self.capInc=max(float(capInc), self.MIN_CAP_INC)
        
        self.capture=cv2.VideoCapture(0)
        self.dbgFlag=dbgFlag
        pass
    
    def setCapNum(self, capNum):
        self.capNum=max(int(capNum), self.MIN_CAP_NUM)
    
    def setCapInc(self, capInc):
        self.capInc=max(float(capInc), self.MIN_CAP_INC)
        
    def savaImage(self, img):
        #这里要考虑区别是否要保存到云端
        cv2.imwrite(os.path.join(self.savePath, self.getTimeString(datetime.datetime.now())+'.jpg'),img)
        
    def run(self):
        
        size = (int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
        
        if self.capture.isOpened():
            #read frame
            if self.capNum==1:
                if self.dbgFlag:
                    print ('Try to Cap Picture')
                ret,img=self.capture.read()
                self.savaImage(img)
                pass
            else:
                # 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数 
                # 第二个参数以某种人为的方式衡量时间 
                self.schedule = sched.scheduler(time.time, time.sleep)
                ret,img=self.capture.read()
                self.savaImage(img)
                if self.dbgFlag:
                    print ('.',)
            
                remainNum = self.capNum-1
                period_capPic_exe(remainNum)

        #close cam
        self.capture.release()
        
    def getTimeString(self, x):
        return x.strftime('%Y%m%d_%H%M%S_')+str(x.microsecond)
    def period_capPic_exe(self, remainNum):
        # enter用来安排某事件的发生时间，从现在起第n秒开始启动 
        self.schedule.enter(self.capInc, 0, period_capPic_action, (remainNum))
        # 持续运行，直到计划时间队列变成空为止 
        self.schedule.run()
        
    def period_capPic_action(self, remainNum):
        if not remainNum:
            return
        
        # 安排inc秒后再次运行自己，即周期运行
        if remainNum>1:
            self.schedule.enter(self.capInc, 0, self.period_capPic_action, (remainNum-1))
        else:
            self.schedule.enter(1, 0, self.period_capPic_action, (remainNum-1))
    
        #action
        ret,img=self.capture.read()
        self.savaImage(img)
        if self.dbgFlag:
            print ('.',)
        
#mC=myCam(dbgFlag=True)
#mC.setCapNum(5)
#mC.setCapInc(1.0)
#mc.run()


