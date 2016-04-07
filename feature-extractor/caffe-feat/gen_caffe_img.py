import os
rootdir = '../Datasets/Caltech/101_ObjectCategories'
out_img = open('img_caffe_input3.txt','wb')
out_label = open('y3.txt','wb')
j = 0
for dirpath, dirnames, filenames in os.walk(rootdir):
    i = 0
    for file in filenames:
        file= os.path.join(os.path.abspath(dirpath), file)
        label = os.path.basename(os.path.normpath(os.path.abspath(dirpath)))
        out_img.write(file+'\n')
        out_label.write(str(j)+'\n')
        i=i+1
        if(i>20):
            break
    j += 1

