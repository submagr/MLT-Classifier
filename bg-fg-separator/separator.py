import numpy as np
import imutils
import cv2
import sys
def background_subtract(filename):
	cap = cv2.VideoCapture(filename)
	#Tried MOG and MOG2, MOG2 has better performance
	fgbg = cv2.BackgroundSubtractorMOG2(history=500,varThreshold = 16)
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5),(3,3))

	i = 1
	j = 1
	k=0
	framedict=[]
	threshdict=[]
	while True:
		ret, frame = cap.read()
		if ret == False:
			break

		# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=(len(frame)/3))
		gray = cv2.blur(frame,(3,3))
		fgmask = fgbg.apply(gray,learningRate=5.0/500)
		#Remove Noise
		thresh = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
		#Fill small holes
		thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
		thresh = cv2.threshold(thresh, 100, 255, cv2.THRESH_BINARY)[1]

		# then find contours
		# on thresholded image
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
			new_object = frame.copy()[y:y+h,x:x+w]
			cv2.imwrite('./MLT-Classifier/classifier/one-vs-rest-svm/Predictor/temp_data/' + str(j) + '.png', new_object)
			j += 1
			text = "Occupied"

		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
	print('Image Saving Done...Computing Features...')
	cap.release()
	cv2.destroyAllWindows()
	import subprocess
	import joblib
	p = subprocess.Popen(['/home/cse/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/prediction.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out1, err = p.communicate()
	predictions = joblib.load('/home/cse/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/predictions.dump')
	cap = cv2.VideoCapture(filename)
	print('features computed..showing the video now...')
	ret, frame = cap.read()
	i = 0
	j = 1
	#print cnts
	while True:
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
			label=predictions[str(j) + '.png']
			if label=="Four-Wheeler":
				color=(255,0,0)
			elif label=="Two-Wheeler":
				color=(0,255,0)
			elif label=="Pedestritian":
				color=(0,0,255)
			elif label=="Three-Wheeler":
				color=(255,255,0)
   
			font = cv2.FONT_HERSHEY_SIMPLEX
			if (2*y+h)/2 >125:
				cv2.putText(frame,label,(x,y-5), font, 0.4,color,1)
			else:
				cv2.putText(frame,label,(x,y+h+10), font, 0.4,color,1)
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
			j += 1
			text = "Occupied"

		cv2.imshow("Security Feed", frame)
		cv2.imwrite('./MLT-Classifier/classifier/one-vs-rest-svm/Predictor/temp_data2/image' + str(i) + '.png', frame)
		cv2.imshow("thresh",threshdict[i])
		cv2.waitKey(0) 
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break

	cap.release()
	#out.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	if len(sys.argv) == 2:
		filename = sys.argv[1]

	background_subtract(filename)
