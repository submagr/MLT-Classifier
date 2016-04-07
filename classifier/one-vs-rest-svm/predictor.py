from sklearn.externals import joblib
import scipy.io
from random import shuffle

CONST_LABELS = 5
CONST_NUMBER_TRAIN_IMG =  50 
CONST_NUMBER_TEST_IMG = 50 
CONST_X_FILE = '../../feature-extractor/caffe-feat/mlt_allX.txt'
CONST_y_FILE = '../../feature-extractor/caffe-feat/mlt_allimg_labels.txt'
CONST_SIFT_FILE = '../../feature-extractor/sift-feat/feat_sift_vlfeat_mlt.mat'
CONST_C=[100]
CONST_KERNEL=['linear']
CONST_FEATURE='SIFT'

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
	return data


ovr_classifiers = joblib.load('ovr_classifiers_SIFT.pkl')
data = get_data()
