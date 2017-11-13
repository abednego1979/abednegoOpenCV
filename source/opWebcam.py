# -*- coding: utf-8 -*-

#Python 2.7.x
import os
import datetime
import time
import sched
import cv2
import threading
import Queue


####通用函数###############################################################
def getTimeString(x):
    return x.strftime('%Y%m%d_%H%M%S_')+str(x.microsecond)

#将[time.time(), image]作为元素的列表，转化为视频
def storeImageArray2Video(saveFile, imArray, fps, size):
    
    if not imArray:
        return
    
    videoWriter=cv2.VideoWriter(saveFile, cv2.cv.CV_FOURCC('I','4','2','0'), fps, size)
    saved_frameNum=0
    startTime,frame=imArray.pop(0)
    old_frame=frame
        
    while imArray:
        curTime,frame=imArray.pop(0)
        #过去的时间里，应该记录的帧数是(curTime-startTime)*fps，已经记录的saved_frameNum帧，所以应该增加记录(curTime-startTime)*fps-saved_frameNum帧
        for i in range(int((curTime-startTime)*fps-saved_frameNum)):
            videoWriter.write(old_frame)
        old_frame=frame
        saved_frameNum=(curTime-startTime)*fps
    videoWriter.release()


####拍照功能###############################################################
def period_capPic_action(schedule, savePath, inc, capture, remainNum):

    if not remainNum:
        return
    
    # 安排inc秒后再次运行自己，即周期运行
    if remainNum>1:
        schedule.enter(inc, 0, period_capPic_action, (schedule, savePath, inc, capture, remainNum-1))
    else:
        schedule.enter(1, 0, period_capPic_action, (schedule, savePath, inc, capture, remainNum-1))

    #action
    ret,img=capture.read()
    cv2.imwrite(os.path.join(savePath, getTimeString(datetime.datetime.now())+'.jpg'),img)
    print '.',
    
    pass

def period_capPic_exe(schedule, savePath, inc, capture, remainNum):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动 
    schedule.enter(inc, 0, period_capPic_action, (schedule, savePath, inc, capture, remainNum))
    # 持续运行，直到计划时间队列变成空为止 
    schedule.run()


def capPicture(savePath='', capNum=1, inc=5.0):
    if not savePath:
        savePath = os.getcwd()
    
    capture=cv2.VideoCapture(0)
    size = (int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    if capture.isOpened():
        #read frame
        if capNum<=0:
            pass
        elif capNum==1:
            print 'Try to Cap Picture'
            ret,img=capture.read()
            cv2.imwrite(os.path.join(savePath, getTimeString(datetime.datetime.now())+'.jpg'),img)
            pass
        else:
            # 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数 
            # 第二个参数以某种人为的方式衡量时间 
            schedule = sched.scheduler(time.time, time.sleep)
            
            ret,img=capture.read()
            cv2.imwrite(os.path.join(savePath, getTimeString(datetime.datetime.now())+'.jpg'),img)
            print '.',
            
            remainNum = capNum-1
            period_capPic_exe(schedule, savePath, inc, capture, remainNum)
            pass
            
    #close cam
    capture.release()
    
    pass

####录像功能##################################################################
def capVideo_Task(q, endTime, capture):
    success,frame=capture.read()
    
    while success and time.time()<endTime:
        success,frame=capture.read()
        q.put([time.time(), frame])

    
def capVideo(savePath='', timeLen=5.0):
    saveFile=str(datetime.datetime.now()).replace(':', '-')+'.avi'
    if not savePath:
        savePath = os.getcwd()
    cameraCapture=cv2.VideoCapture(0)
    fps=30
    size = (int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    if cameraCapture.isOpened():
        numFrameAll = int(timeLen*fps)
        
        #创建队列
        q = Queue.Queue(maxsize = int(fps*(timeLen+3.0)))
        #创建任务
        t = threading.Thread(target=capVideo_Task, args=(q, time.time()+timeLen+2.0, cameraCapture))
        t.start()
        #等待任务结束
        t.join()
        
        #从队列中读取image并写入文件
        print "Start to write file...",
        imArray=[]
        while not q.empty():
            imArray.append(q.get())
            
        if not imArray:
            startTime=imArray[0][0]
            imArray = [item for item in imArray if (item[0]-startTime)<=timeLen]
            
        storeImageArray2Video(os.path.join(savePath, saveFile), imArray, fps, size)
        
        cameraCapture.release()#把摄像头也顺便关了 
        print "Done",
    

####图像动态监测功能##################################################################
def capVideoMotionDetector_saveVideo(saveFile, fps, size, inputFrames):
    #对图像做灰度，然后做高斯模糊
    grayFrames = [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in inputFrames]
    gaussFrames = [cv2.GaussianBlur(frame, (21, 21), 0) for frame in grayFrames]
    
    #计算每一帧和第一帧的不同
    delteFrames = [cv2.absdiff(gaussFrames[0], frame) for frame in gaussFrames]
    #得到差值图像的黑白图
    threshFrames = [cv2.threshold(frame, 25, 255, cv2.THRESH_BINARY)[1] for frame in delteFrames]
    # 扩展阀值图像填充孔洞，然后找到阀值图像上的轮廓
    contourFrames = [cv2.dilate(frame, None, iterations=2) for frame in threshFrames]

    contours = [cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) for frame in contourFrames]
    
    for i in range(len(inputFrames)):#每个图像
        occupied_text='Not Occupied'
        for c in contours[i]:# 遍历轮廓
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue
            #计算轮廓的边界框，在当前帧中画出该框
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(inputFrames[i], (x, y), (x + w, y + h), (0, 255, 0), 2)
            occupied_text='Occupied'
            pass
        cv2.putText(inputFrames, "Room Status: {}".format(occupied_text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(inputFrames, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, inputFrames.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        pass
    
    videoWriter=cv2.VideoWriter(saveFile, cv2.cv.CV_FOURCC('I','4','2','0'), fps, size)
    for frame in inputFrames:
        videoWriter.write(frame)
    videoWriter.release()#如果不用release方法的话无法储存，要等结束程序再等摄像头关了才能显示保持成功
    return

def period_capVideo_action(schedule, q, inc, capture):
    # 安排inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, period_capVideo_action, (schedule, savePath, inc, capture, cv2, remainNum-1))

    #action
    ret,img=capture.read()
    if ret:
        q.put([time.time(), img])
    else:
        q.put([time.time(), None])

def period_capVideo_exe(schedule, q, inc, capture):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动 
    schedule.enter(inc, 0, period_capVideo_action, (schedule, q, inc, capture))
    # 持续运行，直到计划时间队列变成空为止 
    schedule.run()

def capVideoMotionDetector_Task(q, inc, capture):
    #利用调度器实现定时
    schedule = sched.scheduler(time.time, time.sleep)
    period_capVideo_exe(schedule, q, inc, capture)


def capVideoMotionDetector_entry(savePath='', inc=0.5):
    if not savePath:
        savePath = os.getcwd()
        
    cameraCapture=cv2.VideoCapture(0)
    size = (int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    
    old_frame = None
    recordFrames=[]
    saved_frameNum = 0
    
    if cameraCapture.isOpened():
        #启动一个新任务开始拍照，拍完的照片要通过队列传回这里，这里主程序主要进行影像的处理
        #1.启动队列
        q = Queue.Queue(maxsize = 30)
        #2.创建任务
        t = threading.Thread(target=capVideoMotionDetector_Task, args=(q, inc, cameraCapture))
        t.start()
        #t.join()#不要等待线程结束
        
        cur_frame=None
        while True:
            #read the queue
            if q.empty():
                pass
            else:
                capTime,image=q.get()
                cur_frame = image
            
                #proc image
                assert 0
            
            
            #显示当前帧并记录用户是否按下按键
            if cur_frame:
                cv2.imshow("Security Feed", frame)
            #等待用户按键结束录像
            key = cv2.waitKey(1) & 0xFF
            # 如果q键被按下，跳出循环
            if key == ord("q"):
                break
        
        cameraCapture.release()#把摄像头关 
        



def mainEntry():
    print '---MODE 0:\t Cap picture(s)'
    print '---MODE 1:\t Cap a video'
    print '---MODE 2:\t Move detect'
    
    mode=int(raw_input('run mode: '))
    
    
    if mode==0:#抓取一张图片
        capNum=0
        while 0==capNum:
            capNum = int(float(raw_input("Picture Number to Cap:")))
        inc=0
        while 0==inc:
            inc = float(raw_input("Cap interval(seconds):"))
        capPicture(capNum, inc)
    
    if mode==1:#抓取N秒的一段视频
        capVideo(savePath='D:\\', timeLen=10.0)
        
    if mode==2:#图像检测
        capVideoMotionDetector_entry()
        
def mainEntryAuto():
    capPicture(capNum=3600*24, inc=30)
    
    
if __name__ == '__main__':
    mainEntryAuto()
