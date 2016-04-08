#!/bin/sh
echo "Generating image locations in mlt_allimg.txt"
python mlt_get_caffe_img.py 
echo "Directory change to caffe/examples"
cd ~/caffe/examples 
echo "Extracting Caffe features and saving to mlt_allX.txt"
python mlt_caffe.py -i ~/MLT-Classifier/feature-extractor/caffe-feat/fine_allimg.txt -o ~/MLT-Classifier/feature-extractor/caffe-feat/fine_allX.txt
echo "Caffe features extracted for fine dataset"
python mlt_caffe.py -i ~/MLT-Classifier/feature-extractor/caffe-feat/coarse_allimg.txt -o ~/MLT-Classifier/feature-extractor/caffe-feat/coarse_allX.txt
echo "Caffe features extracted for coarse dataset"
