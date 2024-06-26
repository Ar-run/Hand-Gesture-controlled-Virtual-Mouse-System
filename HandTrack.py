import cv2
import mediapipe as mp
from math import sqrt

class HandDetector:
    def __init__(self, mode=False, maxHands=2, modelComplexity=1,detectionConf=0.5, trackConf=0.5):
        self.mode=mode 
        self.maxHands=maxHands
        self.modelComplexity=modelComplexity
        self.detectionConf=detectionConf
        self.trackConf=trackConf 

        self.mpHands=mp.solutions.hands 
        self.hands=self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionConf, self.trackConf) 
        self.mpDraw=mp.solutions.drawing_utils 
        self.tipIds=[4, 8, 12, 16, 20]
    
    def getHands(self, img, draw=True):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        self.results=self.hands.process(imgRGB) 
        
        if self.results.multi_hand_landmarks: 
            for hand in self.results.multi_hand_landmarks: 
                if draw:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS) 
        return img
  
    def getPos(self, img, handNum=0, draw=True):
        lmList=[] 
        x_max=0
        y_max=0
        x_min=0
        y_min=0

        if self.results.multi_hand_landmarks: 
            myHand=self.results.multi_hand_landmarks[handNum]
            
            h,w,c=img.shape
            x_max=0
            y_max=0
            x_min=w
            y_min=h

            for id, lm in enumerate(myHand.landmark):
                cx,cy=int(lm.x*w), int(lm.y*h) 
                if cx > x_max:
                    x_max=cx
                if cx < x_min:
                    x_min=cx
                if cy > y_max:
                    y_max=cy
                if cy < y_min:
                    y_min=cy

                lmList.append([id,cx,cy]) 
                if draw: 
                    cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)  
            cv2.rectangle(img,(x_min-20, y_min-20),(x_max+20, y_max+20), (0,255,0),2)

        self.lmList=lmList
        return lmList,[x_min-20,y_min-20,x_max+20,y_max+20]

    def fingersUp(self):
        fingers=[]
        # Thumb
        if len(self.lmList)!=0:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # Fingers
            for id in range (1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers
    
    def findDistance(self, p1, p2, img):
        length=sqrt((self.lmList[p1][1]-self.lmList[p2][1])**2 + (self.lmList[p1][2]-self.lmList[p2][2])**2)
        img=cv2.line(img, (self.lmList[p1][1], self.lmList[p1][2]), (self.lmList[p2][1], self.lmList[p2][2]), (0,0,255),2)
        return length, img
