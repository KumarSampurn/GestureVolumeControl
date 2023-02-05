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
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(0.0, None)
minVol=volRange[0]
maxVol=volRange[1]


while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)

    img=detector.findHands(img)
    lmList=detector.findPosition(img)
    if(len(lmList)):
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=((x1+x2)//2),((y1+y2)//2)
        
        cv2.circle(img,(x1,y1),12,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),12,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),12,(255,0,255),cv2.FILLED)
        
        length =math.hypot(x2-x1,y2-y1)
        # print(length)
        #HandRange 15-220
        #VolumeRange 65 -0
        vol=np.interp(length,[30,200],[minVol,maxVol])
        print((int)(vol+100))
        volume.SetMasterVolumeLevel(int(vol), None)
        
        if length<50:
            cv2.circle(img,(cx,cy),12,(0,255,0),cv2.FILLED)


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,"FPS : "+str((int)(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break