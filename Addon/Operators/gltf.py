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

                    try:
                         principled = nodetree.nodes["Principled BSDF"]
                    except:
                        print("no principled BSDF node")
                    

                    for node in nodetree.nodes:
                        print("ALL NODES : " + node.name)

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


                        if node.name == "LM_P":
                            
                            LM_Pnode = node

                            for output in LM_Pnode.outputs:
                                if output.name == "Color":
                                    nodetree.links.remove(output.links[0])
                                    nodetree.links.new(output, principled.inputs["Base Color"])
                        

                        if node.name == "Lightmap_BasecolorNode_A":

                            
                            print("this has base colour")

                            baseColor = node
                            nodetree.nodes.remove( baseColor )

                            # for output in baseColor.outputs:
                            #     if output.name == "Color":
                            #         nodetree.nodes.remove( baseColor )
                                    #nodetree.links.remove(output.links[0])
                                    #nodetree.links.new(output, principled.inputs["Base Color"])

                    
                
                try:
                #if nodetree.nodes['Lightmap_Multiplication'] is None:
                #    pass
                #else :
                    multiply = nodetree.nodes['Lightmap_Multiplication']
                    nodetree.nodes.remove( multiply )
                except:
                    print("no multiply node")



                bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
                
        #bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', export_selected=True, use_selection=True)
                

        # print("--baked images--")
        # for image in bpy.data.images:
        #     if image.name.endswith("_baked"):
        #         print(image.name)

        

        return{'FINISHED'}


    #glTF Settings