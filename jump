import time
import math
from PIL import Image
import os
import cv2
import matplotlib.pyplot as plt
import random

#对手机屏幕每5s截一次图，以png格式保存在本地 输入保存路径
def Screenshot_save(path):
    time.sleep(5)
    os.system('adb shell screencap -p /sdcard/wechat_jump_screenshot.png')      #截图
    os.system('adb pull /sdcard/wechat_jump_screenshot.png '+path)                #保存

#对图片进行预处理 输入png格式图片路径 输出分辨率为1080*1920的二值化图片数组
def Pic_pretreat(path):
    img=cv2.imread(path)                      #读取图片
    img=cv2.Canny(img,50,200)                   #边缘检测
    return img

#找小人脑袋的中心 输入二值化图片数组 输出圆心横坐标
def Find_head(img):
    center_x=0
    circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,100,None,100,80,20,40)  #霍夫变换找圆
    circles=circles[0,:,:]               #数组处理，三维变二维
    for x,y,r in circles:
        if y>750 and y<1250:            #排除其他圆的干扰，筛选小人脑袋所在的圆
            center_x=x
    return center_x                     #返回圆心横坐标

#找下个跳台  输入二值化图片数组 输出跳台中心横坐标 （同一水平的两边缘点的中点横坐标等于跳台中心横坐标）
def Find_stage(img):
    flag=0                                        #创建循环跳出标识
    left=0
    right=0
    for i in range(500,len(img),5):               #从第500行开始每5行扫描一行
        for j in range(0,int(len(img[0])/2)):     #对该行的像素从左端点到中点进行扫描
            if img[i][j]!=0:                      #判断像素点的值是否为0
                #flag=1                            #跳出循环标志
                left=j                            #提取第一处值不为0的像素点的横坐标
                break
        for j in range(j+2,len(img[0])):          #越过第一处非0值像素点
            if img[i][j]!=0:
                right=j                            #提取第二处值不为0的像素点的横坐标
                break                             #结束列扫描
        if right-left>50:
            break                                 #跳出行扫描
    center_x=(left+right)/2+1
    return center_x                               #返回中心横坐标

#计算跳跃距离并转化为时间 输入两个横坐标和距离时间系数 输出按压时间（毫秒）
def Press_time(x1,x2,time_coefficient,time_constant):
    t=abs(x1-x2)*time_coefficient+time_constant                   #距离与按压时间成线性关系
    return int(t)

#将按压时间传递给手机 输入按压时间（540,1584）为再来一局的位置，这里用（750,1000）附近作为按压点
def Press(press_time):
    r=100
    os.system('adb shell input swipe {x1} {y1} {x1} {y1} {press_time}'.format(
        x1=random.randrange(750-r,750+r),
        y1=random.randrange(1000-r,1000+r),
        press_time=max(press_time,200)
    ))

def main():
        path='./wechat_jump_screenshot.png'             #设置本地保存路径
        time_coefficient=1.50                               #设置距离时间系数
        time_constant=50                                    #设置时间常数
        Screenshot_save(path)                               #截图保存
        img=Pic_pretreat(path)                              #图片预处理
        x1=Find_head(img)                                   #找小人脑袋
        if x1<len(img[0])/2:                                #判断小人在中轴线左边还是右边，在左边就翻转图片
            img=cv2.flip(img,1)
            x2=1080-Find_stage(img)
        else:
            x2=Find_stage(img)                              #找下个跳台
        print(x1,x2)
        press_time=Press_time(x1,x2,time_coefficient,time_constant)       #计算按压时间
        Press(press_time)                                   #给手机传递按压时间

while(True):
    main()
