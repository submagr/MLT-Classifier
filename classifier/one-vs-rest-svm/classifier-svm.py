import numpy as np
from sklearn.svm import SVC
from random import shuffle
import sys
import pickle
import scipy.io

CONST_LABELS = 5
CONST_NUMBER_TRAIN_IMG =  3500 
CONST_NUMBER_TEST_IMG = 1000 
CONST_X_FILE = '../../feature-extractor/caffe-feat/mlt_allX.txt'
CONST_y_FILE = '../../feature-extractor/caffe-feat/mlt_allimg_labels.txt'
CONST_SIFT_FILE = '../../feature-extractor/sift-feat/feat_sift_vlfeat_mlt.mat'
CONST_C=[100]
CONST_KERNEL=['linear']
CONST_FEATURE='CAFFE'
#C=[0.1,1,10,100,1000,10000,100000,1000000]
#kernel=['linear', 'poly', 'rbf', 'sigmoid']

def double_shuffle(a,b):
    an = []
    bn = []
    index = []
    for i in range(0,len(a)):
        index.append(i) 
    shuffle(index)
    for i in range(0,len(index)):   
        an.append(a[index[i]])
        bn.append(b[index[i]])
    return an,bn

def load_features():
	if CONST_FEATURE == 'CAFFE':	
		with open(CONST_X_FILE,'r') as f:
			content = f.readlines()
			X = []
			for i in range(0,len(content)):
				X.append([float(n) for n in content[i].split()])

		with open(CONST_y_FILE,'r') as f:
			content = f.readlines()
			y = []
			for i in range(0,len(content)):
				y.append(int(content[i]))
		return X,y
	if CONST_FEATURE == 'SIFT':
		mat = scipy.io.loadmat(CONST_SIFT_FILE)
		X = mat['sift_features']
		y = mat['y']
		yn = []
		for i in range(0,len(y)):
			yn.append(int(y[i]))
		return X,yn
	print 'ERROR : CONST_FEATURE = ',CONST_FEATURE, 'does not exist'
	sys.exit()

def get_data():
	X,y = load_features()
	data = {}
	for i in range(0,len(X)):
		if y[i] in data : 
			data[y[i]].append(X[i]) 
		else :
			data[y[i]] = [X[i]]
	for i in range(1,CONST_LABELS+1):
		shuffle(data[i])

	##Temp
	for i in range(1,len(data)+1):
		print "data(",i,") = ", len(data[i])
	train_X=[]
	test_y=[]
	train_y=[]
	test_X=[]

	for i in range(1,CONST_LABELS+1):
		for j in range(0,CONST_NUMBER_TRAIN_IMG/CONST_LABELS):
			train_X = train_X + [data[i][j]]
			train_y = train_y + [i]
		for j in range(CONST_NUMBER_TRAIN_IMG/CONST_LABELS, (CONST_NUMBER_TRAIN_IMG+CONST_NUMBER_TEST_IMG)/CONST_LABELS):
			test_X = test_X + [data[i][j]]
			test_y = test_y + [i]

	train_X, train_y = double_shuffle(train_X, train_y)
	test_X, test_y = double_shuffle(test_X, test_y)
	return train_X, train_y, test_X, test_y

def save_clf(clf,filename):
	s = pickle.dumps(clf)
	with open(filename,'wb') as f:
		f.write(s) 

train_X, train_y, test_X, test_y = get_data()
for c in CONST_C:
	for knl in CONST_KERNEL:
		print "Training for Kernel : ", knl, " with C : ",CONST_C 
		true_predict=0
		false_predict=0
		confidence=[]
		ovr_classifiers = {} 
		for j in range(1,CONST_LABELS+1):
			print "		Training One vs rest for label :", j
			X_extract=[]
			y_extract=[]
			for l in range(0,len(train_X)):
				if train_y[l]==j:
					X_extract.append(train_X[l])
					y_extract.append(1)
				else:
					X_extract.append(train_X[l])
					y_extract.append(-1)
			classifier=SVC(C=c,kernel=knl)
			classifier.fit(X_extract, y_extract)	
			print "		Model trained for label :", j
			ovr_classifiers[j] = classifier
			confidence.append(classifier.decision_function(test_X))

		print "		Dumping model in file : ", 'ovr_classifiers_'+CONST_FEATURE+'.dump'
		save_clf(ovr_classifiers, 'ovr_classifiers_'+CONST_FEATURE+'.dump')
	    #report result
        predictions=[]
        print "		Testing started"
        for j in range(0,len(test_X)):
			predictions.append(-1)
			score=-999999
			for k in range(0,CONST_LABELS):
				if confidence[k][j]>score:
					predictions[j]=k+1
					score=confidence[k][j]
        for j in range(0,len(predictions)):
			if predictions[j]!=test_y[j]:
				false_predict+=1
			else:
				true_predict+=1
        print true_predict, true_predict+false_predict
        accuracy=(true_predict)*1.0/(true_predict+false_predict)
        print ('Accuracy = %f'%accuracy)
