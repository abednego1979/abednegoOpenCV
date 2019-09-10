# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01


import pygame.font
from settings import Settings
import config


class Button():
    def __init__(self, pos, msg, visible=True): #msg为要在按钮中显示的文本, pos是按钮位置,形式为（x,y）,x是第几行，y是第几列
        """初始化按钮的属性"""
        self.global_settings=Settings()

        self.width,self.height=self.global_settings.BUTTON_WIDTH, self.global_settings.BUTTON_HEIGHT
        self.button_color=self.global_settings.BUTTON_BG_COLOR  #设置按钮的rect对象颜色为深蓝
        self.text_color=self.global_settings.BUTTON_TEXT_COLOR  #设置文本的颜色为白色
        self.font=pygame.font.SysFont(None,32)     #设置文本为默认字体，字号为40

        self.rect=self.global_settings.getButtonRect(pos)
        self.showText=msg
        self.visible=visible

        self.deal_msg(msg)  #渲染图像

    def deal_msg(self,msg):       
        """将msg渲染为图像，并将其在按钮上居中"""
        self.msg_img=self.font.render(msg,True,self.text_color,self.button_color) #render将存储在msg的文本转换为图像
        self.msg_img_rect=self.msg_img.get_rect()  #根据文本图像创建一个rect
        self.msg_img_rect.center=self.rect.center  #将该rect的center属性设置为按钮的center属性
        
    def set_msg(self, msg):
        self.showText=msg
        self.deal_msg(msg)  #渲染图像

    def draw(self, screen):
        if self.visible:
            screen.fill(self.button_color,self.rect)  #填充颜色
            screen.blit(self.msg_img,self.msg_img_rect) #将该图像绘制到屏幕
            
    def setVisible(self, visible):
        self.visible = visible
        
    def getButtonText(self):
        return self.showText
        
    def checkClick(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x,mouse_y) and self.visible:
            return True
        return False


