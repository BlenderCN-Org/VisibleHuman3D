"""Npy convertor

This script allows the user to load Dicom files and 
to save the pixaell array into a npy files 

This script requires that 'numpy', 'pydicom', 
and 'os' be installed within the Python environment 
you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * load_scan - load the dicoms and returns the pixel arrays
    * DelHeight - crop the array along the z axis
    * normalize_image - returns the normalized image
    * checkNAN - remove the NAN value from the image
    * preprocess_mask - clean the image
    * process_mask - save the clean images into a npy file
    * dicom_to_npy - load dicom and save the pixel arrays into a npy file
    * clean_mask - crop and process the image
    * clean_mask2 - crop and process the image
"""

import numpy as np
import pydicom as dicom
import os
import GlobalData

def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        
    return slices

def DelHeight(imgy,data_dico,tiss,data):
    mbox = (data_dico[tiss]["box"]["dheight"],data_dico[tiss]["box"]["drow"],data_dico[tiss]["box"]["dcolumn"])
    
    dh, dl, dc= mbox
    h1, h2 = dh
    l1, l2 = dl
    c1, c2 = dc
    
    shape = (l2-l1, c2-c1, h2-h1)
    print("\n \n h2-h1 :",h2-h1)
    ConstPixelDims = (512, 512, int( h2-h1))
    image_corr = np.zeros(ConstPixelDims, dtype=np.int16)
    
    k = 0
    for z in range(imgy.shape[0]):
        image = np.copy(imgy[z, :, :])
        for i in range(512):
            for j in range(512):
                if (z > h1 ) and (z < h2 ) :
                    image_corr[i][j][k] = image[i][j] 
                j += 1
            i += 1
        if (z > h1 ) and (z < h2 ) :
            k+=1
    
    if data == "Mimics":
        np.save( r"..\data\mask\Mimics/Eve_%s_%s_mask.npy" % (tiss,data), image_corr)
    else:
        np.save( r"..\data\mask\Deci/Eve_%s_%s_mask.npy" % (tiss,data), image_corr)
    
    return image_corr 

def normalize_image(img): 
    # Find the average pixel value near the lungs
    # to renormalize washed out images   
    mean = np.mean(img)
    std = np.std(img)
    img = img-mean
    if std != 0:
        img = img/std
    return img

def checkNAN(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] !=  img[i,j] :
                img[i,j]  = 0
    return img

def preprocess_mask(img):
    img   = checkNAN(img)
    img   = normalize_image(img)
    m = np.max(img)
    #if m == m and  m != 0 :
    if m != 0 :
        img[img<int(m)] = 0
        img = img/m
    return img.astype(np.int64)

def process_mask(tiss,data):

    if data == "Mimics":
        path =  r"..\data\mask\Mimics/Eve_%s_%s_mask.npy" % (tiss,data)
    else:
        path =  r"..\data\mask\Deci/Eve_%s_%s_mask.npy" % (tiss,data)
        
    imgy = np.load(path).astype(np.float64)
    
    print(path)
    
    image_corr = np.copy(imgy)

    for z in range(imgy.shape[2]):
        image_corr[:,:,z]   = preprocess_mask(image_corr[:,:,z])
    
    if data == "Mimics":
        np.save( r"..\data\mask\Mimics/Eve_%s_%s_mask.npy" % (tiss,data), image_corr)
    else:
        np.save( r"..\data\mask\Deci/Eve_%s_%s_mask.npy" % (tiss,data), image_corr)
    
    return image_corr

def dicom_to_npy(dir, mask_path):
    print("\n load")
    scan = load_scan(dir)
    print("\n numpy")
    numpy_scan = np.stack([s.pixel_array for s in scan ])
    np.save(mask_path  , numpy_scan)

def clean_mask(mask_path, structure, software):
    mask   =   np.load(mask_path).astype(np.float64)
    print("\n del")
    DelHeight(mask, GlobalData.getDico()["Female"], structure, software)
    print("\n process")
    process_mask(structure, software)

def clean_mask2(mask_path, structure, software):
    mask   =   np.load(mask_path).astype(np.float64)
    print("\n process")
    process_mask(structure, software)

mask_dir_path_Liver   =   r"E:\Model\DICOM\Deci_Bl\Liver/"
mask_dir_path_Lung    =   r"E:\Model\DICOM\Deci_Bl\Lung/"
mask_dir_path_Kidneys =   r"E:\Model\DICOM\Deci_Bl\Kidneys/"
mask_dir_path_Heart   =   r"E:\Model\DICOM\Deci_Bl\Heart/"


fily_Mimics_liver_mask   =r"..\data\mask\Mimics/Eve_Liver_Mimics_mask.npy"
fily_Mimics_lung_mask    =   r"..\data\mask\Mimics/Eve_Lung_Mimics_mask.npy"
fily_Mimics_kidneys_mask =r"..\data\mask\Mimics/Eve_Kidneys_Mimics_mask.npy"
fily_Mimics_heart_mask   =r"..\data\mask\Mimics/Eve_Heart_Mimics_mask.npy"


fily_Deci_Bl_liver_mask=   r"..\data\mask\Deci/Eve_Liver_Deci_Bl_mask.npy"
fily_Deci_Bl_lung_mask=     r"..\data\mask\Deci/Eve_Lung_Deci_Bl_mask.npy"
fily_Deci_Bl_kidneys_mask=    r"..\data\mask\Deci/Eve_Kidneys_Deci_Bl_mask.npy"
fily_Deci_Bl_heart_mask=   r"..\data\mask\Deci/Eve_Heart_Deci_Bl_mask.npy"

fily_Deci_ML_liver_mask=  r"..\data\mask\Deci/Eve_Liver_Deci_MeshLab_mask.npy"
fily_Deci_ML_lung_mask=   r"..\data\mask\Deci/Eve_Lung_Deci_MeshLab_mask.npy"
fily_Deci_ML_kidneys_mask=r"..\data\mask\Deci/Eve_Kidneys_Deci_MeshLab_mask.npy"
fily_Deci_ML_heart_mask=  r"..\data\mask\Deci/Eve_Heart_Deci_MeshLab_mask.npy"



dicom_to_npy(mask_dir_path_Liver,fily_Deci_Bl_liver_mask)
clean_mask(fily_Deci_Bl_liver_mask, "Liver",  "Deci_Bl")
dicom_to_npy(mask_dir_path_Heart,fily_Deci_ML_heart_mask)
clean_mask(fily_Deci_ML_heart_mask, "Heart",  "Deci_ML")
dicom_to_npy(mask_dir_path_Lung,fily_Deci_ML_lung_mask)
clean_mask(fily_Deci_ML_lung_mask, "Lung",  "Deci_ML")
dicom_to_npy(mask_dir_path_Kidneys,fily_Deci_ML_kidneys_mask)
clean_mask(fily_Deci_ML_kidneys_mask, "Kidneys",  "Deci_ML")
