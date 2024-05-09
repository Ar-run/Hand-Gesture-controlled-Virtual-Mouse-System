import cv2
import numpy as np
from HandTrack import HandDetector
import pyautogui as autopy

wCam, hCam=640, 480
frameR=100 
smoothening=5
plocx,plocy=0,0
clocx,clocy=0,0

cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector=HandDetector(maxHands=1)
wScr,hScr=autopy.size()

while True:
    success, img = cap.read()
    img=cv2.flip(img, 1) 
    img=detector.getHands(img)
    lmlist,bbox=detector.getPos(img, draw=False)
   
    if len(lmlist) != 0:
        x1,y1=lmlist[8][1:] 
        x2,y2=lmlist[12][1:]
        
        fingers=detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)

        if fingers[1]==1 and fingers[2]==0:
            x3=np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3=np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocx=plocx+(x3-plocx)/smoothening
            clocy=plocy+(y3-plocy)/smoothening

            autopy.moveTo(clocx, clocy)
            plocx,plocy=clocx, clocy

        if fingers[1]==1 and fingers[2]==1:
            length,img=detector.findDistance(8,12,img)
            if length<35:
                cv2.circle(img,(x1, y1),4,(0,255,0),cv2.FILLED)
                cv2.circle(img,(x2, y2),4,(0,255,0),cv2.FILLED)
                autopy.click()

    cv2.imshow("Image",img)
    cv2.waitKey(1)
