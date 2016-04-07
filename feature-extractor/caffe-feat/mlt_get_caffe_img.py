import os
rootdir = '../../data'
out_img = open('mlt_allimg.txt','wb')
out_label = open('mlt_allimg_labels.txt','wb')
j = 0
for dirpath, dirnames, filenames in os.walk(rootdir):
    for file in filenames:
        file= os.path.join(os.path.abspath(dirpath), file)
        label = os.path.basename(os.path.normpath(os.path.abspath(dirpath)))
        out_img.write(file+'\n')
        out_label.write(str(j)+'\n')
    j += 1

