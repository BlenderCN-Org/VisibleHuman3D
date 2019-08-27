# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 17:10:06 2018

@author: franc
"""
import pydicom as dicom
import os
import numpy

ArrayPath = r"..\data/"

class DataManagement:
    """
    A class used to create and load all informations needed 
    from the Dicom files
        

    Attributes
    ----------
    ConstPixelDims : tuple
        dimensions based on the number of rows, columns,
        and slices (along the Z axis)
    inDir : bool
        check whether the file is in the folder
    ArrayDicom : numpy array
        array of dicoms
    height : int
        length of the ArrayDicom
    row : int
        number of row of 1 slice of pixel_array
    columns : int
        number of columns of 1 slice of pixel_array
    RescaleSlope : float
        slope of the hounsfield transform
    RescaleIntercept : float
        intercept of the hounsfield transform
    dtype : numpy dtype
        type of the array
    image_Crop : numpy array
        array of all the scans
    modality : string
        modality of the scans


    Methods
    -------
    DelHeight(dheight) :  crop ArrayDicom along the z axis to focus on the organ of interest
    DelRow(drow) : erase the pixels out of the rows of interest
    DelColumn(dcolumn) : erase the pixels out of the columns of interest
    fileInDir(pfilename) : check whether the file is in the folder
    cropBoxImages(dheight,drow,dcolumn) : crop ArrayDicom to focus on the organ of interest

    """    
    
    def __init__(self,model):
        """
        Parameters
        ----------
        model : str
            path of the model's dicom
        """

        DicomPathModel = model+"/"
        lstFilesDCM = [] 
        for dirName, subdirList, fileList in os.walk(DicomPathModel):
            for filename in fileList:
                if ".dcm" or ".dc3" in filename.lower():  # check whether the file's DICOM
                    lstFilesDCM.append(os.path.join(dirName,filename))
		# Get ref file
        RefDs = dicom.read_file(lstFilesDCM[0])
        
        direction = numpy.cross(RefDs.ImageOrientationPatient[:3],RefDs.ImageOrientationPatient[3:])

		
		# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
        self.ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
		       
        self.inDir = self.fileInDir("FemaleArrayDicom.npy")
        if not self.inDir :  # check whether the file's DICOM
            print("preparing array")
            # The array is sized based on 'ConstPixelDims'
            self.ArrayDicom = numpy.zeros(self.ConstPixelDims,dtype=numpy.int16)
            ArrayIPP = []
            # loop through all the DICOM files
            for filenameDCM in lstFilesDCM: # read the file
                ds = dicom.read_file(filenameDCM)
                IPP=ds.ImagePositionPatient
                dIPP = direction * IPP
                # store the raw image data
                ArrayIPP.append((dIPP,ds))
                
            ArrayIPP.sort(key=lambda tup: tup[0][2])
            for i in range(len(ArrayIPP)-1):
                self.ArrayDicom[:, :, i] = ArrayIPP[i][1].pixel_array  

            numpy.save("Data/FemaleArrayDicom.npy", self.ArrayDicom)
        else:
            print("Array OK")
            file_Array_Dicom = ArrayPath + "FemaleArrayDicom.npy"                
            imgs_Array_Dicom = numpy.load(file_Array_Dicom).astype(numpy.int16) 
            self.ArrayDicom = imgs_Array_Dicom[:,:,:]

		#global variable to accelerate the global speed
        self.height=len(lstFilesDCM)
        self.rows=RefDs.Rows
        self.columns=RefDs.Columns
        if "RescaleSlope" in RefDs:
                    self.RescaleSlope=RefDs.RescaleSlope
                    self.RescaleIntercept=RefDs.RescaleIntercept
        self.dtype=RefDs.pixel_array.dtype
        self.image_Crop = self.ArrayDicom[:,:,:]
        self.modality = RefDs.Modality
        

    def DelHeight(self,dheight):
        """Prints what the animals name is and what sound it makes.

        Parameters
        ----------
        dheight : tuple
            The sound the animal makes (default is None)

        Returns
        -------
        numpy array
            If no sound is set for the animal or passed in as a
            parameter.
        """
        h_min, h_max = dheight
        self.ConstPixelDims = (int(self.rows), int(self.columns), int(h_max - h_min))
        image_corr = numpy.zeros(self.ConstPixelDims, self.dtype)
        k = 0
        for z in range(self.height):
            image = numpy.copy(self.ArrayDicom[:, :, z])
            for i in range(self.rows):
                for j in range(self.columns):
                    if (z > h_min ) and (z < h_max ) :
                        image_corr[i][j][k] = image[i][j]
                    j += 1
                i += 1
            if (z > h_min ) and (z < h_max ) :
                k+=1
        self.height = int(h_max - h_min)
        self.image_Crop = image_corr
        return image_corr 	
    
    def DelRow(self,drow):
        pix_min, pix_max = drow
        image = numpy.copy(self.image_Crop[:, :, :])
        for z in range(self.height):            
            for i in range(self.rows):
                for j in range(self.columns):
                    if (i > pix_max ) or (i < pix_min ) :
                        image[i][j][z]= 0
                    j += 1
                i += 1
        self.image_Crop = image
        return image 
    
    def DelColumn(self,dcolumn):
        pix_min, pix_max = dcolumn
        image = numpy.copy(self.image_Crop[:, :, :])
        for z in range(self.height): 
            for i in range(self.rows):
                for j in range(self.columns):
                    if (j > pix_max ) or (j < pix_min ) :
                        image[i][j][z] = 0
                    j += 1
                i += 1
        self.image_Crop = image
        return image
		
    def fileInDir(self,pfilename):
        results = []
        result = False
        for dirName, subdirList, fileList in os.walk(ArrayPath):
            for filename in fileList:
                if not pfilename in filename : 
                    results.append(False)
                else :
                    results.append(True)
        results.sort()
        for b in results:
            if b == True:
                result = b
        return result
	
    def cropBoxImages(self,dheight,drow,dcolumn):
        print('DelHeight start')
        self.DelHeight(dheight)
        print('DelRow start')
        self.DelRow(drow)
        print('DelColum start')
        self.DelColumn(dcolumn)
        print('Delpix ok')
        