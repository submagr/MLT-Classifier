Steps : 
- python mlt_get_caffe_img.py : This will generate image locations and labels in mlt_allimg.txt and mlt_allimg_labels.txt
- Then place mlt_caffe.py file in /home/cse/caffe/examples
- run python mlt_caffe.py -i ~/MLT-Classifier/feature-extractor/caffe-feat/mlt_allimg.txt -o ~/MLT-Classifier/feature-extractor/caffe-feat/mlt_allX.txt 
