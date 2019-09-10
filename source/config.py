# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

import json


class global_var:
    grid_on=True           #网格线
    grid_pos=[10, 10]      #网格线基准位置
    grid_internal=200
    grid_step=100          #网格线间隔
    grid_opObj='Pos'       #'Pos'/'Internal'
    
    #旋转相关参数
    rotate_angle = 0.0
    rotate_step = 0.01       #0.01/0.1/1.0
    
    #梯形变换相关参数
    trapezoid_factor = 0.0
    trapezoid_step = 0.01       #0.01/0.1
    
    #平行四边形变换相关参数
    parallelograms_factor = 0.0
    parallelograms_step = 0.01       #0.01/0.1
    
    #缩放相关参数
    zoom_scale = 1.0
    zoom_scale_step = 0.01      #0.01/0.1
    
    #设置灰度标识
    gray = False
    
    #设置黑白图标识
    blackwhite = False
    blackwhite_thresh=127           #黑白色阈值
    
    #选定区域的相关参数
    select_rect=[10,10, 100, 100]       #分别是left，top， right，bottom
    select_opObj='LeftTop'      #标记操作的是左上角还是右下角
    select_step=10      #1/10/100
    
    curProcType='None'#当前操作对象
    
    #图片文件类型
    picFilePath=""
    picFileName=""
    picFileExt='.*'
    
    
def getCurProcType():
    return global_var.curProcType

def setCurProcType(Type):
    global_var.curProcType=Type

    
def getGridOnFlag():
    return global_var.grid_on
def setGridOnFlag(Flag):
    global_var.grid_on = Flag
    
def getGridPos():
    return global_var.grid_pos
def setGridPos(Pos):
    global_var.grid_pos = Pos
    
def getGridInternal():
    return global_var.grid_internal
def setGridInternal(Internal):
    global_var.grid_internal = Internal
    
def getGridStep():
    return global_var.grid_step
def setGridStep(Step):
    global_var.grid_step = Step
    
def getGridOpObj():
    return global_var.grid_opObj
def setGridOpObj(Obj):
    global_var.grid_opObj = Obj    
    
def getRotateAngle():
    return global_var.rotate_angle
def setRotateAngle(Angle):
    global_var.rotate_angle=Angle
    
def getRotateStep():
    return global_var.rotate_step
def setRotateStep(Step):
    global_var.rotate_step=Step

def getTrapezoidFactor():
    return global_var.trapezoid_factor
def setTrapezoidFactor(Factor):
    global_var.trapezoid_factor = Factor
    
def getTrapezoidFactorStep():
    return global_var.trapezoid_step
def setTrapezoidFactorStep(Step):
    global_var.trapezoid_step = Step
    
def getParallelogramsFactor():
    return global_var.parallelograms_factor
def setParallelogramsFactor(Factor):
    global_var.parallelograms_factor = Factor
    
def getParallelogramsFactorStep():
    return global_var.parallelograms_step
def setParallelogramsFactorStep(Step):
    global_var.parallelograms_step = Step
    
def getZoomScale():
    return global_var.zoom_scale
def setZoomScale(scale):
    global_var.zoom_scale = scale
    
def getZoomScaleStep():
    return global_var.zoom_scale_step
def setZoomScaleStep(step):
    global_var.zoom_scale_step = step
    
def getGrayFlag():
    return global_var.gray

def setGrayFlag(Flag):
    global_var.gray = Flag
    
def getBlackwhiteFlag():
    return global_var.blackwhite

def setBlackwhiteFlag(Flag):
    global_var.blackwhite = Flag
    
    
def getSelRect():
    return global_var.select_rect
def setSelRect(rect):
    global_var.select_rect=rect
    
def getSelOpObj():
    return global_var.select_opObj
def setSelOpObj(Obj):
    assert Obj=='LeftTop' or Obj=='RightBottom'
    global_var.select_opObj=Obj
    
def getSelStep():
    return global_var.select_step
def setSelStep(Step):
    global_var.select_step=Step
    
def getBlackwhiteThresh():
    return global_var.blackwhite_thresh
def setBlackwhiteThresh(thresh):
    global_var.blackwhite_thresh=thresh

def getPicFilePathAndExt():
    return global_var.picFilePath, global_var.picFileName, global_var.picFileExt
def setPicFilePathAndExt(picFilePath, picFileName, picFileExt):
    global_var.picFilePath=picFilePath
    global_var.picFileName=picFileName
    global_var.picFileExt=picFileExt


def getFormatParams():
    infoLines=[]
    
    tempLine="<Angle:%.2f, Step:%.2f><Trapezoid: Factor:%.2f, Step:%.2f>" % (global_var.rotate_angle, 
                                                                             global_var.rotate_step,
                                                                             global_var.trapezoid_factor,
                                                                             global_var.trapezoid_step)
    infoLines.append(tempLine)
    
    tempLine='<Paral: Factor:%.2f, Step:%.2f>' % (global_var.parallelograms_factor, global_var.parallelograms_step)
   
    tempLine='<Zoom:Scale:%.2f, Step:%.2f>\t<Gray:%s>\t<B/W:%s>' % (global_var.zoom_scale, global_var.zoom_scale_step, "On" if global_var.gray else 'Off', "On" if global_var.blackwhite else 'Off')
    infoLines.append(tempLine)
    
    tempLine='<Select:Rect:%s, OpObj:%s, Step:%d>' % (json.dumps(global_var.select_rect), global_var.select_opObj, global_var.select_step)
    infoLines.append(tempLine)

    tempLine='<Grid:Pos:%s, Internal:%d, Step:%d, OpObj:%s>' % (json.dumps(global_var.grid_pos), global_var.grid_internal, global_var.grid_step, "Pos" if global_var.grid_opObj=='Pos' else 'Internal')
    infoLines.append(tempLine)
    
    tempLine='<CurProcType:%s>' % (global_var.curProcType)
    infoLines.append(tempLine)
    
    return infoLines
  
