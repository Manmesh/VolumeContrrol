import cv2
import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam =640,480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.handDetector(detectionCon = 0.9)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]
VolBar = 400

while True:
    ret,frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame,draw=False)

    if len(lmList) != 0:
        #print(lmList[4],lmList[8])

        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(frame,(x1,y1),3,(255,0,0),-1)
        cv2.circle(frame,(x2,y2),3,(255,0,0),-1)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),1)
        cv2.circle(frame,(cx,cy),3,(255,0,0),-1)
        length = math.hypot(x2-x1,y2-y1)

        #print(length)
        if length<20:
            cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

        # hand Range(20-170)
        # vol Range(-65 - 0)

        vol = np.interp(length,[20,175],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        VolBar = np.interp(length,[20,175],[400,150])
        cv2.rectangle(frame,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(frame,(50,int(VolBar)),(85,400),(0,255,0),-1)


    cTime = time.time()
    fps=1/(cTime-pTime)
    pTime = cTime

    cv2.putText(frame,f'FPS: {int(fps)}',(30,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),1)


    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break