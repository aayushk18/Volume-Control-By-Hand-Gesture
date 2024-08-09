import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript


################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime=0
detector = htm.handDetector(detectionCon=0.7)
minVol =0
maxVol = 100

 
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)

    result = osascript.osascript('get volume settings')
    volInfo = result[1].split(',')
    outputVol = volInfo[0].replace('output volume:', '')
    

    if len(lmlist)!=0:
        #  print(lmlist[])
        

        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cx,cy = ((x1+x2)//2), ((y1+y2)//2)

        

        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
        cv2.line (img,(x1,y1),(x2,y2),(255),3)
        cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        vol = np.interp(length, [50 ,200] , [minVol , maxVol])
        print(vol)
        osascript.osascript("set volume output volume {}".format(vol))

        # print(length)

        if length<50:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
            osascript.osascript("set volume output volume {}".format(0))

        cv2.putText(img , f'VOL: {int(vol)}',(40,170),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)



    

 


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime= cTime 

    cv2.putText(img , f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)
    

    cv2.imshow("VOlume", img)
    cv2.waitKey(2)
    

