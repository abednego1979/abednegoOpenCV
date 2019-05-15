# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

#family camera/monitor

import os
import datetime
import cv2
from PIL import Image,ImageEnhance
import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol

__metaclass__ = type

class myQrDetector():
    def __init__(self, dbgFlag=False, saveFile="./qr_record"):
        self.saveFile=os.path.join(os.getcwd(), saveFile)
        #self.capture=cv2.VideoCapture("myCreateVideo.mp4")
        self.capture=cv2.VideoCapture(0)
        self.dbgFlag=dbgFlag
        self.img=None
        
    def __del__(self):
        self.capture.release()
    
    def getTimeString(self, x):
        return x.strftime('%Y%m%d_%H%M%S')
    
    def getImage(self):
        if self.capture.isOpened():
            if self.dbgFlag:
                pass
            return self.capture.read()
        else:
            return False,None
        
    def save2File(self, text):
        try:
            with open(self.saveFile, "a") as pf:
                pf.write(text)
        except:
            pass
                
        
    def detect(self):
        rval,img=self.getImage()
        if rval:
            #转换为Image识别的格式
            img=Image.fromarray(img)
        
            #灰度化
            img = img.convert("L")
            
            #识别
            barcodes = pyzbar.decode(img, symbols=[ZBarSymbol.QRCODE])
            #print ("barcodes:",barcodes)
            if len(barcodes):
                for barcode in barcodes:
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    barcodeRect = barcode.rect
                    barcodePolygon = barcode.polygon
                    print (barcodeData)
                    print (barcodeType)
                    print (barcodeRect)
                    print (barcodePolygon)
                    self.save2File(self.getTimeString(datetime.datetime.now())+": "+barcodeData+"\r\n")
                return len(barcodes)
            return 0
            
                
                

mC=myQrDetector(dbgFlag=True)
while True:
    a=input("Catch?(Enter to catch/q to Quit)")
    if a=="q":
        del mC
        break
    mC.detect()
print ("Exit!")
        
