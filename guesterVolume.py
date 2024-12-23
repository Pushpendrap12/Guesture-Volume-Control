import cv2
import mediapipe as mp
import  time
import numpy as np
import math
from numpy.ma.core import minimum_fill_value
from scipy.special import y1_zeros
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import handtrackingmodule as htm

##############################
wCam , hCam = 640,480
#############################
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar =0
volpar =0;
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    if len(lmlist)!=0:
        print(lmlist[4])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        # print(vol)
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volpar = np.interp(length, [50, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        # print(length)

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

        #Hand range 50-300
        #volmeRang -65 0
        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
        cv2.putText(img,f'{int(volpar)}%',(40,450),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS:{int(fps)}',(40,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
    cv2.imshow("image",img)
    cv2.waitKey(1)
