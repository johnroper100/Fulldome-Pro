# Copyright 2016 John Roper
#
# ##### BEGIN GPL LICENSE BLOCK ######
#
# Fulldome Pro is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fulldome Pro is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fulldome Pro.  If not, see <http://www.gnu.org/licenses/>.
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Fulldome Pro",
    "author": "John Roper",
    "version": (1, 0, 0),
    "blender": (2, 78, 0),
    "location": "3D View > Toolbar > Tools > Fulldome Pro",
    "description": "Quicly set up your scene for fulldome production",
    "warning": "",
    "wiki_url": "http://jmroper.com/",
    "tracker_url": "mailto:johnroper100@gmail.com",
    "category": "Render"
}

import bpy
from bpy.types import Operator, Panel
from bpy.props import *


class FPSetupScene(Operator):
    """Setup a fulldome scene"""
    bl_idname = "scene.fp_setup_scene"
    bl_label = "Setup Fulldome Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.render.engine == "CYCLES":
            scene = bpy.context.scene
            main_quality = 4096
            if scene.FP_quality == 'high':
                scene.render.resolution_x = main_quality
                scene.render.resolution_y = main_quality
            elif scene.FP_quality == 'medium':
                scene.render.resolution_x = main_quality/2
                scene.render.resolution_y = main_quality/2
            elif scene.FP_quality == 'low':
                scene.render.resolution_x = main_quality/4
                scene.render.resolution_y = main_quality/4
            else:
                print("There is a problem with the quality variable. Did you try to enter a value other then high, medium, or low?")

            scene.render.resolution_percentage = 100

            cam = bpy.data.cameras.new("Fulldome Camera")
            cam.type = 'PANO'
            cam.cycles.panorama_type = 'FISHEYE_EQUIDISTANT'
            cam_ob = bpy.data.objects.new("Fulldome Camera", cam)
            cam_ob.rotation_euler = (1.5707963705062866, 0, 0)
            scene.objects.link(cam_ob)
            scene.camera = cam_ob
        else:
            self.report({'ERROR'}, "You must enable Cycles to use Fulldome Pro!")

        return {'FINISHED'}


class FPSetupPreview(Operator):
    """Setup a fulldome preview scene"""
    bl_idname = "scene.fp_setup_preview"
    bl_label = "Setup Fulldome Preview"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.render.engine == "CYCLES":
            scene = bpy.context.scene
            print("Preview set up!")
        else:
            self.report({'ERROR'}, "You must enable Cycles to use Fulldome Pro!")

        return {'FINISHED'}


class FPPanel(Panel):
    """Creates Fulldome Pro Panel in the tools panel."""
    bl_idname = "FPPanel"
    bl_label = "Fulldome Pro"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='MAT_SPHERE_SKY')

    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout

        if bpy.context.scene.render.engine == "CYCLES":
            row = layout.row()
            row.prop(scene, "FP_quality", icon='SETTINGS')

            row = layout.row()
            row.scale_y = 1.2
            row.operator("scene.fp_setup_scene", icon='FILE_TICK')

            #row = layout.row()
            #row.scale_y = 1.1
            #row.operator("scene.fp_setup_preview", icon='IMAGE_COL')
        else:
            row = layout.row()
            row.label("You must enable Cycles to use Fulldome Pro!", icon='ERROR')


def register():
    bpy.utils.register_class(FPSetupScene)
    bpy.utils.register_class(FPSetupPreview)
    bpy.utils.register_class(FPPanel)
    bpy.types.Scene.FP_quality = bpy.props.EnumProperty(
        items=[('high', 'High', '4k image quality'),
               ('medium', 'Medium', '2k image quality'),
               ('low', 'Low', 'HD image quality')],
        name="Quality",
        description="The output image size",
        default="high")


def unregister():
    bpy.utils.unregister_class(FPSetupScene)
    bpy.utils.unregister_class(FPSetupPreview)
    bpy.utils.unregister_class(FPPanel)

    del bpy.types.Scene.FP_quality


if __name__ == "__main__":
    register()
