#!/bin/bash
echo "rm video_imgs.txt : Clear earlier stored features if any... "
rm video_imgs.txt
echo "python gen_caffe_input.py : Generating address of images for extracting caffe features... "
python gen_caffe_input.py
echo "cd to caffe directory..."
cd ~/caffe/examples 
echo "Generating caffe features and dumping them in a file..."
python mlt_caffe.py -i ~/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/video_imgs.txt -o ~/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/video_X.txt
echo "directory back to Predictor..."
cd ~/MLT-Classifier/classifier/one-vs-rest-svm/Predictor/ 
echo "Making predictions from pretrained model..."
python predictor.py
echo "Removing image data..."
rm -r temp_data
mkdir temp_data
