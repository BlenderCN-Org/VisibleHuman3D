# -*- coding: utf-8 -*-
"""
    Created on Mon Sep 17 13:44:19 2018
    
    @author: franc
"""

import bpy 
import mcubes

from CGAL import CGAL_Polygon_mesh_processing
from CGAL import CGAL_Polyhedron_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3


import trimesh

from skimage.measure import marching_cubes_lewiner, mesh_surface_area

from collada import *
from DataManagement import *
import GlobalData

class Visualization:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    segmentation : Segmentation
    image : DataManagement
    extention : str
        3D model extention file
    name : str
        name of the 3D model
    vertices :  numpy array
        array of all the vertices of the model
    triangles : numpy array
        array of all the triangles of the model
    factor : float
        Controls the smoothing amount
    iterations : float
        The number of smoothing iterations
    cleanratio : float
        The ratio of faces to keep after decimation


    Methods
    -------
    Smooth(pfactor, piterations) : apply a smooth to the model
    cleanAllDecimateModifiers(id, decimateRatio= 0.1) : reduce the number of faces of the model
    right_rbg(color) : convert rgb color from [0,255] to [0,1] 
    AddTexture() : apply texture to the model
    GenerateTangentsBitangenats() : calculate tangent and bitangents
    pipeline(pfactor= 0.9, piterations = 30) : complete pipeline for the visualization class

    
    """    
        
    def __init__(self,segmentation, mtype="DAE"):
        self.segmentation = segmentation
        self.image = segmentation.dicomimage
        threshold=segmentation.getThreshold()
        if mtype.lower() == "collada" or mtype.lower() == "dae":
            self.extention=".dae"
            self.name = segmentation.name +"_" + mtype+ "_Tresh-" + threshold
            self.vertices, self.triangles = mcubes.marching_cubes(self.segmentation.image_Threshold, 0)
            mcubes.export_mesh(self.vertices, self.triangles, GlobalData.ModelPath + "/"  +self.name + self.extention, self.name)
        if mtype.lower() == "stl":
            self.extention=".stl"
            self.name = segmentation.name + "_" + mtype +"_Tresh-" + threshold
            self.vertices, self.triangles = mcubes.marching_cubes(self.segmentation.image_Threshold, 0)
            mcubes.export_mesh(self.vertices, self.triangles, GlobalData.ModelPath + "/"  +self.name + self.extention, self.name)
        daepath = GlobalData.ModelPath + "/" + self.name
        self.name = daepath  
    
    def Smooth(self, pfactor, piterations):
        self.factor = pfactor
        self.iterations = piterations
                                
        filepath_in = self.name + self.extention 
        a = self.name + "_Smooth"
        self.name = a
        filepath_out = self.name + self.extention 

        if self.extention == ".dae":        
            bpy.ops.wm.collada_import(filepath=filepath_in)           
            bpy.ops.object.modifier_add(type="SMOOTH")
            bpy.context.object.modifiers["Smooth"].factor = self.factor
            bpy.context.object.modifiers["Smooth"].iterations = self.iterations 
            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=True, use_object_instantiation=True, sort_by_name=False)
        else:
            bpy.ops.import_mesh.stl(filepath=filepath_in)
            bpy.ops.object.modifier_add(type="SMOOTH")
            bpy.context.object.modifiers["Smooth"].factor = self.factor
            bpy.context.object.modifiers["Smooth"].iterations = self.iterations
            
            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=True, use_object_instantiation=True, sort_by_name=False)
        
    def cleanAllDecimateModifiers(self, id, decimateRatio= 0.1):
        """ Cleans all decimate modifiers"""
        
        self.cleanratio = decimateRatio            
        
        filepath_in = self.name + self.extention 
        a = self.name +"_Decimate_%d" %(id) 
        self.name = a
        filepath_out = self.name + self.extention
        
        if self.extention == ".dae":   

            bpy.ops.wm.collada_import(filepath=filepath_in) 
                            
            bpy.ops.object.modifier_add(type="DECIMATE")
            bpy.context.object.modifiers["Decimate"].decimate_type = "COLLAPSE"
            bpy.context.object.modifiers["Decimate"].ratio = self.cleanratio
            #bpy.context.object.modifiers["Decimate"].iterations = self.cleanterations
            #bpy.context.object.modifiers["Decimate"].use_collapse_triangulate=True
            #bpy.context.object.modifiers["Decimate"].delimit = {"NORMAL"}       
            
            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=False, use_object_instantiation=True, sort_by_name=False)

        else:
            
            bpy.ops.import_scene.obj(filepath=filepath_in)
            bpy.ops.object.modifier_add(type="DECIMATE")
            bpy.context.object.modifiers["Decimate"].decimate_type = "COLLAPSE"
            bpy.context.object.modifiers["Decimate"].ratio = self.cleanratio

            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=True, use_object_instantiation=True, sort_by_name=False)
    
    def right_rbg(self,color):
        div = 255
        r = color[0]/div
        g = color[1]/div
        b = color[2]/div
        return (r,g,b)
            
    def AddTexture(self):
        
        color = self.segmentation.color
        (r,g,b) = self.right_rbg(color) 

        ipath_diff = self.segmentation.texture["diffuse"]
        imagePath_diff = GlobalData.TexturePath + ipath_diff

        ipath_normal = self.segmentation.texture["normal"]      
        imagePath_normal = GlobalData.TexturePath + ipath_normal
        
                    
        # used names
        matName = "mat_"+ self.segmentation.name
        textName = self.segmentation.name

        filepath_in = self.name + self.extention 
        a = self.name +"_Texture_UV_CUBE_Added" 
        self.name = a
        filepath_out = self.name + self.extention

        if self.extention == ".dae": 
            bpy.ops.wm.collada_import(filepath=filepath_in)
            
            #if not matName in bpy.data.materials:
            mat = bpy.data.materials.new(matName)
            mat.diffuse_color = (r,g,b)
            
            bpy.context.object.data.materials.append(mat)
            
            #UV Map
            UVMapName = textName + "_UVMap"
            #[o.data.uv_textures.new(UVMapName) for o in bpy.context.object
            #                        if o.type == 'MESH']
            if bpy.context.object.type == 'MESH':
                bpy.context.object.data.uv_textures.new(UVMapName)
        
            #Diffuse
            texName_diff = textName + "_diff"
            tex_diff = bpy.data.textures.new(texName_diff, type="IMAGE")            
            image_diff = bpy.data.images.load(imagePath_diff)
            tex_diff.image = image_diff
                
            bpy.data.materials[matName].texture_slots.add().texture = tex_diff  
            bpy.data.materials[matName].texture_slots[0].texture =  bpy.data.textures[texName_diff]  
            bpy.data.materials[matName].texture_slots[0].uv_layer = UVMapName
            bpy.data.materials[matName].texture_slots[0].use_map_color_diffuse = True
            bpy.data.materials[matName].texture_slots[0].texture_coords = "UV"
            bpy.data.materials[matName].texture_slots[0].mapping = "CUBE"          
            
            
            """
            #Normal
            texName_normal = textName + "_normal"
            tex_normal = bpy.data.textures.new(texName_normal, type="IMAGE")            
            image_normal = bpy.data.images.load(imagePath_normal)
            tex_normal.image = image_normal
            bpy.data.textures[texName_normal].use_normal_map = True
            
            bpy.context.object.active_material.texture_slots[1].use_map_color_diffuse = False
            bpy.context.object.active_material.texture_slots[1].use_map_normal = True

            bpy.data.materials[matName].texture_slots.add().texture = tex_normal 
            #bpy.data.materials[matName].active_texture = tex_normal 
            bpy.data.materials[matName].texture_slots[1].use = True
            bpy.data.materials[matName].texture_slots[1].texture =  bpy.data.textures[texName_normal] 
            bpy.data.materials[matName].texture_slots[1].use_map_color_diffuse = False
            bpy.data.materials[matName].texture_slots[1].use_map_normal = True
            #bpy.data.materials[matName].texture_slots[1].normal_factor = 1
            bpy.data.materials[matName].texture_slots[1].texture_coords = "UV"
            bpy.data.materials[matName].texture_slots[1].uv_layer = UVMapName
            bpy.data.materials[matName].texture_slots[1].mapping = "CUBE"
            bpy.data.materials[matName].texture_slots[1].normal_map_space="TANGENT"
            #bpy.data.materials[matName].use_textures = [True,True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
            print("\n \n AddTexture \n \n texture name_normal :", bpy.data.materials[matName].texture_slots[1].name)   
            #bpy.data.materials[matName].active_textures
            """
            #export réussi en collada 
            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=True, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=False, use_object_instantiation=True, sort_by_name=False)
        
        else:
            bpy.ops.import_scene.obj(filepath=filepath_in)
            #if not matName in bpy.data.materials:
            material = bpy.data.materials.new(matName)
            material.diffuse_color = (r,g,b)
            #C = bpy.context
            bpy.context.object.data.materials.append(material)
            
            #Diffuse
            texName_diff = textName + "_diff"
            tex_diff = bpy.data.textures.new(texName_diff, type="IMAGE")            
            image_diff = bpy.data.images.load(imagePath_diff)
            tex_diff.image = image_diff
            
            bpy.ops.mesh.uv_texture_add()
            
            bpy.data.materials[matName].texture_slots.add()
            bpy.data.materials[matName].active_texture = tex_diff 
            bpy.data.materials[matName].texture_slots[0].texture_coords = "UV"
            bpy.data.materials[matName].texture_slots[0].mapping = "CUBE"
            
            """
            #Normal
            texName_normal = textName + "_normal"
            tex_normal = bpy.data.textures.new(texName_normal, type="IMAGE")            
            image_normal = bpy.data.images.load(imagePath_normal)
            tex_normal.image = image_normal
            
            bpy.data.materials[matName].texture_slots.add()
            bpy.data.materials[matName].active_texture = tex_normal 
            bpy.data.textures[texName_normal].use_map_normal
            bpy.data.materials[matName].texture_slots[1].use_map_normal
            bpy.data.materials[matName].texture_slots[1].normal_map_space="TANGENT"
            bpy.data.materials[matName].texture_slots[1].texture_coords = "UV"
            bpy.data.materials[matName].texture_slots[1].mapping = "CUBE"
            """

            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=True, use_object_instantiation=True, sort_by_name=False)
                
    def GenerateTangentsBitangenats(self):
                    
        filepath_in = self.name + self.extention 
        a = self.name +"_tgAdded" 
        self.name = a
        filepath_out = self.name + self.extention

        if self.extention == ".dae": 
            bpy.ops.wm.collada_import(filepath=filepath_in)
            
            ob = bpy.context.object
            if ob.type == 'MESH':
                me = ob.data
                me.calc_tangents()
                
                
                """
                for face in me.polygons:
                    # loop over face loop
                    for vert in [me.loops[i] for i in face.loop_indices]:
                        tangent = vert.tangent
                        normal = vert.normal
                        bitangent = vert.bitangent_sign * normal.cross(tangent)
                        
                for loop in me.loops:
                    print(loop.tangent)

                me.free_tangents()
            my_mesh = Collada(filepath_out) 
            print (filepath_out)
            my_geom = my_mesh.geometries[0]
            my_triset = my_geom.primitives[0]
            print ("vertex : ", my_triset.vertex[my_triset.vertex_index][0])
            print ("normal : ", my_triset.normal[my_triset.normal_index][0])
            print ("tg : ", my_triset.texcoordset[0][my_triset.texcoord_indexset[0]][0])
            """
            
            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=True, use_object_instantiation=True, sort_by_name=False)
            


        else:
            bpy.ops.import_scene.obj(filepath=filepath_in)
            
            ob = bpy.context.object
            if ob.type == 'MESH':
                me = ob.data
                me.calc_tangents()

            bpy.ops.wm.collada_export(filepath=filepath_out, check_existing=True, filter_blender=True, filter_image=True, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, apply_modifiers=True, export_mesh_type=0, export_mesh_type_selection='view', selected=True, include_children=False, include_armatures=False, deform_bones_only=False, active_uv_only=False, include_shapekeys=False, use_texture_copies=True, use_object_instantiation=True, sort_by_name=False)
    
    def load_from_file(self,filepath_in):
        bpy.ops.wm.collada_import(filepath=filepath_in)

    def convertMeshToOFF(self):
        filepath_in = self.name + self.extention 
        filepath_out = self.name + ".off"

        mesh = trimesh.load(filepath_in)
        mesh.export(filepath_out)
        
    def convertMeshToDAE(self):
        filepath_in = self.name + ".off" 
        self.extention =  ".dae"
        filepath_out = self.name + self.extention

        mesh = trimesh.load(filepath_in)
        mesh.export(filepath_out)

    def refine_mesh(self):  
        filepath_in = self.name + ".off" 
        a = self.name + "_Refine"
        self.name = a
        filepath_out = self.name + ".off"

        P=Polyhedron_3(filepath_in)

        flist = []
        for fh in P.facets():
            flist.append(fh)
        outf = []
        outv = []
        CGAL_Polygon_mesh_processing.refine(P, flist, outf, outv)

        P.write_to_file(filepath_out)
        return P
    
    def refine_mesh2(self):
        self.convertMeshToOFF()
        self.refine_mesh()
        self.convertMeshToDAE()
                
    def pipeline(self, pfactor= 0.9, piterations = 30):
        if self.extention == ".stl":
            self.refine_mesh2()
        print('Start Smooth')
        self.Smooth(pfactor,piterations)
        print('End Smooth')
        print('Start AddTexture')
        self.AddTexture()
        print('End AddTexture')
        print('Start cleanAllDecimateModifiers 2')
        self.cleanAllDecimateModifiers(1,decimateRatio= 0.25)
        print('End cleanAllDecimateModifiers 2')
        print("start tangentes")
        self.GenerateTangentsBitangenats()
        print("tangentes ok")
        