# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

import config

import cv2
import pygame
import numpy as np
from settings import Settings

class Picture():
    def __init__(self, image):
        self.global_settings=Settings()
        
        self.rawImage = image.copy()       #原始图像
        self.tempImage=[{'image':image.copy(), 'action':'None'}]      #中间图像，之所以定义为列表，是希望能多保存一些过程图像，用于回退操作
        
        #显示相关
        self.isNeedUpdate=True      #是否需要刷新显示，初始化为True，让系统刷新显示一次，以后每次图形变化以后，设置需要刷新，让系统再次刷新。否则系统不刷新
        
    
    def add2ImgBuf(self, image, imageType):
        if self.tempImage[0]['action'] == imageType:
            self.tempImage.pop(0)
            self.tempImage.insert(0, {'image':image, 'action':imageType})
        else:
            self.tempImage.insert(0, {'image':image, 'action':imageType})
            #self.tempImage=self.tempImage[:self.global_settings.MAX_PIC_BUF_LEN]
        pass
    
    def getCurTempImg(self):
        return self.tempImage[0]['image'].copy()
    
    def getCurTempImgType(self):
        return self.tempImage[0]['action']
    
    def ImgBufLen(self):
        return len(self.tempImage)
    
    def ImgBufPop(self, index=0):
        self.tempImage.pop(index)
        
    def getImageParams(self):
        return self.ImageParams
    
    def _rotate(self, img, angle):
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, scale=1.0)
        return cv2.warpAffine(img, M, (w, h))
    
    def rotate(self, angle):      #旋转
        while self.getCurTempImgType() == 'blackwhite' or self.getCurTempImgType() == 'gray':
            self.undo()

        if self.getCurTempImgType() == 'rotate':
            self.ImgBufPop(0)
            assert self.getCurTempImgType() != 'rotate'
        
        img=self.getCurTempImg()
        img = self._rotate(img, angle)
        config.setRotateAngle(angle)
        self.add2ImgBuf(img, 'rotate')
        self.isNeedUpdate=True
        
    def _trapezoid_trans(self, img, factor):
        rows, cols = img.shape[:2]
        src_points = np.float32([[0, 0], [cols-1, 0], [0, rows-1], [cols-1, rows-1]])
        if factor>=0.0:#收窄下边宽度
            dst_points = np. float32([[0, 0], [cols-1, 0], [int(0+factor*cols), rows-1], [int(cols-1-factor*cols), rows-1]])
        else:#收窄上边宽度
            tempfactor=-1*factor
            dst_points = np. float32([[int(0+tempfactor*cols), 0], [int(cols-1-tempfactor*cols), 0], [0, rows-1], [cols-1, rows-1]])
        projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        return cv2.warpPerspective(img, projective_matrix, (cols, rows))          

    
    def trapezoid_trans(self, factor=1.0):      #梯形变换
        while self.getCurTempImgType() == 'blackwhite' or self.getCurTempImgType() == 'gray':
            self.undo()
        #梯形变换就是一个"射影变换"
        #参考：https://vlight.me/2018/06/25/OpenCV-Recipes-Genometric-Transformations/
        if self.getCurTempImgType() == 'trapezoid':
            self.ImgBufPop(0)
            assert self.getCurTempImgType() != 'trapezoid'
        
        img=self.getCurTempImg()
        img=self._trapezoid_trans(img, factor)
        config.setTrapezoidFactor(factor)
        self.add2ImgBuf(img, 'trapezoid')
        self.isNeedUpdate=True
        pass
    
    def _parallelograms_trans(self, img, factor):
        rows, cols = img.shape[:2]
        src_points = np.float32([[cols//2, 0], [0, rows-1], [cols-1, rows-1]])  #选择顶边中点，左下角，右下角共3个点
        dst_points = np.float32([[cols//2+int(factor*cols), 0], [0, rows-1], [cols-1, rows-1]])   #通过修改顶边中点做仿射
        affine_matrix = cv2.getAffineTransform(src_points, dst_points)
        return cv2.warpAffine(img, affine_matrix, (cols, rows))        
    
    def parallelograms_trans(self, factor=1.0):     #平行四边形变换
        while self.getCurTempImgType() == 'blackwhite' or self.getCurTempImgType() == 'gray':
            self.undo()        
        #平行四边形变换就是一个"仿射变换"，给定三个点的变换前后关系，推算出矩阵，用矩阵去变换
        #参考：https://vlight.me/2018/06/25/OpenCV-Recipes-Genometric-Transformations/
        
        if self.getCurTempImgType() == 'parallelograms':
            self.ImgBufPop(0)
            assert self.getCurTempImgType() != 'parallelograms'
            
        img=self.getCurTempImg()
        img = self._parallelograms_trans(img, factor)
        config.setParallelogramsFactor(factor)
        self.add2ImgBuf(img, 'parallelograms')
        self.isNeedUpdate=True
        pass
    
    def _zoom(self, img, scale):
        return cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
    
    def zoom(self, scale=1.0):     #缩放
        while self.getCurTempImgType() == 'blackwhite' or self.getCurTempImgType() == 'gray':
            self.undo()        
        #图像处理的时候，缩放没有什么效果，但是可以让生成的图片体积减小。所以在做缩放的时候，在程序界面上要显示当前图像的大小
        if self.getCurTempImgType() == 'zoom':
            self.ImgBufPop(0)
            assert self.getCurTempImgType() != 'zoom'
        
        img=self.getCurTempImg()
        img = self._zoom(scale)
        
        config.setZoomScale(scale)
        
        self.add2ImgBuf(img, 'zoom')
        self.isNeedUpdate=True
        pass
    
    def _gray(self, img):
        return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    
    def gray(self):     #灰度化
        if self.getCurTempImgType() == 'blackwhite':
            #当前图片是黑白图，不能再转成灰度图
            self.undo()
        
        if self.getCurTempImgType() == 'gray':
            #当前图片已经是灰度图
            self.undo()
        
        img=self.getCurTempImg()
        img_gray = self._gray(img)
        
        config.setGrayFlag(True)
        
        self.add2ImgBuf(img_gray, 'gray')
        self.isNeedUpdate=True
        pass
    
    def _blackwhite(self, img, thresh):
        ret, img = cv2.threshold(img, thresh=thresh, maxval = 255, type = cv2.THRESH_BINARY)
        return img
    
    def blackwhite(self, thresh):       #黑白化
        if self.getCurTempImgType()=='blackwhite':
            #当前图片已经是黑白图
            self.undo()
            
        if self.getCurTempImgType()=='gray':#只有灰度图能二值化
            img = self.getCurTempImg()
            img = self._blackwhite(img, thresh)
            config.setBlackwhiteFlag(True)
            config.setBlackwhiteThresh(thresh)
            self.add2ImgBuf(img, 'blackwhite')
            self.isNeedUpdate=True
        pass
    
    def _select(self, img, selRect):
        left=selRect[0]
        top=selRect[1]
        right=selRect[2]
        bottom=selRect[3]        
        return img[top:bottom, left:right, :]
    
    def select(self, img):   #选择
        selRect = config.getSelRect()       #selRect 分别是 left，top， right，bottom
        left=selRect[0]
        top=selRect[1]
        right=selRect[2]
        bottom=selRect[3]
        
        img=img.copy()
        
        img = cv2.line(img, pt1=(left, top), pt2=(left, bottom), color=(0,0,255), thickness=1)       #左边线
        img = cv2.line(img, pt1=(right, top), pt2=(right, bottom), color=(0,0,255), thickness=1)       #右边线
        img = cv2.line(img, pt1=(left, top), pt2=(right, top), color=(0,0,255), thickness=1)       #上边线
        img = cv2.line(img, pt1=(left, bottom), pt2=(right, bottom), color=(0,0,255), thickness=1)       #下边线

        return img
    
    def batch(self):        #批量处理
        pass
    
    def undo(self):         #回退
        if self.ImgBufLen()>=2:
            self.ImgBufPop(0)
            self.isNeedUpdate=True
        pass
    
    
    def grid(self, image):     #布置网格线
        if not config.getGridOnFlag():
            return image.copy()
        
        pos = config.getGridPos()
        internal = config.getGridInternal()
        
        #出于使用方便的目的，网格线关键的参数只有缩放比例和位置
        img=image.copy()
        (h, w) = img.shape[:2]
        
        x,y=pos
        
        xArray=[x]
        i=0
        while True:
            i+=1
            if x+i*internal < w:
                xArray.append(x+i*internal)
            if x-i*internal > 0:
                xArray.append(x-i*internal)

            if x+i*internal >= w and x-i*internal <= 0:
                break
        
        yArray=[y]
        i=0
        while True:
            i+=1
            if y+i*internal < h:
                yArray.append(y+i*internal)
            if y-i*internal > 0:
                yArray.append(y-i*internal)

            if y+i*internal >= h and y-i*internal <= 0:
                break        
    
        for x in xArray:
            img = cv2.line(img, pt1=(x, 0), pt2=(x, h), color=(0,255,0), thickness=1)
        for y in yArray:
            img = cv2.line(img, pt1=(0, y), pt2=(w, y), color=(0,255,0), thickness=1)        
        
        return img
    
    def cvimage_to_pygame(self, image):
        """Convert cvimage into a pygame image"""
        image = image[...,[2,1,0]]      #cv2,默认读取的图像是BGR的，先转化为RGB
        return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")
    
    def show(self, showArea):
        #显示图像
        
        #画网格线
        img=self.grid(self.getCurTempImg())
        
        #画选择线
        img=self.select(img)
        
        #将图像转化为适合showArea区域
        (h, w) = img.shape[:2]
        Scale = min(1.0, showArea.width/w, showArea.height/h)
        img = cv2.resize(img, (0, 0), fx=Scale, fy=Scale, interpolation=cv2.INTER_NEAREST)
        (h, w) = img.shape[:2]
        
        #构造一个showArea大小的黑色背景图片,并转化为BGR三通道
        blackBG = np.ones((showArea.height, showArea.width, 3),dtype=np.uint8)
        
        #如果是灰度或者黑白图，只有一个通道，为了嵌入背景，需要转化为三通道图像
        if len(img.shape)==2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        #将图像嵌入黑色背景图片
        blackBG[showArea.height//2-h//2:showArea.height//2-h//2+h, showArea.width//2-w//2:showArea.width//2-w//2+w, :] = img
        img = blackBG

        if False:   #调试时查看图像
            cv2.namedWindow("Image") 
            cv2.imshow("Image", img) 
            cv2.waitKey (0) 
            cv2.destroyAllWindows()
        
        #将当前图像的变换参数写在图像上
        paraInfo=config.getFormatParams()
        for index, line in enumerate(paraInfo):
            img=cv2.putText(img, line, (5,20+index*20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
        
        #cv2格式的图片转化为pygame格式图片
        img = self.cvimage_to_pygame(img)
        
        #显示合成后的图片
        #显示放在主循环中
        return img
    
    def batch(self):
        '''
        获取目录下的所有图片，按保存的图片处理顺序，批量处理图片
        '''
        
        actionArray=[item['action'] for item in self.tempImage].reverse()
        assert actionArray[0]=="None"
        actionArray.pop(0)
        
        PicFilePath,PicFileName,PicFileExt=config.getPicFilePathAndExt()
        
        #遍历图片路径
        objlist = os.listdir(PicFilePath)
        for i in range(len(list)):
            path = os.path.join(PicFilePath,list[i])
            
            if os.path.isfile(path) and path.endswith(PicFileExt):
                #这是一个与操作示例图片类型一样的图片
                
                try:
                    self.DoBatch(path, actionArray)
                except:
                    print ("Error at Proc %s" % path)
        pass
    
    
    def DoBatch(self, picPath, actionArray):
        #读取图片文件
        img = cv2.imread(picPath, cv2.IMREAD_UNCHANGED)
        
        
        for action in actionArray:
            if action == 'rotate':
                img = self._rotate(img, config.getRotateAngle())
            elif action == 'trapezoid':
                img = self._trapezoid_trans(img, config.getTrapezoidFactor())
            elif action == 'parallelograms':
                img = self._parallelograms_trans(img, config.getParallelogramsFactor())
            elif action == 'zoom':
                img = self._zoom(config.getZoomScale())
            elif action == 'gray':
                img = self._gray(img)
            elif action == 'blackwhite':
                img = self._blackwhite(img, config.getBlackwhiteThresh())
            elif action == 'select':
                img = self._select(image, config.getSelRect())
        
        #将img另存
        (filepath,tempfilename) = os.path.split(picPath)
        (filename,extension) = os.path.splitext(tempfilename)
        
        filename='_'+str(datetime.datetime.now()).replace(":","")+'_'+filename
        newFullPath=os.path.join(filepath, filename+extension)
        
        cv2.imwrite(newFullPath, img)
        
