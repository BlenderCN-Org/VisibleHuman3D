# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 16:42:23 2018

@author: franc
"""
import numpy
import pydicom as pydcm
import os

import scipy.ndimage

from skimage import morphology
from skimage import measure
from skimage import filters
from skimage import feature

from skimage.draw import rectangle
from skimage.draw import line_aa

from skimage.transform import resize

from skimage.filters.rank import gradient 
from skimage.filters import median

from skimage.restoration import (denoise_tv_chambolle, denoise_bilateral, denoise_wavelet, estimate_sigma)

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

ArrayPath = r"..\data/"

class Segmentation:
    """
    A class used to segment the images

    ...

    Attributes
    ----------
    name : str
        name of the data set and structur to be segmented
    structure : str
        name of the structur to be segmented
    data : str 
        name of the data set used
    dicomdir : str 
        path to the dicoms
    threshold : tuple 
        threshold used for the segementation
    color : tuple
        color used for the shading
    texture : png
        image use for the texture
    data_dico : dictionary
        dictionnary complited with all the above information
    dicomimage : DataManagement
    mask : numpy array
        array of the masks used for the segmentation
    image_Hounsfield : numpy array
        array of the images after the Hounsfield transform
    image_Threshold : numpy array
        array of the images after the thresholding

    Methods
    -------
    ArrayHounsfield() : make the conversion to Hounsfield Unit
    Threshold(image) : apply the segmentation to the images
    getThreshold() : return the trheshold as a string
    filterInvs(nd) : return the invers image of a binary image
    normalize_image(img) : normalize the image
    preprocess(img) : clean the image by deleting useless information
    Make_mask() : make the masks 
    pipeline() : complete pipeline to do the segmentation

    """ 

    def __init__(self,structure,bd,dicomdir,dicomimage,threshold,color,texture):
        ''' This function allows us to create and load all informations needed from the Dicom files'''
        self.name = bd + "_"+ structure
        self.structure = structure
        self.data = bd
        self.dicomdir = dicomdir
        self.threshold = threshold
        self.color = color
        self.texture = texture
        self.dicomimage = dicomimage
        data_dico = {}
        data_dico[self.name]= {"bd":bd, "structure":structure,"dicomdir" : dicomdir, "threshold" :threshold, "color" :color,"texture" :texture}
        self.data_dico = data_dico
        self.mask = []


    def ArrayHounsfield(self):
        '''The Dicom files don't register the density in Hounsfield Units, this function make the conversion '''
        image_hu = numpy.zeros(self.dicomimage.ConstPixelDims, self.dicomimage.dtype)

        for z in range(self.dicomimage.height): 
            image =  self.dicomimage.image_Crop[:, :, z] #.astype(numpy.int16)
            for i in range(self.dicomimage.rows):
                for j in range(self.dicomimage.columns):
                    image_hu[i][j][z] = image[i][j] * int(self.dicomimage.RescaleSlope) + int(self.dicomimage.RescaleIntercept)
                    j += 1
                i += 1
        self.image_Hounsfield = numpy.array(image_hu, dtype=numpy.int16) 
        numpy.save("..\data\mask\segmentation/%s_hounsfield.npy" % (self.name), self.image_Hounsfield)
        return image_hu
            
    def Threshold(self,image):
        '''This function receive the image and the dimensions of the image, a low threshold and a upper threshold. 
        It returns the image segmented'''
        th_low,th_high = self.threshold
        image_Threshold = numpy.zeros(self.dicomimage.ConstPixelDims, self.dicomimage.dtype)
        for i in range(self.dicomimage.rows):
            for j in range(self.dicomimage.columns):
                for z in range(self.dicomimage.height):
                    if (image[i][j][z] >=th_low )and (image[i,j,z] <=th_high ) :
                        image_Threshold[i][j][z] = 1
                    else:
                        image_Threshold[i][j][z] = 0
                    z += 1
                j += 1
        i += 1
        self.image_Threshold = image_Threshold
        numpy.save("..\data\mask\segmentation/%s_threshold_%s.npy" % (self.name, self.getThreshold()), self.image_Threshold)
        return image_Threshold       
    
    def getThreshold(self):
        thresh=str(self.threshold[0]) +"-" +  str(self.threshold[1])
        return thresh
            
    def filterInvs(self,nd):
        image = numpy.zeros((len(nd),len(nd[0])), dtype=numpy.float64)
        for i in range(len(nd)):
            for j in range(len(nd[0])):
                if nd[i][j] == 0:
                    image[i][j]=1.0
                elif nd[i][j] == 1:
                    image[i][j]=0.0
        return numpy.array(image, dtype=numpy.float64) 

    def normalize_image(self,img):  
        mean = numpy.mean(img)            
        std = numpy.std(img)      
        img = img-mean
        
        if not std == 0.0:   
            img = img/std 
        return img
    
    def preprocess(self,img):
        img[img>500] = 0
        img[img<-100] = 0
        img   = numpy.clip(img, -50, 300)    
        img   = self.normalize_image(img)
        return img

    def DelRow(self,my_img,my_rows):
        pix_min, pix_max = my_rows
        image = numpy.copy(my_img[:, :])
        for i in range(my_img.shape[0]):
            for j in range(my_img.shape[1]):
                if (i > pix_max ) or (i < pix_min ) :
                    image[i][j] = 0
                j += 1
            i += 1
        return image 

    def DelColumn(self,my_img,my_columns):
        pix_min, pix_max = my_columns
        image = numpy.copy(my_img[:, :])
        for i in range(my_img.shape[0]):
            for j in range(my_img.shape[1]):
                if (j > pix_max ) or (j < pix_min ) :
                    image[i][j] = 0
                j += 1
            i += 1
        return image 
    
    def clean_Lung(self,igy, my_rows = (190,321), my_columns = (125,368)):    
        lung_mask = self.DelRow(igy,my_rows)
        lung_mask = self.DelColumn(lung_mask,my_columns)
        return lung_mask
    
    def Make_mask(self):
        
        lst_img = self.image_Hounsfield

        tiss = self.name
        
        mbox = (self.data_dico[tiss]["box"]["dheight"],self.data_dico[tiss]["box"]["drow"],self.data_dico[tiss]["box"]["dcolumn"])
        dh, dl, dc= mbox
        l1, l2 = dl
        c1, c2 = dc

        mask_array = numpy.zeros(self.dicomimage.ConstPixelDims,dtype=numpy.int16)
        noisy_array = numpy.zeros(self.dicomimage.ConstPixelDims,dtype=numpy.int16)
        
        row_size = lst_img.shape[0]
        col_size = lst_img.shape[1]
        
        if tiss == self.data_dico[tiss]["bd"] + "_Lung":

            for z in range (self.dicomimage.height):
                
                img  = numpy.copy(lst_img[:,:,z])                                

                img_2 = numpy.copy(img)
                img_n = numpy.copy(filters.gaussian(img_2, sigma=2, preserve_range=True))
           
                            
                middle = img[l1:l2,c1:c2] 
                
                mean = numpy.mean(middle)  
                max = numpy.max(middle)
                min = numpy.min(middle)

                # To improve threshold finding, I'm moving the underflow and overflow on the pixel spectrum
                img[img==max]=mean
                img[img==min]=mean
                
                # Using Kmeans to separate foreground (soft tissue / bone) and background (lung/air)
                                
                X = numpy.reshape(middle,[numpy.prod(middle.shape),1])
                clf = KMeans(n_clusters=4)
                clf.fit(X)
                
                centers = sorted(clf.cluster_centers_.flatten())
                threshold = numpy.mean(numpy.min(centers))
                thresh_img = numpy.where(img<threshold, 1.0, 0.0) 

                # First erode away the finer elements, then dilate to include some of the pixels surrounding the lung.  
                # We don't want to accidentally clip the lung.

                edges2 = feature.canny(img, sigma=3) 
                edges2 = morphology.dilation(edges2,numpy.ones([6,6]))
                edges2 = morphology.erosion(edges2,numpy.ones([3,3]))
                edges2 = morphology.closing(edges2,numpy.ones([3,3]))
                edges2Inv = self.filterInvs(edges2)

                edges3 = feature.canny(img, sigma=8) 
                edges3 = morphology.dilation(edges3,numpy.ones([6,6]))
                edges3 = self.filterInvs(edges3)

                eroded = morphology.erosion(thresh_img,numpy.ones([2,2]))
                dilation = morphology.dilation(eroded,numpy.ones([10,10]))
                        
                labels = measure.label(dilation) # Different labels are displayed in different colors
                label_vals = numpy.unique(labels)
                regions = measure.regionprops(labels)
                good_labels = []
                bad_labels = []
                
                for prop in regions:
                    B = prop.bbox #= (min_row, min_col, max_row, max_col)        
                    minr, minc, maxr, maxc = B                 
                    if B[2]-B[0]<row_size/10*9 and B[3]-B[1]<col_size/10*9 and B[0]>row_size/5 and B[2]<col_size/5*4: #if  B[2]-B[0]>= (l2 -l1)/2 and B[3]-B[1]>= (c2 -c1)/2 and B[2] <= l2 : # and B[3] <= c2 :
                        good_labels.append(prop.label)
                    elif  B[2]-B[0]< (l2 -l1) and B[3]-B[1]< (c2 -c1) and B[2] < l2 * 8/10  and B[3] < c2 * 8/10 and B[0] > l1 and B[1] >= c1 :
                        good_labels.append(prop.label)
                    else :
                        good_labels.append(prop.label)
                        
                mask = numpy.ndarray([row_size,col_size],dtype=numpy.int8)
                mask[:] = 0
                
                #  After just the lungs are left, we do another large dilation
                #  in order to fill in and out the lung mask 
                
                for N in good_labels:
                    mask = mask + numpy.where(labels==N,1,0)
                mask = morphology.dilation(mask,numpy.ones([10,10])) # one last dilation
                
                final_mask_z = mask * edges3

                final_mask_z = self.clean_Lung(final_mask_z)
                              
                for i in range(self.dicomimage.rows):
                    for j in range(self.dicomimage.columns):
                        mask_array[i,j,z]= final_mask_z[i,j]
                        noisy_array[i,j,z]= img_n[i,j]
            
        elif tiss == self.data_dico[tiss]["bd"] + "_Heart":
        
            for z in range (self.dicomimage.height):
                
                img  = numpy.copy(lst_img[:,:,z])   

                img_2 = numpy.copy(img)
                img_b = numpy.copy(filters.gaussian(img_2, sigma=5, preserve_range=True))
                img_n = numpy.copy(self.preprocess(img_b))
                       
                img = self.preprocess(img)

                middle = img[l1:l2,c1:c2] 
                
                mean = numpy.mean(middle)  
                max = numpy.max(middle)
                min = numpy.min(middle)

                minx = numpy.min(img, axis = 0)
                minx_ = int(numpy.mean(minx))
                
                img[img==max]=mean
                img[img==min]=mean

                edges2 = feature.canny(img, sigma=4) 
                edges2 = morphology.dilation(edges2,numpy.ones([9,9]))
                edges2 = morphology.closing(edges2,numpy.ones([3,3]))
                edges2 = morphology.erosion(edges2,numpy.ones([5,5]))

                edges2Inv = self.filterInvs(edges2)

                edges3 = feature.canny(img, sigma=9) 
                edges3 = morphology.dilation(edges3,numpy.ones([3,3]))
                edges3 = morphology.closing(edges3,numpy.ones([6,6]))
                edges3 = morphology.dilation(edges3,numpy.ones([3,3]))
                edges3 = self.filterInvs(edges3)
                edges3 = morphology.opening(edges3,numpy.ones([3,3]))

                X = numpy.reshape(middle,[numpy.prod(middle.shape),1])
                clf = KMeans(n_clusters=8)
                clf.fit(X)
                
                centers = sorted(clf.cluster_centers_.flatten())
                threshold = numpy.mean(numpy.min(centers))
                thresh_img = numpy.where(img>threshold, 1.0, 0.0) 

                dilation = morphology.dilation(thresh_img,numpy.ones([10,10]))
                eroded = morphology.erosion(dilation,numpy.ones([5,5]))
                dilation *= edges2Inv

                inv = self.filterInvs(dilation)

                labels = measure.label(dilation, connectivity=2) # Different labels are displayed in different colors , neighbors=None, background=None, return_num=False, connectivity=None
                label_vals = numpy.unique(labels)
                regions = measure.regionprops(labels)
                good_labels = []
                bad_labels = []
                for prop in regions:
                    B = prop.bbox #= (min_row, min_col, max_row, max_col)
                    minr, minc, maxr, maxc = B
                    
                    if  B[2]-B[0]< (l2 -l1) and B[3]-B[1]< (c2 -c1) and B[2] < l2 * 9/10  and B[3] < c2 * 11/10 and B[0] > l1 * 12/10 and B[1] > c1 * 14/10 :
                        good_labels.append(prop.label)
                    else :
                        good_labels.append(prop.label)
                        
                mask = numpy.ndarray([row_size,col_size],dtype=numpy.int8)
                mask[:] = 0

                for N in good_labels:
                    mask = mask + numpy.where(labels==N,1,0)
                mask = morphology.dilation(mask,numpy.ones([10,10])) # one last dilation
                mask = morphology.closing(mask,numpy.ones([4,4])) #
                
                final_mask_z = mask 
                                
                for i in range(self.dicomimage.rows):
                    for j in range(self.dicomimage.columns):
                        mask_array[i,j,z]= final_mask_z[i,j]
                        noisy_array[i,j,z]= img_n[i,j]

        elif tiss == self.data_dico[tiss]["bd"] + "_Liver":
            
            for z in range (self.dicomimage.height):
                
                img  = numpy.copy(lst_img[:,:,z])

                            
                img_2 = numpy.copy(img)
                img_b=filters.gaussian(img_2, sigma=5, preserve_range=True)
                img_b2 = numpy.copy(img_b)
                img_c = self.preprocess(img_b2)
                img_c2 = numpy.copy(img_c)
                img_n   = self.normalize_image(img_c2)
                
                img = self.preprocess(img)

                middle = img[l1:l2,c1:c2] 
                
                mean = numpy.mean(middle)  
                max = numpy.max(middle)
                min = numpy.min(middle)

                minx = numpy.min(img, axis = 0)
                minx_ = int(numpy.mean(minx)) 
                
                img[img==max]=mean
                img[img==min]=mean
                                
                edges2 = feature.canny(img_b, sigma=6) 
                edges2 = morphology.dilation(edges2,numpy.ones([7,7]))
                edges2 = morphology.erosion(edges2,numpy.ones([4,4]))
                edges2 = morphology.closing(edges2,numpy.ones([3,3]))

                edges2Inv = self.filterInvs(edges2)

                edges3 = feature.canny(img_b, sigma=6) 
                edges3 = morphology.dilation(edges3,numpy.ones([8,8]))
                edges3 = morphology.erosion(edges3,numpy.ones([4,4]))
                edges3 = morphology.closing(edges3,numpy.ones([6,6]))
                edges3 = self.filterInvs(edges3)

                X = numpy.reshape(middle,[numpy.prod(middle.shape),1])
                clf = KMeans(n_clusters=4)
                clf.fit(X)
                
                centers = sorted(clf.cluster_centers_.flatten())
                threshold = numpy.mean(numpy.min(centers))
                thresh_img = numpy.where(img>threshold, 1.0, 0.0) 

                eroded = morphology.erosion(thresh_img,numpy.ones([9,9]))
                dilation = morphology.dilation(eroded,numpy.ones([6,6]))
                dilation[:,int(c2*6/10):] = morphology.opening(dilation[:,int(c2*6/10):],numpy.ones([15,15]))
                dilation[:,:int(c2*6/10)] = morphology.dilation(dilation[:,:int(c2*6/10)],numpy.ones([11,11]))
                dilation *= edges2Inv

                inv = self.filterInvs(dilation)

                labels = measure.label(dilation, background=minx_) # Different labels are displayed in different colors , neighbors=None, background=None, return_num=False, connectivity=None
                label_vals = numpy.unique(labels)
                regions = measure.regionprops(labels)
                good_labels = []
                bad_labels = []

                for prop in regions:
                    B = prop.bbox #= (min_row, min_col, max_row, max_col)        
                    if  B[2]-B[0]>= (l2 -l1)/2 and B[3]-B[1]>= (c2 -c1)/2 and B[0] > l1 * 2/10 and B[2] < l2 * 12/10 and B[1]> c1 * 8/10:
                        good_labels.append(prop.label)
                    elif  B[2]-B[0]< (l2 -l1) and B[3]-B[1]< (c2 -c1) and B[2] <= l2 and B[1] > c1 and B[0]> l1 * 8/10 :
                        good_labels.append(prop.label)
                    else :
                        good_labels.append(prop.label)
                mask = numpy.ndarray([row_size,col_size],dtype=numpy.int8)
                mask[:] = 0

                for N in good_labels:
                    mask = mask + numpy.where(labels==N,1,0)
                mask = morphology.dilation(mask,numpy.ones([3,3])) # one last dilation
                mask[:,:int(c2*8/10)] = morphology.dilation(mask[:,:int(c2*8/10)],numpy.ones([6,6]))


                final_mask_z = numpy.copy(mask*edges3)
                
                for i in range(self.dicomimage.rows):
                    for j in range(self.dicomimage.columns):
                        mask_array[i][j][z]= final_mask_z[i][j]
                        noisy_array[i][j][z]= img_n[i][j]

        elif tiss ==  self.data_dico[tiss]["bd"] + "_kidneyR":
        
            for z in range (self.dicomimage.height):
                
                img  = numpy.copy(lst_img[:,:,z])
                
                img_2 = numpy.copy(img)
                img_b = numpy.copy(filters.gaussian(img_2, sigma=2, preserve_range=True))
                img_n = numpy.copy(self.preprocess(img_b))
                
                img = self.preprocess(img)
                
                middle = img[l1:l2,c1:c2] 
                
                mean = numpy.mean(middle)  
                max = numpy.max(middle)
                min = numpy.min(middle)

                minx = numpy.min(img, axis = 0)
                minx_ = int(numpy.mean(minx))
                
                # To improve threshold finding, I'm moving the underflow and overflow on the pixel spectrum
                img[img==max]=mean
                img[img==min]=mean
                
                edges2 = feature.canny(img, sigma=6) 
                edges2 = morphology.dilation(edges2,numpy.ones([7,7]))
                edges2 = morphology.closing(edges2,numpy.ones([3,3]))
                edges2 = morphology.dilation(edges2,numpy.ones([7,7]))

                edges2Inv = self.filterInvs(edges2)

                edges3 = feature.canny(img, sigma=6) 
                edges3 = morphology.dilation(edges3,numpy.ones([5,5]))
                edges3 = morphology.closing(edges3,numpy.ones([6,6]))
                edges3 = self.filterInvs(edges3)
                edges3 = morphology.closing(edges3,numpy.ones([3,3]))
                edges3 = morphology.dilation(edges3,numpy.ones([5,5]))
                
                X = numpy.reshape(middle,[numpy.prod(middle.shape),1])
                clf = KMeans(n_clusters=4)
                clf.fit(X)
                
                centers = sorted(clf.cluster_centers_.flatten())
                threshold = numpy.mean(numpy.min(centers))
                thresh_img = numpy.where(img>threshold, 1.0, 0.0) 

                eroded = morphology.erosion(thresh_img,numpy.ones([5,5]))
                dilation = morphology.dilation(eroded,numpy.ones([6,6]))
                dilation *= edges2Inv

                inv = self.filterInvs(dilation)

                labels = measure.label(dilation, background=minx_) # Different labels are displayed in different colors , neighbors=None, background=None, return_num=False, connectivity=None
                label_vals = numpy.unique(labels)
                regions = measure.regionprops(labels)
                good_labels = []
                bad_labels = []
                
                for prop in regions:
                    B = prop.bbox #= (min_row, min_col, max_row, max_col)
                    minr, minc, maxr, maxc = B
                    
                    if  B[2]-B[0]< (l2 -l1) and B[3]-B[1]< (c2 -c1) and B[2] < l2  and B[3] < c2 * 8/10  and B[0] > l1 and B[1] >= c1 * 8/10 :
                        good_labels.append(prop.label)
                    elif  B[2]-B[0]> (l2 -l1) and B[3]-B[1]> (c2 -c1) and B[0] > l1 * 2/10  :
                        good_labels.append(prop.label)
                    else :
                        good_labels.append(prop.label)

                        
                mask = numpy.ndarray([row_size,col_size],dtype=numpy.int8)
                mask[:] = 0

                for N in good_labels:
                    mask = mask + numpy.where(labels==N,1,0)
                mask = morphology.dilation(mask,numpy.ones([10,10])) 
                
                final_mask_z = mask

                for i in range(self.dicomimage.rows):
                    for j in range(self.dicomimage.columns):
                        mask_array[i,j,z]= final_mask_z[i,j]
                        noisy_array[i,j,z]= img_n[i,j]

        elif tiss == self.data_dico[tiss]["bd"] + "_kidneyL" :
    
            for z in range (self.dicomimage.height):
                
                img  = numpy.copy(lst_img[:,:,z]) 

                img_2 = numpy.copy(img)
                img_b = numpy.copy(filters.gaussian(img_2, sigma=5, preserve_range=True))
                img_n = numpy.copy(self.preprocess(img_b))
                
                img = self.preprocess(img)

                middle = img[l1:l2,c1:c2] 
                
                minx = numpy.min(img, axis = 0)
                minx_ = int(numpy.mean(minx))
                
                img[img==max]=mean
                img[img==min]=mean
                
                X = numpy.reshape(middle,[numpy.prod(middle.shape),1])
                clf = KMeans(n_clusters=4)
                clf.fit(X)
                
                centers = sorted(clf.cluster_centers_.flatten())
                threshold = numpy.mean(numpy.min(centers))
                thresh_img = numpy.where(img>threshold, 1.0, 0.0) 
                
                edges2 = feature.canny(img, sigma=6) 
                edges2 = morphology.dilation(edges2,numpy.ones([7,7]))
                edges2 = morphology.erosion(edges2,numpy.ones([4,4]))
                edges2 = morphology.closing(edges2,numpy.ones([3,3]))
                edges2Inv = self.filterInvs(edges2)

                edges3 = feature.canny(img, sigma=6) 
                edges3 = morphology.dilation(edges3,numpy.ones([5,5]))
                edges3 = morphology.closing(edges3,numpy.ones([6,6]))
                edges3 = self.filterInvs(edges3)
                edges3 = morphology.closing(edges3,numpy.ones([3,3]))
                edges3 = morphology.dilation(edges3,numpy.ones([5,5]))

                eroded = morphology.erosion(thresh_img,numpy.ones([5,5]))
                dilation = morphology.dilation(eroded,numpy.ones([6,6]))
                dilation *= edges2Inv

                labels = measure.label(dilation, background=minx_) # Different labels are displayed in different colors , neighbors=None, background=None, return_num=False, connectivity=None
                label_vals = numpy.unique(labels)
                regions = measure.regionprops(labels)
                good_labels = []

                
                for prop in regions:
                    B = prop.bbox #= (min_row, min_col, max_row, max_col)            
                    if  B[2]-B[0]>= (l2 -l1)/2 and B[3]-B[1]>= (c2 -c1)/2 and B[2] <= l2 and B[1] > c1 :
                        good_labels.append(prop.label)
                    elif  B[2]-B[0]> (l2 -l1) and B[3]-B[1]> (c2 -c1) and B[0] > l1 * 2/10  :
                        good_labels.append(prop.label)
                    else :
                        good_labels.append(prop.label)

                mask = numpy.ndarray([row_size,col_size],dtype=numpy.int8)
                mask[:] = 0
                
                for N in good_labels:
                    mask = mask + numpy.where(labels==N,1,0)
                mask = morphology.dilation(mask,numpy.ones([10,10])) # one last dilation

                final_mask_z = mask*edges3

                for i in range(self.dicomimage.rows):
                    for j in range(self.dicomimage.columns):
                        mask_array[i,j,z]= final_mask_z[i,j]
                        noisy_array[i,j,z]= img_n[i,j]

        self.mask = mask_array
        self.noisy = noisy_array

        numpy.save("..\data\mask\segmentation/%s_mask.npy" % (self.name), self.mask)

        return mask_array

    def pipeline(self):
        #Sub=Substance(name,dicomdir,dicomimage,threshold,color,texture)
        #image_hu = self.dicomimage.image_Hounsfield # image_Hounsfield        
        if self.dicomimage.modality == "CT":
            print("CT")
            self.inDir = self.dicomimage.fileInDir("..\data\mask\segmentation/%s_hounsfield.npy" % (self.name))
            if not self.inDir :  # check whether the file's DICOM
                print('Start ArrayHounsfield')
                self.ArrayHounsfield()
                print('End ArrayHounsfield')
            else:                        
                print("Hounsfield OK")
                file_Array_Hounsfield = "..\data\mask\segmentation/%s_hounsfield.npy" % (self.name)           
                imgs_Array_Hounsfield = numpy.load(file_Array_Hounsfield).astype( self.dicomimage.dtype) 
                self.image_Hounsfield = imgs_Array_Hounsfield[:,:,:]
            
            print('Start Mask')
            self.Make_mask()

            if len(self.mask) != 0:
                #nv_hd = numpy.multiply(self.mask, filters.gaussian(self.image_Hounsfield, sigma=4, preserve_range=True))
                nv_hd = numpy.multiply(self.mask, self.noisy)
                print('End Mask')
                print('Start Threshold')
                self.Threshold(nv_hd)
                #self.KmeanSegmentation(self.image_Hounsfield)
                print('End Threshold')
            else:
                print('Start Threshold')
                self.Threshold(filters.gaussian(self.image_Hounsfield, sigma=1, preserve_range=True))
                #self.KmeanSegmentation(self.image_Hounsfield)
                print('End Threshold')

        
        elif self.dicomimage.modality == "MR":
            print("MRI")
            print('Start Threshold')
            self.Threshold(self.dicomimage.image_Crop)
            print('End Threshold')
        
        else :
            print("Only CT and MRI are compatible")        
        print('Start Filling')
        #self.Filling()
        print('End Filling')

