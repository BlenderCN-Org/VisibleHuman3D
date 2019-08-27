# -*- coding: utf-8 -*-
"""Spreadsheet Column Printer

This script allows the user to generate a 3D model of the wanted organ.

This tool accepts name of the organ given as string. 

This script requires that 'Segmentation', 'Visualization',  'DataManagement' and GlobalData be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * auto - generate the 3D model
"""
from Visualization import *
from Segmentation import *
from DataManagement import *

from GlobalData import getDSubstance

   
def auto(tiss,data="Female"):
    print('\n')
    segmentation, dico = getDSubstance(data,tiss)
    dicomdir = segmentation.dicomdir
    print('Dicom Dir : ', dicomdir)
    print('Initialize ImageDicom')
    image = segmentation.dicomimage
    if "box" in dico.keys():
        image.cropBoxImages(dico["box"]["dheight"],dico["box"]["drow"],dico["box"]["dcolumn"])
        segmentation.data_dico[segmentation.name]["box"]=dico["box"]
        print("height :", image.height)
    segmentation.pipeline()
    print('Initialize Visualization')
    myMesh = Visualization(segmentation)
    myMesh.pipeline()
    print('Object Created')
    print('----------')
    print('\n')
      


#auto('kidneyL')
#auto('kidneyR')
auto('liver')
#auto('lung')
#auto('heart')
#auto('abdo')
#auto('liver','Male')
#auto('bone')