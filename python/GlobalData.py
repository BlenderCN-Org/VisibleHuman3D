# -*- coding: utf-8 -*-
"""Data 

This script includes all the useful data. 

This script requires that 'Segmentation' and 'DataManagement' be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * getDSubstance - returns the dictionnary of the wanted sructure
    * getDico - return the full dictionnary
"""
import Segmentation
import DataManagement

DicomPath=r"..\data\DICOM"
ModelPath=r"..\data\Model"
TexturePath = r"..\data\Model\Material/"
ArrayPath = r"..\data/"

dataSubstance = {}

dataS={}
dataSF={}
dataSM={}

dataSF["Bones"]= {"structure":"bone", "dicomdir" : "Female", "box" : {"dheight":(0,1733),"drow":(5,505),"dcolumn":(0,510)},"threshold" :(600,3000), "color" :(241,214,145),"texture" :{"diffuse": "bone_diff.png", "normal":"bone_normal.png"}}
dataSF["Lung"]= {"structure":"lung", "dicomdir" : "Female", "box" : {"dheight":(1210,1455),"drow":(185,325),"dcolumn":(120,370)}, "threshold" :(-995,-145), "color" :(221,130,101),"texture" :{"diffuse": "lung_diff.png", "normal":"lung_normal.png"}}
dataSF["Heart"]= {"structure":"heart", "dicomdir" : "Female", "box" : {"dheight":(1250,1445),"drow":(198,305),"dcolumn":(210,365)}, "threshold" :(5,72), "color" :(192,104,88),"texture" :{"diffuse": "Heart_diffuse.jpg", "normal":"Heart_NormalMap.jpg"}}
dataSF["Liver"]= {"structure":"liver", "dicomdir" : "Female", "box" : {"dheight":(1105,1315),"drow":(150,365),"dcolumn":(110,325)}, "threshold" :(1, 50), "color" :(192,104,88),"texture" :{"diffuse": "liver_diff.png", "normal":"liver_normal.png"}}
dataSF["kidneyL"]= {"structure":"kidneyL", "dicomdir" : "Female", "box" : {"dheight":(1040,1175),"drow":(242,322),"dcolumn":(275,370)}, "threshold" :(5,65), "color" :(221,130,101),"texture" :{"diffuse": "kidney_diff.png", "normal":"kidney_normal.png"}}
dataSF["kidneyR"]= {"structure":"kidneyR", "dicomdir" : "Female", "box" : {"dheight":(1055,1180),"drow":(245,315),"dcolumn":(160,245)}, "threshold" :(5,65), "color" :(221,130,101),"texture" :{"diffuse": "kidney_diff.png", "normal":"kidney_normal.png"}}
dataSF["Kidneys"]= {"structure":"kidneyR", "dicomdir" : "Female", "box" : {"dheight":(1040,1180),"drow":(245,315),"dcolumn":(160,245)}, "threshold" :(5,65), "color" :(221,130,101),"texture" :{"diffuse": "kidney_diff.png", "normal":"kidney_normal.png"}}
dataSF["Abdo"]= {"structure":"abdo", "dicomdir" : "Female", "box" : {"dheight":(902,1395),"drow":(97,198),"dcolumn":(90,375)}, "threshold" :(0,45), "color" :(221,130,101),"texture" :{"diffuse": "abdo_diff.png", "normal":"abdo_normal.png"}}
dataSF["fat"]= {"structure":"fat", "dicomdir" : "Female","threshold" :(-150,-50), "color" :(230,220,70),"texture" :"fat.png"}
dataSF["muscle"]= {"structure":"muscle", "dicomdir" : "Female", "box" : {"dheight":(0,985),"drow":(95,415),"dcolumn":(40,500)}, "threshold" :(5,55), "color" :(221,130,101),"texture" :"muscle.png"}

dataSM["Bone"]= {"structure":"bone", "dicomdir" : "Male", "box" : {"dheight":(0,1733),"drow":(5,505),"dcolumn":(0,510)},"threshold" :(600,3000), "color" :(241,214,145),"texture" :{"diffuse": "bone_diff.png", "normal":"bone_normal.png"}}
dataSM["Lung"]= {"structure":"lung", "dicomdir" : "Male", "box" : {"dheight":(752,970),"drow":(165,358),"dcolumn":(119,394)}, "threshold" :(-995,-145), "color" :(221,130,101),"texture" :{"diffuse": "lung_diff.png", "normal":"lung_normal.png"}}
dataSM["Heart"]= {"structure":"heart", "dicomdir" : "Male", "box" : {"dheight":(774,945),"drow":(166,296),"dcolumn":(210,348)}, "threshold" :(5,72), "color" :(192,104,88),"texture" :{"diffuse": "Heart_diffuse.jpg", "normal":"Heart_NormalMap.jpg"}}
dataSM["Liver"]= {"structure":"liver", "dicomdir" : "Male", "box" : {"dheight":(610,830),"drow":(142,350),"dcolumn":(110,325)}, "threshold" :(5,75), "color" :(221,130,101),"texture" :{"diffuse": "liver_diff.png", "normal":"liver_normal.png"}}
dataSM["kidneyL"]= {"structure":"kidneyL", "dicomdir" : "Male", "box" : {"dheight":(595,713),"drow":(248,332),"dcolumn":(290,390)}, "threshold" :(5,65), "color" :(221,130,101),"texture" :{"diffuse": "kidney_diff.png", "normal":"kidney_normal.png"}}
dataSM["kidneyR"]= {"structure":"kidneyR", "dicomdir" : "Male", "box" : {"dheight":(575,700),"drow":(245,320),"dcolumn":(160,233)}, "threshold" :(5,65), "color" :(221,130,101),"texture" :{"diffuse": "kidney_diff.png", "normal":"kidney_normal.png"}}
dataSM["Kidneys"]= {"structure":"kidneys", "dicomdir" : "Male", "box" : {"dheight":(575,713),"drow":(245,315),"dcolumn":(160,245)}, "threshold" :(5,65), "color" :(221,130,101),"texture" :{"diffuse": "kidney_diff.png", "normal":"kidney_normal.png"}}
dataSM["Abdo"]= {"structure":"abdo", "dicomdir" : "Male", "box" : {"dheight":(525,970),"drow":(100,240),"dcolumn":(70,450)}, "threshold" :(0,45), "color" :(221,130,101),"texture" :{"diffuse": "abdo_diff.png", "normal":"abdo_normal.png"}}
dataSM["fat"]= {"structure":"fat", "dicomdir" : "Male","threshold" :(-150,-50), "color" :(230,220,70),"texture" :"fat.png"}
dataSM["muscle"]= {"structure":"muscle", "dicomdir" : "Male", "box" : {"dheight":(0,985),"drow":(95,415),"dcolumn":(40,500)}, "threshold" :(5,55), "color" :(221,130,101),"texture" :"muscle.png"}

dataS["Female"]= dataSF
dataS["Male"]= dataSM


def getDSubstance(data,elem):    
    if data in dataS.keys() : 
        if elem in dataS[data].keys() : 
            path = DicomPath + "/"+  dataS[data][elem]["dicomdir"]
            subs = Segmentation.Segmentation(dataS[data][elem]["structure"],data,path,DataManagement.DataManagement(path),dataS[data][elem]["threshold"],dataS[data][elem]["color"],dataS[data][elem]["texture"])
            subsDico =  dataS[data][elem]
    return subs, subsDico

def getDico():
    return dataS

def getArrayPath():
    return ArrayPath

def getDicomPath():
    return DicomPath

def getModelPath():
    return ModelPath

def getTexturePath():
    return TexturePath
