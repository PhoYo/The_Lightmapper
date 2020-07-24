import bpy, os, webbrowser
from bpy.props import *
from .. Utility import utility

class TLM_GltfLightmaps(bpy.types.Operator):
    """gltf the lightmaps"""
    bl_idname = "tlm.gltf_lightmaps"
    bl_label = "GLTF Lightmaps"
    bl_description = "GLTF Lightmaps"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scene = context.scene
        cycles = bpy.data.scenes[scene.name].cycles
        selection = []

        #make gltf
        print("////////////////////////////// MAKE GLTF ")


        print("--mesh objects--")

        for obj in bpy.data.objects:
            if obj.type == "MESH":
                print(obj.name)
                for slot in obj.material_slots:
                    
                    print("slot : " + slot.name)

                    tlm_gltf = bpy.data.node_groups.get('glTF Settings')
                    
                    if tlm_gltf == None:
                        utility.load_library('glTF Settings')
                        
                    # find the nodetree for the material slot
                    nodetree = bpy.data.materials[slot.name].node_tree

                    for node in nodetree.nodes:
                        if node.type == "TEX_IMAGE":
                            if node.name == "Lightmap_Image":
                                lightmapNode = node
                                print("node type : " + str(node) + " label : " + node.bl_label + " name : " + node.name)

                    outputNode = nodetree.nodes[0]

                    # if(outputNode.type != "OUTPUT_MATERIAL"):
                    #     for node in nodetree.nodes:
                    #         if node.type == "OUTPUT_MATERIAL":
                    #             outputNode = node
                    #             break
                    
                    #print("out node : " + str(outputNode))
                    
                    gltfNode = nodetree.nodes.new(type="ShaderNodeGroup")
                    gltfNode.node_tree = bpy.data.node_groups["glTF Settings"]
                    gltfNode.location = ((lightmapNode.location[0] + 600, lightmapNode.location[1]))
                    gltfNode.name = "gltfNode"

                    
                    for output in lightmapNode.outputs:
                        if output.name == "Color":
                            #output.default_value = gltfNode.inputs[0].default_value
                            print("lightmap output socket : " + output.name)
                            
                            #link the nodes
                            nodetree.links.remove(output.links[0])
                            nodetree.links.new(output, gltfNode.inputs[0])
                        
                    

                    print("gltf node created : " + gltfNode.name)

                    # first restore the backup material
                        
        print("--baked images--")
        for image in bpy.data.images:
            if image.name.endswith("_baked"):
                print(image.name)
                #connect that to the gltf node
                #bpy.data.images.remove(image, do_unlink=True)


        # for mat in bpy.data.materials:
        #     mat.update_tag()

        return{'FINISHED'}


    #glTF Settings