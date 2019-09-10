# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

import pygame


class Settings():
    def __init__(self):
        #屏幕区域
        DisplayScale_W=1.6
        DisplayScale_H=1.2
        
        self.SCREEN_WIDTH = int(1024*DisplayScale_W)
        self.SCREEN_HEIGHT = int(768*DisplayScale_H)
        #绘图区域
        self.DRAWING_LEFT = 0
        self.DRAWING_RIGHT = int(self.SCREEN_WIDTH*0.75)
        self.DRAWING_TOP = 0
        self.DRAWING_BOTTOM = self.SCREEN_HEIGHT
        #控制按钮区
        self.CONTROL_AREA_LEFT = self.DRAWING_RIGHT
        self.CONTROL_AREA_RIGHT = self.SCREEN_WIDTH
        self.CONTROL_AREA_TOP = 0
        self.CONTROL_AREA_BOTTOM = self.SCREEN_HEIGHT
        
        #按钮大小
        self.BUTTON_WIDTH, self.BUTTON_HEIGHT = 75, 50
        self.BUTTON_SPACE = 8   #按钮之间的间隔
        self.BUTTON_BG_COLOR = (72,61,139)   #按钮颜色
        self.BUTTON_TEXT_COLOR = (255,255,255)   #按钮文本颜色
        
        #背景颜色
        self.BG_COLOR=(230,230,230)
        
        #为了实现undo功能，最多缓存几个历史图片
        #self.MAX_PIC_BUF_LEN=10
        
    def getElementRect(self, pos):
        y,x=pos
        
        x=self.BUTTON_SPACE+(self.BUTTON_WIDTH+self.BUTTON_SPACE)*x     #按钮左上角x
        y=self.BUTTON_SPACE+(self.BUTTON_HEIGHT+self.BUTTON_SPACE)*y    #按钮左上角y
        
        x+=self.CONTROL_AREA_LEFT
        y+=self.CONTROL_AREA_TOP
        
        return pygame.Rect((x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        
    def getButtonRect(self, pos):
        return self.getElementRect(pos)

    def getTextRect(self, pos):
        return self.getElementRect(pos)
    
    def getEditerRect(self, pos):
        return self.getElementRect(pos)
    
    def getImageRect(self):
        return pygame.Rect((self.DRAWING_LEFT, self.DRAWING_TOP, self.DRAWING_RIGHT-self.DRAWING_LEFT, self.DRAWING_BOTTOM-self.DRAWING_TOP))
        