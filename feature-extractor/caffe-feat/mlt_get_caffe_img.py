import os
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

