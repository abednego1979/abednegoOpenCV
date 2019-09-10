# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

import config
import pygame
import pygame.font
from settings import Settings




class Controler():
    def __init__(self):
        self.global_settings=Settings()
        
    def KeyUpProcEntry(self, ProcType, key, mod, pic):

        print ("Key:", key)
        print ("mod:", mod)

        if ProcType == 'rotate':
            if key == pygame.K_LEFT:
                #逆时针旋转图像
                self.ProcRotate(1, pic)
            elif key == pygame.K_RIGHT:
                #顺时针旋转图像
                self.ProcRotate(-1, pic)
            elif key == pygame.K_s:
                #设定步长
                self.ProcRotateStep()
                
        elif ProcType == 'trapezoid':
            if key == pygame.K_LEFT:
                #
                self.ProcTrapezoid(-1, pic)
            elif key == pygame.K_RIGHT:
                #
                self.ProcTrapezoid(1, pic)
            elif key == pygame.K_s:
                #设定因子
                self.ProcTrapezoidStep()
                
        elif ProcType == 'parallelograms':
            if key == pygame.K_LEFT:
                #
                self.ProcParallelograms(-1, pic)
            elif key == pygame.K_RIGHT:
                #
                self.ProcParallelograms(1, pic)            
            elif key == pygame.K_s:
                #设定因子
                self.ProcParallelogramsStep()
                
        elif ProcType == 'zoom':
            if key == pygame.K_s:
                self.ProcZoomStep()
            elif key == pygame.K_LEFT:
                self.ProcZoom(-1, pic)
            elif key == pygame.K_RIGHT:
                self.ProcZoom(1, pic)
            
        elif ProcType == 'grid':
            if key == pygame.K_s:
                self.ProcGridStep()
            elif key == pygame.K_m:
                #在处理pos和网格间隔功能之间切换
                config.setGridOpObj('Pos' if config.getGridOpObj() == 'Internal' else 'Internal')
            elif key == pygame.K_LEFT:
                if config.getGridOpObj() == 'Pos':
                    pos=config.getGridPos()
                    config.setGridPos((max(pos[0]-10, 0), pos[1]))
                else:
                    internal=config.getGridInternal()
                    step=config.getGridStep()
                    internal-=step
                    internal=max(internal, 10)
                    config.setGridInternal(internal)
            elif key == pygame.K_RIGHT:
                if config.getGridOpObj() == 'Pos':
                    pos=config.getGridPos()
                    config.setGridPos((min(pos[0]+10, 1000), pos[1]))
                else:
                    internal=config.getGridInternal()
                    step=config.getGridStep()
                    internal+=step
                    internal=min(internal, 1000)
                    config.setGridInternal(internal)                    
            elif key == pygame.K_UP:
                if config.getGridOpObj() == 'Pos':
                    pos=config.getGridPos()
                    config.setGridPos((pos[0], max(pos[1]-10, 0)))
            elif key == pygame.K_DOWN:
                if config.getGridOpObj() == 'Pos':
                    pos=config.getGridPos()
                    config.setGridPos((pos[0], min(pos[1]+10, 1000)))
                
        elif ProcType == 'select':
            rect=config.getSelRect()
            step=config.getSelStep()
            
            if key == pygame.K_s:
                self.ProcSelectStep()
            elif key == pygame.K_m:
                #按M在操作对象之间切换
                config.setSelOpObj('LeftTop' if config.getSelOpObj() == 'RightBottom' else 'RightBottom')            
            elif key == pygame.K_LEFT:
                if config.getSelOpObj() == 'LeftTop':
                    config.setSelRect([rect[0]-step, rect[1], rect[2]-step, rect[3]])
                else:
                    config.setSelRect([rect[0], rect[1], rect[2]-step, rect[3]])
            elif key == pygame.K_RIGHT:
                if config.getSelOpObj() == 'LeftTop':
                    config.setSelRect([rect[0]+step, rect[1], rect[2]+step, rect[3]])
                else:
                    config.setSelRect([rect[0], rect[1], rect[2]+step, rect[3]]) 
            elif key == pygame.K_UP:
                if config.getSelOpObj() == 'LeftTop':
                    config.setSelRect([rect[0], rect[1]-step, rect[2], rect[3]-step])
                else:
                    config.setSelRect([rect[0], rect[1], rect[2], rect[3]-step])
            elif key == pygame.K_DOWN:
                if config.getSelOpObj() == 'LeftTop':
                    config.setSelRect([rect[0], rect[1]+step, rect[2], rect[3]+step])
                else:
                    config.setSelRect([rect[0], rect[1], rect[2], rect[3]+step])
        elif ProcType == 'blackwhite':
            if key == pygame.K_LEFT:
                #减少黑白门限阈值
                self.ProcBlackwhite(-1, pic)
            elif key == pygame.K_RIGHT:
                #增加黑白门限阈值
                self.ProcBlackwhite(1, pic)                        
            
        else:
            pass
        return    
        
    def ProcRotate(self, num, pic):
        angle = config.getRotateAngle()
        step = config.getRotateStep()
        angle += num*step
        pic.rotate(angle)
        
    def ProcRotateStep(self):
        step=config.getRotateStep()
        step=float(10*step)
        if step==10.0:
            step=0.01
        config.setRotateStep(step)
    
    def ProcTrapezoid(self, num, pic):
        factor = config.getTrapezoidFactor()
        step = config.getTrapezoidFactorStep()
        factor += num*step
        pic.trapezoid_trans(factor)
        
    def ProcTrapezoidStep(self):
        step=config.getTrapezoidFactorStep()
        step=float(10*step)
        if step==1.0:
            step=0.01
        config.setTrapezoidFactorStep(step)
        
    def ProcParallelograms(self, num, pic):
        factor = config.getParallelogramsFactor()
        step = config.getParallelogramsFactorStep()
        factor += num*step
        pic.parallelograms_trans(factor)
        
    def ProcParallelogramsStep(self):
        step=config.getParallelogramsFactorStep()
        step=float(10*step)
        if step==1.0:
            step=0.01
        config.setParallelogramsFactorStep(step)        
        
    def ProcZoom(self, num, pic):
        scale = config.getZoomScale()
        step = config.getZoomScaleStep()
        scale += num*step
        pic.zoom(scale)
        
    def ProcZoomStep(self):
        step=config.getZoomScaleStep()
        step=float(10*step)
        if step==1.0:
            step=0.01
        config.setZoomScaleStep(step)
        
    
    def ProcGridStep(self):
        step=config.getGridStep()
        step=int(10*step)
        if step==1000:
            step=1
        config.setGridStep(step)   
    
    
    def ProcSelectStep(self):
        step=config.getSelStep()
        step=int(10*step)
        if step==1000:
            step=1
        config.setSelStep(step)
        
    def ProcBlackwhite(self, num, pic):
        thresh=config.getBlackwhiteThresh()
        thresh += num
        pic.blackwhite(thresh)
        
        
    
        
    
        
