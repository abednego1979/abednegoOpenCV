# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01
#将图片分隔为左右两个部分
import cv2
images=["d:\\a.b.c.d.png"]
for picName in images:
    img = cv2.imread(picName,cv2.IMREAD_UNCHANGED)
    x,y,z=img.shape
    outImg1=img[:, :int(y/2), :]
    outImg2=img[:, int(y/2):, :]
    picName1=picName.split(".")
    picName1.insert(-1, "_1")
    picName1=".".join(picName1)
    picName2=picName.split(".")
    picName2.insert(-1, "_2")
    picName2=".".join(picName2)
    cv2.imwrite(picName1, outImg1, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    cv2.imwrite(picName2, outImg2, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


