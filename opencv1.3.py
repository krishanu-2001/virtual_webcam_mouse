# import the necessary packages

from imutils.video import VideoStream
import imutils
import time
import numpy as np
import argparse
from collections import deque
import cv2
import pyautogui
import threading
pyautogui.PAUSE = 0.05


flag = 1

def posinside(x_,y_):
    cur = pyautogui.position()
    maxp = pyautogui.size()
    if( 10<=cur[0] + x_ <= maxp[0]-10  and 10<=cur[1] + y_ <= maxp[1]-10):
        return True
    else:
        return False

rain = argparse.ArgumentParser()
rain.add_argument("-v", "--video",
	help="path to the (optional) video file")
rain.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(rain.parse_args())
color_r1 = (30, 100, 20)
color_r2 = (60, 255, 240)
pts = deque(maxlen=args["buffer"])
if not args.get("video", False):
	cv = VideoStream(src=0).start()
else:
	cv = cv2.VideoCapture(args["video"])
time.sleep(1.0)
def f1():
    while True:
        frame = cv.read()
        frame = frame
        if args.get("video", False):
            frame = frame[1]
        else:
            frame = frame
        if frame is None:
            break
        frame = imutils.resize(frame, width=500)
        isblr = cv2.GaussianBlur(frame, (11, 11), 0)
        sauce = cv2.cvtColor(isblr, cv2.COLOR_BGR2HSV)
        #first things required for extracting information.
        mask = cv2.inRange(sauce, color_r1, color_r2)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        cnter = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnter = imutils.grab_contours(cnter)
        centroid = None
        if f3(cnter) >0:
            card = max(cnter, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(card)
            joe = cv2.moments(card)
            centroid = (int(joe["m10"] / joe["m00"]), int(joe["m01"] / joe["m00"]))

        if centroid != np.NaN:
            pts.appendleft(centroid)
    if not args.get("video", False):
        cv.stop()
    else:
        cv.release()
    cv2.destroyAllWindows()

def f2():
    while True:
        global flag

        pts1 = list(pts)

        #print(pts1)
        #print(pyautogui.position())
        if len(pts)>1:
            argx = (100,100)
            argy = (100,100)
            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                argy = argx
                argx = pts[i]



            print(type(argx))
            x_ = argx[0] - argy[0]
            y_ = argx[1] - argy[1]
            print(x_)
            print(y_)
            if(x_ ==0 or y_==0 ):
                continue
            else:
                if(posinside(x_,y_)):
                    print('*')
                    print(pyautogui.position())
                    cur = pyautogui.position()
                    pyautogui.mouseDown(cur[0]+x_,cur[1]-y_,button='left')


def f3(count):
    if len(count) > 0 :
        return True
    else:
        print("ERRORO")
        return False

#if __name__ == "__main__":
i = input("start?")
t1 = threading.Thread(target=f1)
t2 = threading.Thread(target=f2)

t1.start()
t2.start()


t1.join()
t2.join()
print("the end")
