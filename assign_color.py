bl_info = {
    'name': 'Random Color',
    'author': 'Ethan Luo, congcong009, (http://www.blendercg.com)',
    'version': (0,1),
    "blender": (2, 6, 5),
    "api": 52859,
    'location': '',
    'description': 'Generate and assign random diffuse color to a object',
    'warning': 'Only working for MESH object!',
    'category': 'Add Material'}


import bpy
import time
from random import random, seed

def getRandomColor( color_min, color_max ):
    seed( time.time() )
   
    if color_min > color_max:
        color_min, color_max = 0, 1
   
    new_color = lambda : color_min + random() * ( color_max - color_min )
   
    red = new_color()
    green = new_color()
    blue = new_color()   
   
    return red, green, blue


def makeMaterials( ob, color_min, color_max ):
   
     randcolor = getRandomColor( color_min, color_max )
     mat = bpy.data.materials.new( "randmat" )
     mat.diffuse_color = randcolor     
   
   
def assignMats2Ob( ob ):
   
    mats = [ mat for mat in bpy.data.materials if mat.name.startswith( "rand" )]
   
    for mat in mats:
        if mat.users == 0:
          bpy.ops.object.material_slot_add()
          ob.active_material = mat


getUnusedRandoms = lambda : [ x for x in bpy.data.materials
                   if x.name.startswith( "randmat" ) and x.users == 0 ]


def clearMaterialSlots( ob ):
    while len( ob.material_slots ) > 0:
        bpy.ops.object.material_slot_remove()
        
        
def removeUnusedRandoms():
    unusedRandoms = getUnusedRandoms()
    for mat in unusedRandoms:
        bpy.data.materials.remove( mat )
       
class RandomMatOp( bpy.types.Operator ):
   
    bl_label = "Random Materials For Activea"
    bl_idname = "material.randommat"
    bl_options = { 'REGISTER', 'UNDO' }
   
   
    def execute( self, context ):
        ob = context.active_object
        scn = bpy.context.scene
       
        if len( ob.material_slots ) < 1:
            clearMaterialSlots( ob )
            removeUnusedRandoms()
            makeMaterials( ob, scn.color_min, scn.color_max )
            assignMats2Ob( ob )
           
        return {'FINISHED'}
   
    @classmethod   
    def poll( self, context ):
        ob = context.active_object
        return ob != None and ob.select

class RemoveAllMat( bpy.types.Operator):
    bl_label = "Remove Active Ob's Material"
    bl_options = { 'REGISTER'}
    bl_idname = "material.remove_allmats"
    
    def execute( self, context ):
        ob = context.active_object
        
        if len( ob.material_slots ) > 0:
            clearMaterialSlots( ob )
            removeUnusedRandoms()

        return {'FINISHED'}
    
class RemoveUnusedRandomOp( bpy.types.Operator ):
    bl_label = "Remove Unused Randoms"
    bl_options = { 'REGISTER'}
    bl_idname = "material.remove_unusedmats"
   
    def execute( self, context ):
        removeUnusedRandoms()
        return {'FINISHED'}

      
class RandomMatPanel( bpy.types.Panel ):
   
    bl_label = "Random Color Panel"
    bl_region_type = "TOOLS"
    bl_space_type = "VIEW_3D"
   
    def draw( self, context ):
        scn = context.scene
        new_row = self.layout.row
       
        new_row().operator( "material.randommat" )
        new_row().operator( "material.remove_allmats" )
        new_row().operator( "material.remove_unusedmats" )
       
        matCount = len( getUnusedRandoms() )
        countLabel = "Unused Random Materials: %d" % matCount
        self.layout.row().label( countLabel )
       

def register():
   
    scn_type = bpy.types.Scene
    BoolProperty = bpy.props.BoolProperty
    FloatProperty = bpy.props.FloatProperty
                                
    scn_type.color_min = FloatProperty( name = "Color Min", default = 0, min=0,
                         max=1, description = "Extreme Min for R, G, and B" )
                        
    scn_type.color_max = FloatProperty( name = "Color Max", default = 1, min=0,
                         max=1, description = "Max Color for R, G, and B" )
   
   
    bpy.utils.register_class( RandomMatOp )
    bpy.utils.register_class( RemoveAllMat )
    bpy.utils.register_class( RemoveUnusedRandomOp )
    bpy.utils.register_class( RandomMatPanel )


def unregister():
    bpy.utils.register_class( RandomMatOp )
    bpy.utils.register_class( RemoveAllMat )
    bpy.utils.register_class( RemoveUnusedRandomOp )
    bpy.utils.unregister_class( RandomMatPanel )


if __name__ == '__main__':
    register()
