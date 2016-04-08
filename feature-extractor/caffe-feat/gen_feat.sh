#!/bin/sh
echo "Generating image locations"
python mlt_get_caffe_img.py 
echo "Directory change to caffe/examples"
cd ~/caffe/examples 
echo "Extracting Caffe features and saving to mlt_allX.txt"
python mlt_caffe.py -i ~/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/mlt_allimg.txt -o ~/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/mlt_allX.txt
echo "Caffe features extracted"
