import os
rootdir = 'temp_data/'
out_img = open('video_imgs.txt','wb')
# This 0 is correct ! 
for dirpath, dirnames, filenames in os.walk(rootdir):
    for file in filenames:
        file= os.path.join(os.path.abspath(dirpath), file)
        out_img.write(file+'\n')

