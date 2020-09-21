import bpy
from bpy.props import *
from .. Utility import utility

class TLM_UvChange(bpy.types.Operator):
    """UV Change"""
    bl_idname = "tlm.uv_change"
    bl_label = "UV change"
    bl_description = "UV Change"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # scene = context.scene
        # cycles = bpy.data.scenes[scene.name].cycles
        # selection = []

        #context = bpy.context

        for o in context.selected_objects:
            if o.type != 'MESH':
                continue # only meshes?
            uv = o.data.uv_layers
            ai = uv.active_index
            uv.active_index = 0 if ai else 1
            uv.active.active_render = True

        #ChangeUV
        print("////////////////////////////// Change UV")


        return{'FINISHED'}
