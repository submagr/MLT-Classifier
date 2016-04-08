import numpy as np
from sklearn.svm import SVC
from random import shuffle
import sys
import pickle
import scipy.io
from sklearn.externals import joblib

CONST_DATA = 'FINE' 
CONST_USE_ENTIRE_DATA = 1 
CONST_NUMBER_TRAIN_IMG =  35
CONST_NUMBER_TEST_IMG = 10 
CONST_C=[10]
CONST_KERNEL=['rbf']
CONST_FEATURE='CAFFE'
CONST_MODEL_DUMP = 'trained_model/'+CONST_FEATURE+'_'+CONST_DATA+'/ovr.pkl'

if CONST_DATA == 'FINE':
    CONST_X_FILE = '../../feature-extractor/caffe-feat/fine_allX.txt'
    CONST_y_FILE = '../../feature-extractor/caffe-feat/fine_allimg_labels.txt'
    CONST_SIFT_FILE = '../../feature-extractor/sift-feat/feat_sift_vlfeat_mlt.mat'
    CONST_LABELS = 6 
    CONST_MAP = {2:"Autorickshaw",1:"Bicycle",6:"Car",4:"Motorcycle",5:"Person",3:"Rickshaw"}
else : 
    CONST_X_FILE = '../../feature-extractor/caffe-feat/coarse_allX.txt'
    CONST_y_FILE = '../../feature-extractor/caffe-feat/coarse_allimg_labels.txt'
    CONST_SIFT_FILE = '../../feature-extractor/sift-feat/feat_sift_vlfeat_mlt.mat'
    CONST_LABELS = 4 
    CONST_MAP = {1:"Four-Wheeler",2:"Two-Wheeler",3:"Pedestritian",4:"Three-Wheeler"}

#C=[0.1,1,10,100,1000,10000,100000,1000000]
#kernel=['linear', 'poly', 'rbf', 'sigmoid']
#Tuned Parameters : C = 10, kernel = rbf

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

def trim_data(data):
	train_X=[]
	test_y=[]
	train_y=[]
	test_X=[]
	if CONST_USE_ENTIRE_DATA == 1:
		print('Using Entire Data Set with 3:1 Train Test Ratio')
		for i in range(1,CONST_LABELS+1):
			for j in range(0,int(len(data[i])*0.75)):
				train_X = train_X + [data[i][j]]
				train_y = train_y + [i]
			for j in range(int(len(data[i])*0.75), len(data[i])):
				test_X = test_X + [data[i][j]]
				test_y = test_y + [i]
	else : 
		print('Trimming Data Set Train : ',CONST_NUMBER_TRAIN_IMG,', Test : ',CONST_NUMBER_TEST_IMG)
		for i in range(1,CONST_LABELS+1):
			for j in range(0,CONST_NUMBER_TRAIN_IMG/CONST_LABELS):
				try : 
					train_X = train_X + [data[i][j]]
					train_y = train_y + [i]
				except Exception as e:
					print 'Insufficient Train Images for label : ', j
					break
			for j in range(CONST_NUMBER_TRAIN_IMG/CONST_LABELS, (CONST_NUMBER_TRAIN_IMG+CONST_NUMBER_TEST_IMG)/CONST_LABELS):
				try:	
					test_X = test_X + [data[i][j]]
					test_y = test_y + [i]
				except Exception as e:
					print 'Insufficient Test Images for label : ', j
					break
	return train_X, train_y, test_X, test_y

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
		print "Number of ",CONST_MAP[i]," = ", len(data[i])

	train_X, train_y, test_X, test_y = trim_data(data)
	train_X, train_y = double_shuffle(train_X, train_y)
	test_X, test_y = double_shuffle(test_X, test_y)
	return train_X, train_y, test_X, test_y


def get_binary_data(X,y,pos_label):
	X_extract=[]
	y_extract=[]
	for l in range(0,len(X)):
		if train_y[l]==pos_label:
			X_extract.append(train_X[l])
			y_extract.append(1)
		else:
			X_extract.append(train_X[l])
			y_extract.append(-1)
	return X_extract, y_extract

def print_results(result):
    true = 0
    false = 0
    for label in result:
        true += result[label]['true']
        false += result[label]['false']
        print '         Accuracy for Label : ', label,' is ', result[label]['true']*1.0/(result[label]['true']+result[label]['false'])
    print '     Overall Accuracy = ', true*1.0/(true+false)
        
train_X, train_y, test_X, test_y = get_data()
for c in CONST_C:
	for knl in CONST_KERNEL:
		print "Training for Kernel : ", knl, " with C : ",c
		true_predict=0
		false_predict=0
		confidence=[]
		ovr_classifiers = {} 
		for j in range(1,CONST_LABELS+1):
			print "		Training One vs rest for label :", j
			X_extract, y_extract =  get_binary_data(train_X, train_y, j)
			classifier=SVC(C=c,kernel=knl)
			classifier.fit(X_extract, y_extract)	
			print "		Model trained for label :", j
			ovr_classifiers[j] = classifier
			confidence.append(classifier.decision_function(test_X))
                print "         Dumping model in file : ",CONST_MODEL_DUMP 
                joblib.dump(ovr_classifiers,CONST_MODEL_DUMP)
                predictions=[]
                print "		Testing started"
                for j in range(0,len(test_X)):
                                predictions.append(-1)
                                score=-999999
                                for k in range(0,CONST_LABELS):
                                        if confidence[k][j]>score:
                                                predictions[j]=k+1
                                                score=confidence[k][j]
                detailed_predictions = {}
                for j in range(0,len(predictions)):
                                if predictions[j]!=test_y[j]:
                                        if CONST_MAP[test_y[j]] in detailed_predictions : 
                                            detailed_predictions[CONST_MAP[test_y[j]]]['false']+=1
                                        else : 
                                            detailed_predictions[CONST_MAP[test_y[j]]] = {}
                                            detailed_predictions[CONST_MAP[test_y[j]]]['true'] = 0 
                                            detailed_predictions[CONST_MAP[test_y[j]]]['false'] = 1 
                                else:
                                        if CONST_MAP[test_y[j]] in detailed_predictions : 
                                            detailed_predictions[CONST_MAP[test_y[j]]]['true']+=1
                                        else : 
                                            detailed_predictions[CONST_MAP[test_y[j]]] = {}
                                            detailed_predictions[CONST_MAP[test_y[j]]]['true'] = 1 
                                            detailed_predictions[CONST_MAP[test_y[j]]]['false'] = 0 
                print_results(detailed_predictions)
