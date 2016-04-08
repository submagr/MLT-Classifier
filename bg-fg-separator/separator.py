import numpy as np
import imutils
import cv2
import sys
def background_subtract(filename):
	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
	cap = cv2.VideoCapture(filename)
	fgbg = cv2.BackgroundSubtractorMOG2(history=300,varThreshold = 30)
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5),(3,3))

	ret, frame = cap.read()
	# frame = imutils.resize(frame, width=500)
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# gray = cv2.GaussiaBlur(gray, (21, 21), 0)
	frame = imutils.resize(frame, width=(len(frame)/3))
	gray = cv2.blur(frame,(3,3))
	fgmask = fgbg.apply(gray)

	i = 1
	j = 1
	k=0
	framedict=[]
	threshdict=[]
	while True:
		# print i
#		k+=1
#		if k>=100:
#			break
		ret, frame = cap.read()

		if ret == False:
			break

		# resize the frame, convert it to grayscale, and blur it
		# frame = imutils.resize(frame, width=500)
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# gray = cv2.GaussianBlur(gray, (11, 11), 0)
		frame = imutils.resize(frame, width=(len(frame)/3))
		gray = cv2.blur(frame,(3,3))
		fgmask = fgbg.apply(gray)
		thresh = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
		thresh = cv2.threshold(thresh, 100, 255, cv2.THRESH_BINARY)[1]

		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image

		# thresh = cv2.erode(thresh, kernel, iterations=1)
		#cv2.imshow('thresh without erosion', thresh)
		threshdict.append(thresh.copy())
		(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		framedict.append(cnts)
		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < 400:
				continue

			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			# print x,y,w,h
			#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			new_object = frame.copy()[y:y+h,x:x+w]
			#cv2.imshow('detected_object', new_object)
			# key = cv2.waitKey(1) & 0xFF
			cv2.imwrite('./MLT-Classifier/classifier/one-vs-rest-svm/Predictor/temp_data/' + str(j) + '.png', new_object)
			j += 1
			text = "Occupied"
		#cv2.imshow("Security Feed", frame)
		#cv2.imshow("Security Feed", frame)
		#cv2.imshow("threshold", thresh)

		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
	print('hi')
	cap.release()
	cv2.destroyAllWindows()
	import subprocess
	import joblib
	p = subprocess.Popen(['/home/cse/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/prediction.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out1, err = p.communicate()
	predictions = joblib.load('/home/cse/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/predictions.dump')
	cap = cv2.VideoCapture(filename)
	print('hi1')
	ret, frame = cap.read()
	i = 0
	j = 1
	#print cnts
	while True:
		# print i
		ret, frame = cap.read()
		if ret == False:
			break
		frame = imutils.resize(frame, width=(len(frame)/3))
		# loop over the contours
		cnts=framedict[i]
		i+=1
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < 400:
				continue

			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			# print x,y,w,h
			label=predictions[str(j) + '.png']
			font = cv2.FONT_HERSHEY_SIMPLEX
			if (2*y+h)/2 >125:
				cv2.putText(frame,label,(x,y-5), font, 0.4,(255,255,0),1)
			else:
				cv2.putText(frame,label,(x,y+h+10), font, 0.4,(255,255,0),1)
	                #cv2.putText(frame,label,(x,y), font, 0.5,(0,255,0),1)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			#new_object = frame.copy()[y:y+h,x:x+w]
			#cv2.imshow('detected_object', new_object)
			# key = cv2.waitKey(1) & 0xFF
			#cv2.imwrite('./temp/' + str(j) + '.png', new_object)
			j += 1
			text = "Occupied"

		cv2.imshow("Security Feed", frame)
		out.write(frame)
		cv2.imshow("thresh",threshdict[i])
		cv2.waitKey(0) 
		#cv2.imshow("threshold", thresh)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break

	cap.release()
	out.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	if len(sys.argv) == 2:
		filename = sys.argv[1]

	background_subtract(filename)
