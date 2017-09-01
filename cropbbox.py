import scipy.misc as misc
import cv2
#import pdb
import os
import numpy as np

#imageDirA = "Data_zoo/MIT_SceneParsing/ADEChallengeData2016/images/training/"
#maskDirA = "Data_zoo/MIT_SceneParsing/ADEChallengeData2016/annotations/training/"
#imageDirB = "Data_zoo/MIT_SceneParsing/ADEChallengeData2016/images/validation/"
#maskDirB = "Data_zoo/MIT_SceneParsing/ADEChallengeData2016/annotations/validation/"
imageDirA = "img_train/"
maskDirA  = "mask_train/"
imageDirB = "img_test/"
maskDirB  = "mask_test/"

def watershed(mask):
    img = cv2.imread(mask)
    #cv2.imshow("window",img)
    #cv2.waitKey (0)
    #cv2.destroyAllWindows()



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
    y0 = i

    for i in range(len(ax_x)):
        if ax_x[len(ax_x)-i-1] != 0:
            break
    y1 = len(ax_x) - i-1

    for i in range(len(ax_y)):
        if ax_y[i] != 0:
            break
    x0 = i

    for i in range(len(ax_y)):
        if ax_y[len(ax_y)-i-1] != 0:
            break
    x1 = len(ax_y) - i -1

    maskclipped = misc.imread(mask)[x0:x1,y0:y1]
    imageclipped = misc.imread(image)[int(x0*1.0/len(ax_y)*388):int(x1*1.0/len(ax_y)*388),int(y0*1.0/len(ax_x)*388):int(y1*1.0/len(ax_x)*388)]
    misc.imsave(imageOut,imageclipped)
    misc.imsave(maskOut,maskclipped)

def readimage(imageDir,maskDir):
    fnames = os.listdir(imageDir)
    for fname in fnames:
        print(fname)
        if fname[-3:] != 'png':
            continue
        clip(os.path.join(imageDir,fname), \
                os.path.join(maskDir,fname), \
                os.path.join('./',imageDir,'out',fname), \
                os.path.join('./',maskDir,'out',fname))

def run():
    readimage(imageDirA,maskDirA)
    readimage(imageDirB,maskDirB)

run()
