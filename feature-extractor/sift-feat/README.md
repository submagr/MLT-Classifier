- mlt_sift.m : Place this file in home directory and run
- feat_sift_vlfeat_mlt.mat : generated features 
- For using these features in python 

	import scipy.io
	mat = scipy.io.loadmat('feat_sift_vlfeat_mlt.mat')
	X = mat['sift_features']
	y = mat['y']
