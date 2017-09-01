import cv2;
import numpy as np;
import copy
import os
import matplotlib.pyplot as plt
 
    
    
    
def diff(roiname,imgname):



    print(roiname)
    roi = np.int8(cv2.imread(roiname)[:,:,2])
    img = np.int8(cv2.imread(imgname)[:,:,2])
    diff = np.uint8(np.abs(roi - img))
    
    th, im_th = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY_INV);

    plt.imshow(im_th)

    plt.show()
    # Copy the thresholded image.
    im_floodfill = copy.copy(im_th)#.copy()
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))  
    erodei = cv2.erode(im_floodfill, element) 
    print(erodei)
    
    
    cimg,contours,hierarchy = cv2.findContours(erodei,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    plt.imshow(erodei)
    plt.imsave('./roi/%s'%roiname.split('/')[-1],erodei)
    
    
    
# Read image
flists = sorted(os.listdir('all/'))
print(len(flists))
#for ind in range(len(flists)):
for ind in range(1):
    imgname = flists[ind]
    if '_ROI' in imgname:
        continue
    roiname = ''.join([imgname.split('.')[0],'_ROI','.jpg'])
    print(roiname)
    if roiname not in flists:
        print(roiname,'Not Found!')
        continue
    diff(os.path.join('all/',roiname),os.path.join('all/',imgname))


