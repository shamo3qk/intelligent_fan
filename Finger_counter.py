import cv2
import os
import hand_tracking_module as htm
# import RPi.GPIO as GPIO
import time

# Relay_Ch1 = 26
# Relay_Ch2 = 20
# Relay_Ch3 = 21
#
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
#
# GPIO.setup(Relay_Ch1,GPIO.OUT)
# GPIO.setup(Relay_Ch2,GPIO.OUT)
# GPIO.setup(Relay_Ch3,GPIO.OUT)

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


path="finger"
myList=os.listdir(path)
myList.sort()
overlayList=[]

for impath in myList:
    image=cv2.imread(f'{path}/{impath}')
    overlayList.append(image)
pTime=0

detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if detector.results.multi_handedness:
        for idx, hand_handedness in enumerate(detector.results.multi_handedness):
            label = hand_handedness.classification[0].label
    #print(lmList)
    if len(lmList) !=0:
        fingers=[]

        # Thumb
        # if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        #     fingers.append(1)
        # else:
        #     fingers.append(0)
        if label == "Left" and lmList[4][1] > lmList[3][1]:
            fingers.append(1)
        elif label == "Right" and lmList[4][1] < lmList[3][1]:
            fingers.append(1)

        for id in range(1,5):  #y axis
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers=fingers.count(1)
        # print(totalFingers)


        # if totalFingers==0:
        #     GPIO.output(Relay_Ch1, GPIO.HIGH)
        #     GPIO.output(Relay_Ch2, GPIO.HIGH)
        #     GPIO.output(Relay_Ch3, GPIO.HIGH)
        # elif totalFingers==1:
        #     GPIO.output(Relay_Ch1, GPIO.LOW)
        #     GPIO.output(Relay_Ch2, GPIO.HIGH)
        #     GPIO.output(Relay_Ch3, GPIO.HIGH)
        # elif totalFingers==2:
        #     GPIO.output(Relay_Ch1, GPIO.HIGH)
        #     GPIO.output(Relay_Ch2, GPIO.LOW)
        #     GPIO.output(Relay_Ch3, GPIO.HIGH)
        # elif totalFingers == 3:
        #     GPIO.output(Relay_Ch1, GPIO.HIGH)
        #     GPIO.output(Relay_Ch2, GPIO.HIGH)
        #     GPIO.output(Relay_Ch3, GPIO.LOW)
        h,w,c=overlayList[totalFingers].shape
        img[0:h,0:w]=overlayList[totalFingers]

        cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    #cv2.imshow("Image",img)
    cv2.waitKey(1)

if __name__=="__main__":
    exec()