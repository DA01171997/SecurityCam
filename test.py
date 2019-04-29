from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
bodyCascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	grayFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	face = faceCascade.detectMultiScale(grayFrame, 1.3, 5)
	body = bodyCascade.detectMultiScale(grayFrame, 1.3, 5)
	if len(face) > 0 or len(body) > 0:
		cv2.imwrite('detection.png', image)
	for (xTop, yTop, width, height) in body:
		cv2.rectangle(image, (xTop, yTop), (xTop + width, yTop + height), (255, 0, 0), 2)
	for (xTop, yTop, width, height) in face: 
		cv2.rectangle(image, (xTop, yTop), (xTop + width, yTop + height), (255, 255, 0), 2)
	cv2.imshow("Frame", image)
	key = cv2.waitKey(10)
	rawCapture.truncate(0)
	if key == 27:
		break

