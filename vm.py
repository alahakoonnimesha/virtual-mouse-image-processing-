import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
mouse=Controller()

app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(capx,capy)=(320,240)


cap=cv2.VideoCapture(0)
cap.set(3,capx)
cap.set(4,capy)

#detect green
greenmin=np.array([33,80,40])
greenmax=np.array([102,255,255])

kernelopen=np.ones((5,5))
kernelclose=np.ones((20,20))

#previousmouse coord
mlocold=np.array([0,0])
dampingfactor=3
#after applyindamping
mouseloc=np.array([0,0])


pinchflag=0

openx,openy,openw,openh=(0,0,0,0)

while True:
        
    
    success,img = cap.read()
    img=cv2.flip(img,1)
    imghsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(imghsv,greenmin,greenmax)

    maskopen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelopen)
    maskc=cv2.morphologyEx(maskopen,cv2.MORPH_CLOSE,kernelclose)
    maskfinal=maskc
    _,conts,h=cv2.findContours(maskfinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #x,y:top left corner coordinates,w,h:width & height
    if(len(conts)==2):
        if(pinchflag==1):
            pinchflag=0
            mouse.release(Button.left)
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1=round(x1+w1/2)
        cy1=round(y1+h1/2)
        cx2=round(x2+w2/2)
        cy2=round(y2+h2/2)
        cx=round((cx1+cx2)/2)
        cy=round((cy1+cy2)/2)
        cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,0),2)
        cv2.circle(img,(cx,cy),3,(255,0,0),2)
        mouseloc=mlocold+((cx,cy)-mlocold)/dampingfactor
        #au.position=(mouseloc[0]*sx/capx,mouseloc[1]*sy/capy)
        mouse.position=(int(mouseloc[0]*sx/capx),int(mouseloc[1]*sy/capy))  
        while mouse.position!=(int(mouseloc[0]*sx/capx),int(mouseloc[1]*sy/capy)):
            pass
            
        mlocold=mouseloc

        #outerbound box takes as one box
        openx,openy,openw,openh=cv2.boundingRect(np.array([[[x1,y1],[x1+w1,y1+h1],[x2,y2],[x2+w2,y2+h2]]]))
        #cv2.rectangle(img,(openx,openy),(openx+openw,openy+openh),(255,0,0),2)

       
    elif(len(conts)==1):
        
        x,y,w,h=cv2.boundingRect(conts[0])
        if(pinchflag==0):
            if(abs((w*h-openw*openh)*100/(w*h))<30):
                pinchflag=1
                mouse.click(Button.left,2)
                 
                openx,openy,openw,openh=(0,0,0,0)
            
        else:
            
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cx=round(x+w/2)
            cy=round(y+h/2)
            cv2.circle(img,(cx,cy),round((w+h)/4),(0,0,255),2)
            mouseloc=mlocold+((cx,cy)-mlocold)/dampingfactor
            mouse.position=(int(mouseloc[0]*sx/capx),int(mouseloc[1]*sy/capy))
            while mouse.position!=(int(mouseloc[0]*sx/capx),int(mouseloc[1]*sy/capy)):
                pass
            mlocold=mouseloc
          
    #cv2.drawContours(img,conts,-1,(255,0,0),3)
    #cv2.drawContours(img, conts,-1,(0,0,255),3)

            
    #cv2.imshow('mask',mask)
    #cv2.imshow('mask1',imghsv)
    #cv2.imshow('maskopen',maskopen)
    #cv2.imshow('maskclose',maskfinal)
    
    
    cv2.imshow('cap',img)
    k=cv2.waitKey(5) & 0xff
    if k == 27:
        break
    


cap.release()
cv2.destroyAllWindows()
        
