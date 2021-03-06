from collections import deque
import numpy as np
import argparse
import imutils
import cv2
 

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--ballvideo.mp4",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

 
greenLower = (22, 68, 77)
greenUpper = (36, 235, 255)
pts = deque(maxlen=args["buffer"])
 

if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
else:
	camera = cv2.VideoCapture(args["video"])


while True:
	(grabbed, frame) = camera.read()
 
	if args.get("video") and not grabbed:
		break
 
	frame = imutils.resize(frame, width=600)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)


		((x, y), radius) = cv2.minEnclosingCircle(c)
		#a,b,c,d = cv2.boundingRect(c)
		rect = cv2.minAreaRect(c)
		rect = rect[1][0]*rect[1][1]
		cir = 3.14*radius*radius
		#print 'rec area'
		#print rect
		
		#print 'cir area'
		#print cir


		if rect + 100> cir and cir>350:

			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
			#if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
			(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			dist = (60*100)/(radius*2)
			print ("Distance: ",dist-2)
 
		pts.appendleft(center)
		#print pts
	# loop over the set of tracked points
	#for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
	#	if pts[i - 1] is None or pts[i] is None:
#			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
#		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
#		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
 
		if key == ord("q"):
			break
 
camera.release()
cv2.destroyAllWindows()