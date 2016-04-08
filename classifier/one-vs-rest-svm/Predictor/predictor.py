from sklearn.externals import joblib
import scipy.io
from random import shuffle
import os

CONST_LABELS = 6 
CONST_NUMBER_TRAIN_IMG =  50 
CONST_NUMBER_TEST_IMG = 50 
CONST_X_FILE = 'video_X.txt'
CONST_y_FILE = '../../feature-extractor/caffe-feat/mlt_allimg_labels.txt'
CONST_SIFT_FILE = '../../feature-extractor/sift-feat/feat_sift_vlfeat_mlt.mat'
CONST_C=[100]
CONST_KERNEL=['linear']
CONST_FEATURE='CAFFE'
CONST_MAP = {2:"Autorickshaw",1:"Bicycle",6:"Car",4:"Motorcycle",5:"Person",3:"Rickshaw"}
def load_features():
	if CONST_FEATURE == 'CAFFE':	
		with open(CONST_X_FILE,'r') as f:
			content = f.readlines()
			X = []
			for i in range(0,len(content)):
				X.append([float(n) for n in content[i].split()])
		return X
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


ovr_classifiers = joblib.load('../trained_model/CAFFE/ovr.pkl')
X = load_features()
predictions=[]
confidence = []
print "Making Binary Predictions"
for i in range(1,len(ovr_classifiers)+1):
        print i
	confidence.append(ovr_classifiers[i].decision_function(X))

print "Overall Predictions "
for j in range(0,len(X)):
	predictions.append(-1)
	score=-999999
	for k in range(0,CONST_LABELS):
		if confidence[k][j]>score:
			predictions[j]=k+1
			score=confidence[k][j]

predicted = {}
print "Making predicted dictionary"
imgs = [line.rstrip('\n') for line in open('video_imgs.txt')]
for i in range(0,len(imgs)):
	imgs[i] = os.path.basename(imgs[i])
	predicted[imgs[i]] = CONST_MAP[predictions[i]]

print "Dumping predicted images to predictions.dump"
joblib.dump(predicted,'predictions.dump')

# import subprocess
# import joblib
# p = subprocess.Popen(['/home/cse/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/prediction.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out, err = p.communicate()
# predictions = joblib.load('/home/cse/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/predictions.dump')
