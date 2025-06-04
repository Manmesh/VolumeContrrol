import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self,vid,draw=True):
        vid = cv2.flipND(vid, 1)
        vidRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(vidRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(vid, handLms, self.mpHands.HAND_CONNECTIONS)
        return vid

    def findPosition(self,vid,handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm, in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = vid.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,cx,cy)
                # if id == 4:
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(vid, (cx, cy), 3, (255, 0, 255), -1)

        return lmList

def main():
    pTime =0
    cTime =0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, vid = cap.read()
        vid = detector.findHands(vid)
        lmList = detector.findPosition(vid)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(vid, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("video", vid)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()