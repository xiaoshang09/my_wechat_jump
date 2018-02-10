import cv2
import numpy as np
#import matplotlib.pyplot as plt

img = cv2.imread('D:\openCV\OCR\\6.jpg')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

class MyLine:
    def __init__(self,x1,y1,x2,y2):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.l=np.sqrt(np.square(self.x1-self.x2)+np.square(self.y1-self.y2))
        self.k=(self.y1-self.y2)/(self.x1-self.x2)
    def show(self):
        print('k=%-5.2f  l=%d'%(self.k,self.l))

class Myline2:
    def __init__(self,ID,k,l):
        self.ID=ID
        self.k=k
        self.l=l
    def show(self):
        print('ID=%d  k=%5.2f  l=%d'%(self.ID,self.k,self.l))

def exchange(k):
    if k<=0:
        a=np.arctan(-k)/np.pi*180
        b=90-a
    else:
        a=np.arctan(k)/np.pi*180
        b=a+90
    return b

cv2.imshow('a',img)
edges = cv2.Canny(img,50,200)
cv2.imshow('edges',edges)

lines = cv2.HoughLines(edges,1,np.pi/180,150)
line=cv2.HoughLinesP(edges,1,np.pi/180,20,20,100)
lines1=lines[:,0,:]
lines2=line[:,0,:]
circles=cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,20,None,50,30,200,300)
circles1=circles[0,:,:]
for rho,theta in lines1:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 500*(-b))
    y1 = int(y0 + 500*(a))
    x2 = int(x0 - 500*(-b))
    y2 = int(y0 - 500*(a))
    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
for x1,y1,x2,y2 in lines2:
    cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
circles1x=circles1[:,0]
circles1y=circles1[:,1]
circles1r=circles1[:,2]
x0=int(sum(circles1x)/len(circles1x))
y0=int(sum(circles1y)/len(circles1y))
r0=int(max(circles1r)*2)-int(sum(circles1r)/len(circles1r))
r1=int(sum(circles1r)/len(circles1r))
cv2.circle(img,(x0,y0),r0,(0,0,255),1)
cv2.circle(img,(x0,y0),10,(0,255,255),-1)
cv2.circle(img,(x0,y0),r1,(0,0,255),1)

for i in range(0,len(lines2)):
    l1=MyLine(lines2[i][0],lines2[i][1],lines2[i][2],lines2[i][3])
    print('ID=%d'%(i),end='  ')
    l1.show()
print()
pass
for i in range(0,len(lines2)):
    l1=MyLine(lines2[i][0],lines2[i][1],lines2[i][2],lines2[i][3])
    l2=Myline2(i,round(l1.k,2),int(l1.l))
    l2.show()
print()
olines=[[0]*3 for i in range(len(lines2))]
for i in range(0,len(lines2)):
    l1=MyLine(lines2[i][0],lines2[i][1],lines2[i][2],lines2[i][3])
    l2=Myline2(i,float('%.2f'%l1.k),int(l1.l))
    olines[i][0]=l2.ID
    olines[i][1]=l2.k
    olines[i][2]=l2.l
print(olines)
arrayID=[m[0] for m in olines]
arrayk  =[m[1] for m in olines]
arrayl=[m[2] for m in olines]
for i in range(0,len(lines2)):
    if arrayl[i]==max(arrayl):
        IDsecond=arrayID[i]
        ksecond=arrayk[i]
    if arrayl[i]==min(arrayl):
        IDhour=arrayID[i]
        khour=arrayk[i]
for i in range(0,len(lines2)):
    if not((abs(arrayk[i])<abs(khour)*1.1 and abs(arrayk[i])>abs(khour)*0.9)):
        if not ((abs(arrayk[i])<abs(ksecond)*1.1 and abs(arrayk[i])>abs(ksecond)*0.9)):
            kminiter=arrayk[i]
            IDminiter=arrayID[i]
print()
print('hour:{}\nminiter:{}\nsecond:{}'.format(khour,kminiter,ksecond))
hour=exchange(khour)
miniter=exchange(kminiter)
second=exchange(ksecond)

print(x0,y0)
print(lines2)
print(IDhour,IDminiter,IDsecond)

if (lines2[IDhour][0]+lines2[IDhour][2])/2<x0:
    hour+=180
if (lines2[IDminiter][0]+lines2[IDminiter][2])/2<x0:
    miniter+=180
if (lines2[IDsecond][0]+lines2[IDsecond][2])/2<x0:
    second+=180
print(hour,miniter,second)
Hour=int(hour//30)
Miniter=int(miniter//6)
Second=int(second//6)
print()
print('The time now is {}:{}:{}'.format(Hour,Miniter,Second))

cv2.imshow('image',img)
cv2.waitKey(0)
