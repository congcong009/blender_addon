bl_info = {
    'name': 'RenderLayer Assign',
    'author': 'Ethan Luo, congcong009, (http://www.blenderget.com)',
    'version': (0,2),
    "blender": (2, 6, 5),
    "api": 52859,
    'location': '',
    'description': 'Assign selected objects to specific layer and generate layer-render output node',
    'warning': '',
    'category': 'Render'}

import bpy
import os

scn_type = bpy.types.Scene
scn = bpy.context.scene
obs = bpy.context.selected_objects
tree = bpy.context.scene.node_tree
#links = tree.links

def moveSelectedObjects2Layer ( layer ):
   
    layers = 20 * [False]
    layers[ layer - 1 ] = True
    bpy.ops.object.move_to_layer(layers=layers)
   
    layers = 20 * [True]
    scn.layers = layers

    return


def clearRenderLayer ():
   
    for i in range(0, len(scn.render.layers)):
        bpy.ops.scene.render_layer_remove()
   
    scn.render.layers.active.name = 'LeaveThisRenderLayer'
   
    for layers in scn.render.layers:
        if layers.use == True:
           layers.use = False
   

def newRenderLayer( layer ):
   
    bpy.ops.scene.render_layer_add()
   
    scn.render.layers.active.name = str(layer)
   
    layers = 20 * [False]
    layers[ layer - 1] = True
    layers[ 10 ] = True
    scn.render.layers.active.layers = layers
   
    return

def activeRenderNose ():
    scn = bpy.context.scene
    tree = bpy.context.scene.node_tree
   
    scn.use_nodes = True
       
    return

def cleanUpNodes ():
    scn = bpy.context.scene
    tree = bpy.context.scene.node_tree
   
    for n in tree.nodes:
        tree.nodes.remove(n)
       
    return   

def addImportRenderLayerNode ( layer, x, y ):
    tree = bpy.context.scene.node_tree
       
    importrenderlayer = tree.nodes.new('R_LAYERS')  
      
    importrenderlayer.location = x,y
    importrenderlayer.layer = str(layer)
   
    return importrenderlayer

def addOutputImageNode ( layer, x, y ):
    tree = bpy.context.scene.node_tree    
    outputrenderlayer = tree.nodes.new('OUTPUT_FILE')  
      
    outputrenderlayer.location = x,y
    #outputrenderlayer.base_path = outputrenderlayer.base_path  + str(layer)
    outputrenderlayer.file_slots['Image'].path = 'Image' + str(layer)
       
    return outputrenderlayer

def addCompositionNode ( x, y):
    tree = bpy.context.scene.node_tree    
    compositionNode = tree.nodes.new('COMPOSITE')  
    compositionNode.location = x,y
   
    return compositionNode


def setOutputFileFormat ( ):
   
    scn.render.image_settings.color_mode = "RGBA"
   
    return

def linkNode ( importNode, outputNode):
    tree = bpy.context.scene.node_tree   
    links = tree.links

    links.new(importNode.outputs[0], outputNode.inputs[0])
   
    return importNode
      
class MoveAllOb2Layer11 (bpy.types.Operator):

    bl_label = "Move All Objects to Layer 11"
    bl_idname = "object.moveall2layer11"
    bl_options = { 'REGISTER', 'UNDO' }
   
    def execute( self, context ):
       
        bpy.ops.object.select_all( action='SELECT' )
        moveSelectedObjects2Layer( 11 )
        clearRenderLayer()
       
        return {'FINISHED'}

       
class AssignObjectRenderLayer01 (bpy.types.Operator):
   
    bl_label = "Move to Layer 01 and Create RenderLayer 01"
    bl_idname = "object.assignlayer01"
    bl_options = { 'REGISTER', 'UNDO' }
   
    def execute( self, context ):
       
        moveSelectedObjects2Layer ( 1 )
       
        newRenderLayer( 1 )
        setOutputFileFormat()
       
        activeRenderNose()
       
        linkNode ( linkNode (addImportRenderLayerNode( 1, 0, 500 ), addOutputImageNode( 1, 500, 500 )), addCompositionNode( 1000, 500 ))
       
       
        return {'FINISHED'}

class AssignObjectRenderLayer02 (bpy.types.Operator):
   
    bl_label = "Move to Layer 02 and Create RenderLayer 02"
    bl_idname = "object.assignlayer02"
    bl_options = { 'REGISTER', 'UNDO' }
   
    def execute( self, context ):
       
        moveSelectedObjects2Layer ( 2 )
       
        newRenderLayer( 2 )
       
        linkNode (addImportRenderLayerNode( 2, 0, 0 ), addOutputImageNode( 2, 500, 0 ))
       
        return {'FINISHED'}   

class AssignObjectRenderLayer03 (bpy.types.Operator):
   
    bl_label = "Move to Layer 03 and Create RenderLayer 03"
    bl_idname = "object.assignlayer03"
    bl_options = { 'REGISTER', 'UNDO' }
   
    def execute( self, context ):
       
        moveSelectedObjects2Layer ( 3 )
       
        newRenderLayer( 3 )
       
        linkNode (addImportRenderLayerNode( 3, 0, -500 ), addOutputImageNode( 3, 500, -500 ))
        return {'FINISHED'}  

class AssignObjectRenderLayer04 (bpy.types.Operator):
   
    bl_label = "Move to Layer 04 and Create RenderLayer 04"
    bl_idname = "object.assignlayer04"
    bl_options = { 'REGISTER', 'UNDO' }
   
    def execute( self, context ):
       
        moveSelectedObjects2Layer ( 4 )
       
        newRenderLayer( 4 )
       
        linkNode (addImportRenderLayerNode( 4, 0, -1000 ), addOutputImageNode( 4, 500, -1000 ))
        return {'FINISHED'}  

class AssignObjectRenderLayer05 (bpy.types.Operator):
   
    bl_label = "Move to Layer 05 and Create RenderLayer 05"
    bl_idname = "object.assignlayer05"
    bl_options = { 'REGISTER', 'UNDO' }
   
    def execute( self, context ):
       
        moveSelectedObjects2Layer ( 5 )
       
        newRenderLayer( 5 )
       
        linkNode (addImportRenderLayerNode( 5, 0, -1500 ), addOutputImageNode( 5, 500, -1500 ))
        return {'FINISHED'}      

class CleanUpNodes (bpy.types.Operator):

    bl_label = "Delete All Nodes"
    bl_idname = "node.cleanup"
    bl_options = { 'REGISTER', 'UNDO' }
   
    def execute( self, context ):

        cleanUpNodes()
       
        return {'FINISHED'}
               
class LayerAssignPanel( bpy.types.Panel ):
 
    bl_label = "Layer Assignment Panel"
    bl_region_type = "TOOLS"
    bl_space_type = "VIEW_3D"
 
    def draw( self, context ):
        scn = context.scene.render
        layout = self.layout
        new_row = self.layout.row      
     
        new_row().operator( "object.moveall2layer11" )
       
        layout.prop(scn, "filepath", text="")
       
        layout.split()       
        new_row().operator( "object.assignlayer01" )
        new_row().operator( "object.assignlayer02" )
        new_row().operator( "object.assignlayer03" )
        new_row().operator( "object.assignlayer04" )
        new_row().operator( "object.assignlayer05" )
        new_row().operator( "node.cleanup" )
            

def register():
 
    StringProperty = bpy.props.StringProperty
   
    scn_type.filepath = StringProperty( name = "filepath", default = "d:/tmp/" )

    bpy.utils.register_class( LayerAssignPanel )
    bpy.utils.register_class( MoveAllOb2Layer11 )
    bpy.utils.register_class( AssignObjectRenderLayer01 )
    bpy.utils.register_class( AssignObjectRenderLayer02 )
    bpy.utils.register_class( AssignObjectRenderLayer03 )
    bpy.utils.register_class( AssignObjectRenderLayer04 )
    bpy.utils.register_class( AssignObjectRenderLayer05 )
    bpy.utils.register_class( CleanUpNodes )
   
def unregister():
    bpy.utils.register_class( LayerAssignPanel )
    bpy.utils.register_class( MoveAllOb2Layer11 )
    bpy.utils.register_class( AssignObjectRenderLayer01 )
    bpy.utils.register_class( AssignObjectRenderLayer02 )
    bpy.utils.register_class( AssignObjectRenderLayer03 )
    bpy.utils.register_class( AssignObjectRenderLayer04 )
    bpy.utils.register_class( AssignObjectRenderLayer05 )
    bpy.utils.register_class( CleanUpNodes )

if __name__ == '__main__':
    register()