import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success,vid = cap.read()
    vid= cv2.flipND(vid,1)
    vidRGB = cv2.cvtColor(vid,cv2.COLOR_BGR2RGB)
    results = hands.process(vidRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm, in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c = vid.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                if id ==4:
                    cv2.circle(vid,(cx,cy),10,(255,0,255),-1)
            mpDraw.draw_landmarks(vid,handLms, mpHands.HAND_CONNECTIONS)

    cTime =  time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(vid,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
    cv2.imshow("video",vid)
    if cv2.waitKey(4) & 0xFF == ord('q'):
        break