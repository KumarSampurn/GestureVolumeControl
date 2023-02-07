import math
import time
from ctypes import POINTER, cast

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import handTrackingModule as htm

#####################################
wCam, hCam= 640 ,480
#####################################

cap= cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
 
pTime=0
cTime=0

detector=htm.handDetector(detectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]

vol=0
ymax=0
while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)

    img=detector.findHands(img,draw=False)
    lmList=detector.findPosition(img, draw=False)
    if(len(lmList)):
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=((x1+x2)//2),((y1+y2)//2)
        
        cv2.circle(img,(x1,y1),12,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),12,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),12,(255,0,255),cv2.FILLED)
        
        length =math.hypot(x2-x1,y2-y1)
       
        vol=np.interp(length,[50,200],[minVol,maxVol])
        
        volume.SetMasterVolumeLevel(int(vol), None)
        
        if length<50:
            cv2.circle(img,(cx,cy),12,(0,255,0),cv2.FILLED)
        cv2.rectangle(img,(40,260-int(vol)-100), (75,260),(0,255,0),-1)
    cv2.putText(img,str((int)(vol+100))+"%",(40,120),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)     
    cv2.rectangle(img,(40,160), (75,260),(0,255,0),2)
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,"FPS : "+str((int)(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break