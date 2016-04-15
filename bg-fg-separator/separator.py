import sys
import cv2
import imutils
import numpy as np
def background_subtraction(file):
	threshdict=[]
	framedict=[]
	kvariable=0
	jvariable=1
	ivariable=1
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5),(3,3))	
	capture = cv2.VideoCapture(file)
	fgbg = cv2.BackgroundSubtractorMOG2(history=500,varThreshold = 16)
	#Tried MOG and MOG2, MOG2 has better performance

	framedict=[]
	threshdict=[]
	while 1:
		retvalue, frame = capture.read()
		if retvalue == False:
			break

		# doing blur, resizing and then getting fgmask
		frame = cv2.blur(frame,(3,3))
		grayscale = imutils.resize(frame, width=(len(frame)/3))
		fgmask = fgbg.apply(grayscale,learningRate=5.0/500)
		#fill holes
		threshold = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
		threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
		#remove noise

		# then find contours
		# on thresholded image
		threshdict.append(threshold.copy())
		(contours, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		framedict.append(contours)
		# loop over the contours
		for contour in contours:
			# ignore too small contours
			if cv2.contourArea(contour) < 450:
				continue

			# compute the bounding box
			(x, y, width, height) = cv2.boundingRect(contour)
			new_object = frame.copy()[y:y+height,x:x+width]
			cv2.imwrite('../classifier/one-vs-rest-svm/Predictor/temp_data/' + str(jvariable) + '.png', new_object)
			jvariable += 1

		key = cv2.waitKey(1) & 0xFF

	print('Image Saving Done...Computing Features...')
	capture.release()
	cv2.destroyAllWindows()
	import subprocess
	import joblib
	p = subprocess.Popen(['../classifier/one-vs-rest-svm/Predictor/prediction.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out1, err = p.communicate()
	predictions = joblib.load('../classifier/one-vs-rest-svm/Predictor/predictions.dump')
	capture = cv2.VideoCapture(file)
	print('features computed..showing the video now...')
	ivariable = 0
	jvariable = 1
	while 1:
		retvalue, frame = capture.read()
		if retvalue == False:
			break
		ivariable+=1
		contours=framedict[ivariable]
		frame = imutils.resize(frame, width=(len(frame)/3))
		# loop over the contours
		for contour in contours:
			# if the contour is too small, ignore it
			if cv2.contourArea(contour) < 450:
				continue

			# predict the label
			(x, y, width, height) = cv2.boundingRect(contour)
			label=predictions[str(jvariable) + '.png']
			if label=="Four-Wheeler":
				color=(255,0,0)
			elif label=="Two-Wheeler":
				color=(0,255,0)
			elif label=="Pedestritian":
				color=(0,0,255)
			elif label=="Three-Wheeler":
				color=(255,255,0)
   
			font = cv2.FONT_HERSHEY_SIMPLEX
			if (2*y+height)/2 >125:
				cv2.putText(frame,label,(x,y-5), font, 0.4,color,1)
			else:
				cv2.putText(frame,label,(x,y+height+10), font, 0.4,color,1)
			jvariable+=1
			cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)

		cv2.imshow("Final Output", frame)
		cv2.imwrite('../classifier/one-vs-rest-svm/Predictor/temp_data2/image' + str(ivariable) + '.png', frame)
		cv2.imshow("threshold",threshdict[ivariable])
		cv2.waitKey(0) 
		key = cv2.waitKey(1) & 0xFF


	capture.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	if len(sys.argv) == 2:
		file = sys.argv[1]

	background_subtraction(file)
