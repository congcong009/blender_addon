bl_info = {
    'name': 'Shadeless Material',
    'author': 'Ethan Luo, congcong009, (http://www.blenderget.com)',
    'version': (0,1),
    "blender": (2, 6, 5),
    "api": 52859,
    'location': '',
    'description': 'Shadeless all the materials, or make all shade',
    'warning': 'Not support in BGE mode',
    'category': 'Add Material'}


import bpy

def shadelessMat( ):

    mats = [ mat for mat in bpy.data.materials]   
    
    for mat in mats:
     if (mat.use_shadeless == False):
       mat.use_shadeless = True


def shadeMat( ):
   
    mats = [ mat for mat in bpy.data.materials] 
   
    for mat in mats:
     if (mat.use_shadeless == True):
       mat.use_shadeless = False
       
    
class ALlShadeless( bpy.types.Operator ):
    bl_label = "All Shader in Shadeless"
    bl_options = { 'REGISTER'}
    bl_idname = "material.shadeless"
   
    def execute( self, context ):
        shadelessMat()
        return {'FINISHED'}

class ALlShade( bpy.types.Operator ):
    bl_label = "All Shader in Shade"
    bl_options = { 'REGISTER'}
    bl_idname = "material.allshade"
   
    def execute( self, context ):
        shadeMat()
        return {'FINISHED'}
      
class RandomMatPanel( bpy.types.Panel ):
   
    bl_label = "Color Shadeless Panel"
    bl_region_type = "TOOLS"
    bl_space_type = "VIEW_3D"
   
    def draw( self, context ):
        scn = context.scene
        new_row = self.layout.row
       
        new_row().operator( "material.shadeless" )
        new_row().operator( "material.allshade" )
       

def register():
   
    scn_type = bpy.types.Scene
    BoolProperty = bpy.props.BoolProperty
    FloatProperty = bpy.props.FloatProperty
                                
    bpy.utils.register_class( ALlShadeless )
    bpy.utils.register_class( ALlShade )
    bpy.utils.register_class( RandomMatPanel )


def unregister():
    bpy.utils.register_class( ALlShadeless )
    bpy.utils.register_class( ALlShade )
    bpy.utils.register_class( RandomMatPanel )


if __name__ == '__main__':
    register()
