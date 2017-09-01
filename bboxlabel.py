import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import scipy.misc as misc
import glob
import os




def watershed(fname):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    dist_transform = cv2.distanceTransform(gray,1,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.05*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)

    box = []
    cimg,contours,hierarchy = cv2.findContours(sure_fg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        cnt = contours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        box.append([x,y,x+w,y+h])

    resizedbox = []
    newsize = 388
    print len(box)
    for item in box:
        newitem = [0,0,0,0]
        newitem[0] = int(item[0]*newsize*1.0/img.shape[1])
        newitem[1] = int(item[1]*newsize*1.0/img.shape[0])
        newitem[2] = int(item[2]*newsize*1.0/img.shape[1])
        newitem[3] = int(item[3]*newsize*1.0/img.shape[0])
        resizedbox.append(newitem)
    print len(resizedbox)

    CHECK_RESULT = True
    if CHECK_RESULT and np.random.rand() < 0.1:
        imgname = fname.split('/')[-1]
        imgpath = '/Users/wang/work/processingData/data/img_train/'
        img = cv2.imread(os.path.join(imgpath,imgname))
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        new = gray
        for item in resizedbox:
            print(item)
            new = cv2.rectangle(new,(item[0],item[1]),(item[2],item[3]),(0,255,0),2)
        plt.imshow(new)
        plt.show()

    return resizedbox

def clip(image,mask,imageOut,maskOut):
    masktmp = misc.imread(mask)
    if len(masktmp.shape)==3:
        mask2 = np.sum(masktmp,axis=2)
    else:
        mask2 = masktmp
    ax_x = np.sum(mask2,axis=0)
    ax_y = np.sum(mask2,axis=1)

    print(len(ax_x))
    for i in range(len(ax_x)):
        if ax_x[i] != 0:
            break
    y1 = i

    for i in range(len(ax_x)):
        if ax_x[len(ax_x)-i-1] != 0:
            break
    y2 = len(ax_x) - i-1

    for i in range(len(ax_y)):
        if ax_y[i] != 0:
            break
    x1 = i

    for i in range(len(ax_y)):
        if ax_y[len(ax_y)-i-1] != 0:
            break
    x2 = len(ax_y) - i -1

    #maskclipped = misc.imread(mask)[x1:x2,y1:y2]
    #imageclipped = misc.imread(image)[int(x1*1.0/len(ax_y)*388):int(x2*1.0/len(ax_y)*388),int(y1*1.0/len(ax_x)*388):int(y2*1.0/len(ax_x)*388)]
    #misc.imsave(imageOut,imageclipped)
    #misc.imsave(maskOut,maskclipped)


def run(fpath,savename,MULTI_BBOX):
    fnames = glob.glob(os.path.join(fpath,'*.png'))
    imgpath = '/Users/wang/work/processingData/data/img_train/'
    imgnames = [imgpath + name.split('/')[-1] for name in fnames]
    with open(savename,'w') as savefile:
        for i,fname in enumerate(fnames):
            print(fname)
            if MULTI_BBOX:
                coords = watershed(fname)
                for coord in coords:
                    savefile.write("%s,%s,%d,%d,%d,%d,%s\n"%(imgnames[i],fname,coord[0],coord[1],coord[2],coord[3],'node'))
            else:
                boxes = watershed(fname)
                boxes = np.array(boxes)
                coord = np.zeros(4)
                coord[0],coord[1] = min(boxes[:,0]),min(boxes[:,1])
                coord[2],coord[3] = max(boxes[:,2]),max(boxes[:,3])
                savefile.write("%s,%s,%d,%d,%d,%d,%s\n"%(imgnames[i],fname,coord[0],coord[1],coord[2],coord[3],'node'))
        #watershed('/Users/wang/work/processingData/mask_test/pw0310965_11_38.png')

run('/Users/wang/work/processingData/data/mask_train/',savename='multilabel.txt',MULTI_BBOX=True)

