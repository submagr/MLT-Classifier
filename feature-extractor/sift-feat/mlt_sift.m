imgSets = [imageSet('/home/cse/UGP/data_mlt/Rickshaw'),imageSet('/home/cse/UGP/data_mlt/Autorickshaw'),imageSet('/home/cse/UGP/data_mlt/Motorcycle'),imageSet('/home/cse/UGP/data_mlt/Bicycle'),imageSet('/home/cse/UGP/data_mlt/Person')]
{ imgSets.Description } % display all labels on one line
[imgSets.Count]         % show the corresponding count of images
minSetCount = min([imgSets.Count]); % determine the smallest amount of images in a category

% Use partition method to trim the set.
%imgSets = partition(imgSets, minSetCount, 'randomize');

% Notice that each set now has exactly the same number of images.
[imgSets.Count]

run('VLFEATROOT/toolbox/vl_setup')

y = []
for i = 1:5
   i
   for j = 1:imgSets(i).Count;
        I_img.label = i ;
        I = read(imgSets(i),j);
        if size(I,3) == 3
            I = rgb2gray(I);
        end
        I = single(I) ;
        [f,d] = vl_sift(I) ;
        I_img.descrip = single(d);
        if exist('X','var')
            X = [X d];
        else
            X = d;
        end
        if exist('X_img','var')
            X_img = [X_img I_img];
        else
            X_img = [I_img];
        end
        y = [y i];
    end
end

numClusters = 10 ;
X = single(X);
[centers, assignments] = vl_kmeans(X, numClusters);

for i = 1:length(X_img)
    raw_img(i).label = X_img(i).label;
    [m,n] = size(X_img(i).descrip)
    for j = 1:n
        [~, k] = min(vl_alldist(X_img(i).descrip(:,j), centers)) ;   
        if exist('hist1','var')
            hist1 = [hist1 k];
        else
            hist1 = [k];
        end
    raw_img(i).hist = hist1;
    end
end    

sift_features = []
y = []
for i = 1:length(raw_img)
    fe(numClusters) = 0; 
    for j = 1:length(raw_img(i).hist)
        fe(raw_img(i).hist(j))= fe(raw_img(i).hist(j)) + 1;
    end
    sift_features = [sift_features ; fe];
    y = [y ; raw_img(i).label];
end

save('feat_sift_vlfeat_mlt.mat','sift_features','y')

%{
For using these features in python 

import scipy.io
mat = scipy.io.loadmat('feat_sift_vlfeat_mlt.mat')
X = mat['sift_features']
y = mat['y']

}%
