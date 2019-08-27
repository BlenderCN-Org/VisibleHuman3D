"""Metrics

This script allows the user to calculate the indices.

This script requires that 'numpy', 'sklearn', 'scipy', and 'GlobalData' be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * dice - returns the dice indices
    * getCoordMask - returns the coordonate of the contours of the mask
    * msd - returns the msd indices
"""

import numpy as np 

from sklearn import metrics
from skimage import feature
from scipy.spatial.distance import directed_hausdorff
import GlobalData

fily_Mimics_liver_mask=r"..\data\mask\Mimics/Eve_Liver_Mimics_mask.npy"
fily_Mimics_lung_mask=   r"..\data\mask\Mimics/Eve_Lung_Mimics_mask.npy"
fily_Mimics_kidneys_mask=r"..\data\mask\Mimics/Eve_Kidneys_Mimics_mask.npy"
fily_Mimics_heart_mask=r"..\data\mask\Mimics/Eve_Heart_Mimics_mask.npy"
fily_Mimics_bones_mask =r"..\data\mask\Mimics/Eve_Bones_Mimics_mask.npy"
fily_Mimics_abdo_mask   =r"..\data\mask\Mimics/Eve_Abdo_Mimics_mask.npy"

fily_Deci_ML_liver_mask=  r"..\data\mask\Deci/Eve_Liver_Deci_ML_mask.npy"
fily_Deci_ML_lung_mask=   r"..\data\mask\Deci/Eve_Lung_Deci_ML_mask.npy"
fily_Deci_ML_kidneys_mask=r"..\data\mask\Deci/Eve_Kidneys_Deci_ML_mask.npy"
fily_Deci_ML_heart_mask=  r"..\data\mask\Deci/Eve_Heart_Deci_ML_mask.npy"
fily_Deci_ML_bones_mask=r"..\data\mask\Deci/Eve_Bones_Deci_ML_mask.npy"
fily_Deci_ML_abdo_mask=  r"..\data\mask\Deci/Eve_Abdo_Deci_ML_mask.npy"

fily_OG_liver_mask=  r"..\data\mask\OG/Eve_Liver_threshold.npy"
fily_OG_lung_mask=   r"..\data\mask\OG/Eve_Lung_threshold.npy"
fily_OG_kidneys_mask=r"..\data\mask\OG/Eve_Kidneys_threshold.npy"
fily_OG_heart_mask=  r"..\data\mask\OG/Eve_Heart_threshold.npy"
fily_OG_bones_mask = r"..\data\mask\OG/Eve_Bones_OG_threshold.npy"
fily_OG_abdo_mask   =r"..\data\mask\OG/Eve_Abdo_OG_threshold.npy"

fily_Deci_Bl_liver_mask=    r"..\data\mask\Deci/Eve_Liver_Deci_Bl_mask.npy"
fily_Deci_Bl_lung_mask=      r"..\data\mask\Deci/Eve_Lung_Deci_Bl_mask.npy"
fily_Deci_Bl_kidneys_mask=r"..\data\mask\Deci/Eve_Kidneys_Deci_Bl_mask.npy"
fily_Deci_Bl_heart_mask=    r"..\data\mask\Deci/Eve_Heart_Deci_Bl_mask.npy"
#fily_Deci_Bl_bones_mask=r"..\data\mask\Deci/Eve_Bones_Deci_Bl_mask.npy"
#fily_Deci_Bl_abdo_mask=  r"..\data\mask\Deci/Eve_Abdo_Deci_Bl_mask.npy"

fily_Adam_Mimics_liver_mask=r"..\data\mask\Mimics/Adam_Liver_Mimics_mask.npy"
fily_Adam_Mimics_lung_mask=   r"..\data\mask\Mimics/Adam_Lung_Mimics_mask.npy"
fily_Adam_Mimics_kidneys_mask=r"..\data\mask\Mimics/Adam_Kidneys_Mimics_mask.npy"
fily_Adam_Mimics_heart_mask=r"..\data\mask\Mimics/Adam_Heart_Mimics_mask.npy"
fily_Adam_Mimics_bones_mask =r"..\data\mask\Mimics/Adam_Bones_Mimics_mask.npy"
fily_Adam_Mimics_abdo_mask   =r"..\data\mask\Mimics/Adam_Abdo_Mimics_mask.npy"

fily_Adam_OG_liver_mask=     r"..\data\mask\OG/Adam_Liver_threshold.npy"
fily_Adam_OG_lung_mask=      r"..\data\mask\OG/Adam_Lung_threshold.npy"
fily_Adam_OG_kidneys_mask=   r"..\data\mask\OG/Adam_Kidneys_threshold.npy"
fily_Adam_OG_kidneyL_mask=   r"..\data\mask\OG/Adam_KidneyL_threshold.npy"
fily_Adam_OG_kidneyR_mask=   r"..\data\mask\OG/Adam_KidneyR_threshold.npy"
fily_Adam_OG_heart_mask=     r"..\data\mask\OG/Adam_Heart_threshold.npy"
fily_Adam_OG_bones_mask =    r"..\data\mask\OG/Adam_Bones_OG_threshold.npy"
fily_Adam_OG_abdo_mask   =   r"..\data\mask\OG/Adam_Abdo_OG_threshold.npy"


Metrics_Adam_DICE_kidneys_Mimics_OG_path=  r"..\data\metrics/Adam_kidneys_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_Adam_DICE_liver_Mimics_OG_path  =    r"..\data\metrics/Adam_liver_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_Adam_DICE_lung_Mimics_OG_path   =     r"..\data\metrics/Adam_lung_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_Adam_DICE_heart_Mimics_OG_path  =    r"..\data\metrics/Adam_heart_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_Adam_DICE_bones_Mimics_OG_path   =   r"..\data\metrics/Adam_bones_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_Adam_DICE_abdo_Mimics_OG_path  =      r"..\data\metrics/Adam_abdo_Metrics_DICE_Mimics_OG_mask.npy"

Metrics_DICE_kidneys_Mimics_OG_path=  r"..\data\metrics/Eve_kidneys_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_DICE_liver_Mimics_OG_path  =    r"..\data\metrics/Eve_liver_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_DICE_lung_Mimics_OG_path   =     r"..\data\metrics/Eve_lung_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_DICE_heart_Mimics_OG_path  =    r"..\data\metrics/Eve_heart_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_DICE_bones_Mimics_OG_path   =   r"..\data\metrics/Eve_bones_Metrics_DICE_Mimics_OG_mask.npy"
Metrics_DICE_abdo_Mimics_OG_path  =      r"..\data\metrics/Eve_abdo_Metrics_DICE_Mimics_OG_mask.npy"


Metrics_DICE_kidneys_OG_Deci_Bl_path=  r"..\data\metrics/Eve_kidneys_Metrics_DICE_OG_Bl_mask.npy"
Metrics_DICE_liver_OG_Deci_Bl_path  =    r"..\data\metrics/Eve_liver_Metrics_DICE_OG_Bl_mask.npy"
Metrics_DICE_lung_OG_Deci_Bl_path   =     r"..\data\metrics/Eve_lung_Metrics_DICE_OG_Bl_mask.npy"
Metrics_DICE_heart_OG_Deci_Bl_path  =    r"..\data\metrics/Eve_heart_Metrics_DICE_OG_Bl_mask.npy"
Metrics_DICE_bones_OG_Deci_Bl_path   =   r"..\data\metrics/Eve_bones_Metrics_DICE_OG_Bl_mask.npy"
Metrics_DICE_abdo_OG_Deci_Bl_path   =     r"..\data\metrics/Eve_abdo_Metrics_DICE_OG_Bl_mask.npy"


Metrics_kidneys_Deci_ML_Bl_path=    r"..\data\metrics/Eve_kidneys_Metrics_ML_Bl_mask.npy"
Metrics_liver_Deci_ML_Bl_path  =    r"..\data\metrics/Eve_liver_Metrics_ML_Bl_mask.npy"
Metrics_lung_Deci_ML_Bl_path   =    r"..\data\metrics/Eve_lung_Metrics_ML_Bl_mask.npy"
Metrics_heart_Deci_ML_Bl_path  =    r"..\data\metrics/Eve_heart_Metrics_ML_Bl_mask.npy"
Metrics_bones_Deci_ML_Bl_path    =  r"..\data\metrics/Eve_bones_Metrics_ML_Bl_mask.npy"
Metrics_abdo_Deci_ML_Bl_path   =    r"..\data\metrics/Eve_abdo_Metrics_ML_Bl_mask.npy"

Metrics_DICE_kidneys_OG_ML_path = r"..\data\metrics/Eve_kidneys_Metrics_DICE_OG_ML_mask.npy"
Metrics_DICE_liver_OG_ML_path   =   r"..\data\metrics/Eve_liver_Metrics_DICE_Final_ML_mask.npy"
Metrics_DICE_lung_OG_ML_path    =    r"..\data\metrics/Eve_lung_Metrics_DICE_OG_ML_mask.npy"
Metrics_DICE_heart_OG_ML_path   =   r"..\data\metrics/Eve_heart_Metrics_DICE_OG_ML_mask.npy"
Metrics_DICE_bones_OG_ML_path   =   r"..\data\metrics/Eve_bones_Metrics_DICE_OG_ML_mask.npy"
Metrics_DICE_abdo_OG_ML_path    =    r"..\data\metrics/Eve_abdo_Metrics_DICE_OG_ML_mask.npy"

#imgy_Adam_Mimics_liver_mask  =  np.load(fily_Adam_Mimics_liver_mask).astype(np.float64) 
#imgy_Adam_Mimics_lung_mask   =  np.load(fily_Adam_Mimics_lung_mask).astype(np.float64) 
#imgy_Adam_Mimics_kidneys_mask = np.load(fily_Adam_Mimics_kidneys_mask).astype(np.float64) 
#imgy_Adam_Mimics_heart_mask   = np.load(fily_Adam_Mimics_heart_mask).astype(np.float64) 
##imgyAdam__Mimics_bones_mask = np.load(fily_MAdam_imics_bones_mask).astype(np.float64) 
##imgyAdam__Mimics_abdo_mask =   np.load(fily_Adam_Mimics_abdo_mask).astype(np.float64) 

imgy_Mimics_liver_mask  =  np.load(fily_Mimics_liver_mask).astype(np.float64) 
#imgy_Mimics_lung_mask   =  np.load(fily_Mimics_lung_mask).astype(np.float64) 
imgy_Mimics_kidneys_mask = np.load(fily_Mimics_kidneys_mask).astype(np.float64) 
#imgy_Mimics_heart_mask   = np.load(fily_Mimics_heart_mask).astype(np.float64) 
##imgy_Mimics_bones_mask = np.load(fily_Mimics_bones_mask).astype(np.float64) 
##imgy_Mimics_abdo_mask =   np.load(fily_Mimics_abdo_mask).astype(np.float64) 

imgy_Deci_ML_liver_mask  =   np.load(fily_Deci_ML_liver_mask).astype(np.float64) 
imgy_Deci_ML_lung_mask   =    np.load(fily_Deci_ML_lung_mask).astype(np.float64) 
imgy_Deci_ML_kidneys_mask = np.load(fily_Deci_ML_kidneys_mask).astype(np.float64) 
imgy_Deci_ML_heart_mask   =   np.load(fily_Deci_ML_heart_mask).astype(np.float64) 
#imgy_Deci_ML_bones_mask = np.load(fily_Deci_ML_bones_mask).astype(np.float64) 
#imgy_Deci_ML_abdo_mask =   np.load(fily_Deci_ML_abdo_mask).astype(np.float64) 

#imgy_OG_liver_mask =   np.load(fily_OG_liver_mask).astype(np.float64) 
imgy_OG_lung_mask =    np.load(fily_OG_lung_mask).astype(np.float64) 
#imgy_OG_kidneys_mask = np.load(fily_OG_kidneys_mask).astype(np.float64) 
imgy_OG_heart_mask =   np.load(fily_OG_heart_mask).astype(np.float64) 
##imgy_OG_bones_mask =   np.load(fily_OG_bones_mask).astype(np.float64) 
##imgy_OG_abdo_mask =    np.load(fily_OG_abdo_mask).astype(np.float64) 

#imgy_Adam_OG_liver_mask =   np.load(fily_Adam_OG_liver_mask).astype(np.float64) 
#imgy_Adam_OG_lung_mask =    np.load(fily_Adam_OG_lung_mask).astype(np.float64) 
#imgy_Adam_OG_kidneys_mask = np.load(fily_Adam_OG_kidneys_mask).astype(np.float64) 
#imgy_Adam_OG_heart_mask =   np.load(fily_Adam_OG_heart_mask).astype(np.float64) 
##imgyAdam__OG_bones_mask =   np.load(filyAdam__OG_bones_mask).astype(np.float64) 
##imgyAdam__OG_abdo_mask =    np.load(filyAdam__OG_abdo_mask).astype(np.float64) 

imgy_Deci_Bl_liver_mask =   np.load(fily_Deci_Bl_liver_mask).astype(np.float64) 
#imgy_Deci_Bl_lung_mask =    np.load(fily_Deci_Bl_lung_mask).astype(np.float64) 
#imgy_Deci_Bl_kidneys_mask = np.load(fily_Deci_Bl_kidneys_mask).astype(np.float64) 
#imgy_Deci_Bl_heart_mask =   np.load(fily_Deci_Bl_heart_mask).astype(np.float64) 
##imgy_Deci_Bl_bones_mask =   np.load(fily_Deci_Bl_bones_mask).astype(np.float64) 
##imgy_Deci_Bl_abdo_mask =    np.load(fily_Deci_Bl_abdo_mask).astype(np.float64) 

def dice(data_dico, y_true, y_pred, name, true_name, pred_name, labels=None, pos_label=1, average='binary', sample_weight=None):
    """
    Parameters:
    -----------
    y_true : 1d array-like, or label indicator array / sparse matrix
    Ground truth (correct) target values.

    y_pred : 1d array-like, or label indicator array / sparse matrix
    Estimated targets as returned by a classifier.

    labels : list, optional

    """
    
    mbox = (data_dico[name]["box"]["dheight"],data_dico[name]["box"]["drow"],data_dico[name]["box"]["dcolumn"])
    
    dh, dl, dc= mbox
    l1, l2 = dl

    score = []
    print(y_true.shape)
    print(y_pred.shape)
    for z in range (y_true.shape[2]):
        scr = []
        for i in range(y_true.shape[0]):
            if (i < l2) and (i>l1):
                s=metrics.f1_score(y_true[i,:,z], y_pred[i,:,z], labels, pos_label, average, sample_weight)
                scr.append(s)
        score.append(scr)
    sc = np.asarray(score, dtype=np.float64)
    np.save( r"..\data\metrics/Eve_%s_Metrics_DICE_%s_%s_mask.npy" %(name, true_name, pred_name), sc)
    return sc

def getCoordMask(mask):
    edge = feature.canny(np.copy(mask), sigma=6) 
    pixelpoints = np.transpose(np.nonzero(np.copy(edge)))
    X =  pixelpoints[:,0]
    Y =  pixelpoints[:,1]
    return pixelpoints

def msd(mask1, mask2, name, true_name, pred_name):
    score = []
    for z in range (mask1.shape[2]):
        coord1 =  getCoordMask(mask1[:,:,z])
        coord2 =  getCoordMask(mask2[:,:,z])
        score.append(directed_hausdorff(coord1,coord2))
    sc = np.asarray(score, dtype=np.float64)
    np.save( r"..\data\metrics/Eve_%s_Metrics_MSD_%s_%s_mask.npy" %(name, true_name, pred_name), sc)
    return sc
    
dataSF = GlobalData.getDico()["Female"]
dataSM = GlobalData.getDico()["Male"]

dice_score_kidneys  = dice(dataSF,imgy_Mimics_kidneys_mask, imgy_Deci_ML_kidneys_mask ,"Kidneys", "Final", "ML")
dice_score_liver    = dice(dataSF,imgy_Mimics_liver_mask  , imgy_Deci_ML_liver_mask   ,"Liver"  , "Final", "ML")
dice_score_lung     = dice(dataSF,imgy_OG_lung_mask       , imgy_Deci_ML_lung_mask    ,"Lung"   , "Final", "ML")
dice_score_heart    = dice(dataSF,imgy_OG_heart_mask      , imgy_Deci_ML_heart_mask   ,"Heart"  , "Final", "ML")

msd_score_kidneys  = msd(imgy_Mimics_kidneys_mask, imgy_Deci_ML_kidneys_mask ,"Kidneys", "Final", "ML")[:,0]
msd_score_liver    = msd(imgy_Mimics_liver_mask  , imgy_Deci_Bl_liver_mask   ,"Liver"  , "Final", "Bl")[:,0]
msd_score_lung     = msd(imgy_OG_lung_mask       , imgy_Deci_ML_lung_mask    ,"Lung"   , "Final", "ML")[:,0]
msd_score_heart    = msd(imgy_OG_heart_mask      , imgy_Deci_ML_heart_mask   ,"Heart"  , "Final", "ML")[:,0]

print("\n \n dice_score_kidneys ; mean : ", np.mean(dice_score_kidneys), ", std : ", np.std(dice_score_kidneys), ", min : ", np.min(dice_score_kidneys), ", max : ", np.max(dice_score_kidneys), " shape : ", dice_score_kidneys.shape )
print("\n \n dice_score_liver   ; mean : ", np.mean(dice_score_liver  ), ", std : ", np.std(dice_score_liver  ), ", min : ", np.min(dice_score_liver  ), ", max : ", np.max(dice_score_liver  ), " shape : ", dice_score_liver.shape   )
print("\n \n dice_score_lung    ; mean : ", np.mean(dice_score_lung   ), ", std : ", np.std(dice_score_lung   ), ", min : ", np.min(dice_score_lung   ), ", max : ", np.max(dice_score_lung   ), " shape : ", dice_score_lung.shape    )
print("\n \n dice_score_heart   ; mean : ", np.mean(dice_score_heart  ), ", std : ", np.std(dice_score_heart  ), ", min : ", np.min(dice_score_heart  ), ", max : ", np.max(dice_score_heart  ), " shape : ", dice_score_heart.shape   )

print("\n \n msd_score_kidneys ; mean : ", np.mean(msd_score_kidneys), ", std : ", np.std(msd_score_kidneys), ", min : ", np.min(msd_score_kidneys), ", max : ", np.max(msd_score_kidneys), " shape : ", msd_score_kidneys.shape )
print("\n \n msd_score_liver   ; mean : ", np.mean(msd_score_liver  ), ", std : ", np.std(msd_score_liver  ), ", min : ", np.min(msd_score_liver  ), ", max : ", np.max(msd_score_liver  ), " shape : ", msd_score_liver.shape   )
print("\n \n msd_score_lung    ; mean : ", np.mean(msd_score_lung   ), ", std : ", np.std(msd_score_lung   ), ", min : ", np.min(msd_score_lung   ), ", max : ", np.max(msd_score_lung   ), " shape : ", msd_score_lung.shape    )
print("\n \n msd_score_heart   ; mean : ", np.mean(msd_score_heart  ), ", std : ", np.std(msd_score_heart  ), ", min : ", np.min(msd_score_heart  ), ", max : ", np.max(msd_score_heart  ), " shape : ", msd_score_heart.shape   )
