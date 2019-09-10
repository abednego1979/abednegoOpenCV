# -*- coding: utf-8 -*-
#Python 3.6.x
#V0.01

import config

import sys      
import wx
import cv2
import pygame
from settings import Settings
from picture import Picture
from controler import Controler
from button import Button


#显示对话框并选中一个文件
#是文件类型的匹配表达式，比如"*.txt"
#返回值为选中文件的路径
def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path



#procType:按下按钮的id
#curFunc:当前选择的功能状态
#FuncDisplayBitMap:当前按钮按下以后，功能区的
#FuncText
#LButtonText
#RButtonText
def ButtonProcEntry(buttonItem, pic):
    handle = buttonItem['handle']
    ProcType = buttonItem['ProcType']
    
    print ("Run ButtonProcEntry: %s" % ProcType)
    
    if ProcType == 'gray':
        pic.gray()
    if ProcType == 'blackwhite':
        pic.blackwhite(config.getBlackwhiteThresh())
    if ProcType == 'select':
        pass
    if ProcType == 'grid':
        #点击按钮会在显示和隐藏网格之间切换
        state=config.getGridOnFlag()
        state = False if state else True
        config.setGridOnFlag(state)
    if ProcType == 'undo':
        pic.undo()
    
    if ProcType == 'batch':
        pic.batch()
        
    
    return



def run_proc():
    pygame.init()
    
    global_settings=Settings()  #实例化

    # 创建游戏主窗口
    screen = pygame.display.set_mode((global_settings.SCREEN_WIDTH, global_settings.SCREEN_HEIGHT))  # 元组参数表示窗口大小,默认全屏024
    pygame.display.set_caption("My Picture Tool")
    
    SCREEN_RECT = screen.get_rect()
    pygame.display.update()


    #创建按钮
    buttonArray=[]
    #按钮的元素：
    #'handle'按钮句柄, 
    #Field:所属区域
    #'ProcType'执行动作类型, 
    buttonArray.append({'handle':Button((0,0),"ROT", visible=True), 'ProcType':'rotate'})
    buttonArray.append({'handle':Button((0,1),"TRAP", visible=True), 'ProcType':'trapezoid'})
    buttonArray.append({'handle':Button((0,2),"PARA", visible=True), 'ProcType':'parallelograms'})
    buttonArray.append({'handle':Button((1,0),"ZOOM", visible=True), 'ProcType':'zoom'})
    buttonArray.append({'handle':Button((1,1),"GRAY", visible=True), 'ProcType':'gray'})
    buttonArray.append({'handle':Button((1,2),"B/W", visible=True), 'ProcType':'blackwhite'})
    buttonArray.append({'handle':Button((2,0),"SEL", visible=True), 'ProcType':'select'})
    buttonArray.append({'handle':Button((2,1),"GRID", visible=True), 'ProcType':'grid'})
    buttonArray.append({'handle':Button((2,2),"BATCH", visible=True), 'ProcType':'batch'})
    buttonArray.append({'handle':Button((4,0),"UNDO", visible=True), 'ProcType':'undo'})
        
    #当前选中的功能按钮
    config.setCurProcType("None")

    #创建图像
    imgFile=get_path("*.*")
    if not imgFile:
        return
    image = cv2.imread(imgFile, cv2.IMREAD_UNCHANGED)
    pic = Picture(image)
    
    (filepath,tempfilename) = os.path.split(imgFile)
    (filename,extension) = os.path.splitext(tempfilename)
    config.setPicFilePathAndExt(filepath, filename, extension)    

    #创建控制器
    ctrl = Controler()

    while True:
        screen.fill(global_settings.BG_COLOR)  #调用属性设置屏幕的填充颜色
        #绘制各个按钮
        for item in buttonArray:
            item['handle'].draw(screen)
        
        #事件处理循环
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y=pygame.mouse.get_pos()

                #检查是否点击了某个按钮
                for item in buttonArray:
                    tempButtonHandle=item['handle']
                    if tempButtonHandle.checkClick(mouse_x, mouse_y):
                        print (tempButtonHandle.getButtonText(), 'click')
                        #call entry
                        ButtonProcEntry(item, pic)
                        config.setCurProcType(item['ProcType'])
            elif event.type == pygame.KEYUP:
                if config.getCurProcType():
                    ctrl.KeyUpProcEntry(config.getCurProcType(), event.key, event.mod, pic)
                pass 
                        
        #绘制图形
        if pic.isNeedUpdate:
            img = pic.show(global_settings.getImageRect())
            screen.blit(img, (global_settings.DRAWING_LEFT, global_settings.DRAWING_TOP), img.get_rect())
            #pic.isNeedUpdate=False

        pygame.display.flip()   #使最近绘制的屏幕可见
    
    pygame.quit()


run_proc()