import os
import numpy as np
import glob
import cv2
from sklearn.cluster import KMeans

rootdir = '../../data/fine'
out_img = open('fine_allimg.txt','wb')
out_label = open('fine_allimg_labels.txt','wb')
# This 0 is correct ! 
j = 0
for dirpath, dirnames, filenames in os.walk(rootdir):
    for file in filenames:
        file= os.path.join(os.path.abspath(dirpath), file)
        out_img.write(file+'\n')
        out_label.write(str(j)+'\n')
    j += 1

rootdir = '../../data/coarse'
out_img = open('coarse_allimg.txt','wb')
out_label = open('coarse_allimg_labels.txt','wb')
# This 0 is correct ! 
j = 0
for dirpath, dirnames, filenames in os.walk(rootdir):
    for file in filenames:
        file= os.path.join(os.path.abspath(dirpath), file)
        out_img.write(file+'\n')
        out_label.write(str(j)+'\n')
    j += 1

CONST_DATA_FILE = 'coarse_allimg.txt'
CONST_ENTIRE_DATA = 0
CONST_NUM_IMAGES = 20
images = []
img_locations = []
img_locations = [line.rstrip('\n') for line in open(CONST_DATA_FILE)]
for img in img_locations:
        pic = cv2.imread(img)
        images.append(pic)

if CONST_ENTIRE_DATA != 1 : 
    images = images[0:CONST_NUM_IMAGES]

#get train descriptors
descriptors = np.array([])
detector = cv2.FeatureDetector_create("SIFT")
descriptor = cv2.DescriptorExtractor_create("SIFT")
for img in images:
    continue 
    kp = detector.detect(img)
    kp, des = descriptor.compute(img, kp)
    descriptors = np.append(descriptors, des)

#
##creating a list of images 
#images = []
#path = "Frame_datasample1/frame"
#for count in range(0, 5):
#        infile = path+str(count)+".jpg"
#        pic = cv2.imread(infile)
#        images.append(pic)
#
#my_set = images
#
##get train descriptors
#descriptors = np.array([])
#for pic in my_set:
#    kp, des = cv2.SIFT().detectAndCompute(pic, None)
#    descriptors = np.append(descriptors, des)
#
#desc = np.reshape(descriptors, (len(descriptors)/128, 128))
#desc = np.float32(desc)
#clf = KMeans(n_clusters = 200)
#clf.fit(desc)
#print "Training Done!"
#
## x = cv2.kmeans(descriptors, K=500, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10), attempts=1, flags=cv2.KMEANS_RANDOM_CENTERS)
#train = []
#for count in range(5, 7):
#        infile = path+str(count)+".jpg"
#        pic = cv2.imread(infile)
#        train.append(pic)
#
#fv=[]
#for pic in train:
#    kp, des = cv2.SIFT().detectAndCompute(pic, None)
#    y = clf.predict(des)
#    temp=np.bincount(y)
#    fv.append(temp)
#    print temp
#print("***********************************")
#print fv
