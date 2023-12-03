import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
from scipy.fft import fft
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import win32api, win32con

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

tracker = htm.handTracker(detectionCon=0.7, maxHands=1)

x = 0
y = 0
area = 0

while True:
	success, img = cap.read()

	# Find Hand
	img = tracker.findHands(img)
	lmList, bbox = tracker.findPosition(img, draw=True)

	if len(lmList) != 0:
		img, lineInfo = tracker.findCoordinate(8, img)
		xo = x
		yo = y
		xn = 1920 - int(lineInfo[0] / 0.416) 
		yn = int(lineInfo[1] / 0.555)
		if(xn != xo):
			if(yn != yo):
				x =  int((xo + xn) / 2)
				y =  int(yo + ((x - xo) * ((yn - yo)/(xn - xo))))
		cv2.circle(img, (lineInfo[0], lineInfo[1]), 15, (255,255,0), cv2.FILLED)
		cv2.putText(img, f'x {x} y {y} ', (600,50), cv2.FONT_HERSHEY_COMPLEX, 1, ( 255,255,0), 3)
		win32api.SetCursorPos((x,y))
		

	
	# Frame rate
	cTime = time.time()
	fps = 1 / (cTime - pTime)
	pTime = cTime

	cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX, 1, ( 255,255,0), 3)

	cv2.imshow("Img", img)
	cv2.waitKey(1)