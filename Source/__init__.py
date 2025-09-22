# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This is a 3DMigoto plugin for Blender 4.5
# Source code is from https://github.com/DarkStarSword/3d-fixes
# Base this code, I make a SidebarUI and some extensins

from . import blender_3dmigoto
import re
import bpy

num_only = re.compile(r'''^\d+$''')

class Clear_Vertex_Groups(bpy.types.Operator):
    "Clear Vertex Group"
    bl_idname = "helper.clear_vertex_group"
    bl_label = "Clear Vertex Group"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        remove_count=0
        select_objects = context.selected_objects
        for select_object in select_objects:
            if select_object is None or select_object.type != 'MESH':
                continue
            vertex_groups=select_object.vertex_groups
            remove_vertex_groups=[]
            for vertex_group in vertex_groups:
                if num_only.match(vertex_group.name) is None:
                    remove_vertex_groups.append(vertex_group)
            remove_count+=len(remove_vertex_groups)
            for vertex_group in remove_vertex_groups:
                vertex_groups.remove(vertex_group)
        print(f"remove {remove_count} vertex groups")
        return{'FINISHED'}

class Clear_Armatures(bpy.types.Operator):
    "Clear Armatures"
    bl_idname = "helper.clear_armatures"
    bl_label = "Clear Armatures"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        objects = context.scene.objects
        armature_objects = [obj for obj in objects if obj.type == 'ARMATURE']
        clear_armatures = []
        for armature in armature_objects:
            children = [child for child in armature.children if child.type == 'MESH']
            if len(children) == 0:
                clear_armatures.append(armature)
        for armature in clear_armatures:
            bpy.data.objects.remove(object=armature,do_unlink=True)
        print(f"reomve {len(clear_armatures)} armatures")
        return{'FINISHED'}

class View3D_PT_3DMigoto(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "3DMigoto"
    bl_label = "3DMigoto Tools"

    def draw(self, context):
        self.layout.label(text="Import")
        self.layout.operator("import_mesh.migoto_frame_analysis",text="Frame Analysis")
        self.layout.operator("import_mesh.migoto_raw_buffers",text="Raw Buffer")
        self.layout.operator("armature.migoto_pose",text='Pose')
        self.layout.label(text="Export")
        self.layout.operator("export_mesh.migoto",text="Raw Buffer")
        self.layout.label(text="Helper")
        self.layout.operator("armature.merge_pose",text="Merge Pose")
        self.layout.operator(Clear_Armatures.bl_idname,text="Clear Armatures")
        self.layout.operator(Clear_Vertex_Groups.bl_idname,text="Clear Vertex Groups")

classes=[Clear_Vertex_Groups,Clear_Armatures,View3D_PT_3DMigoto]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for cls in blender_3dmigoto.register_classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(blender_3dmigoto.menu_func_import_fa)
    bpy.types.TOPBAR_MT_file_import.append(blender_3dmigoto.menu_func_import_raw)
    bpy.types.TOPBAR_MT_file_import.append(blender_3dmigoto.menu_func_import_pose)
    bpy.types.TOPBAR_MT_file_import.append(blender_3dmigoto.menu_func_apply_vgmap)
    bpy.types.TOPBAR_MT_file_export.append(blender_3dmigoto.menu_func_export_raw)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for cls in blender_3dmigoto.register_classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(blender_3dmigoto.menu_func_import_fa)
    bpy.types.TOPBAR_MT_file_import.remove(blender_3dmigoto.menu_func_import_raw)
    bpy.types.TOPBAR_MT_file_import.remove(blender_3dmigoto.menu_func_apply_vgmap)
    bpy.types.TOPBAR_MT_file_import.remove(blender_3dmigoto.menu_func_import_pose)
    bpy.types.TOPBAR_MT_file_export.remove(blender_3dmigoto.menu_func_export_raw)

if __name__ == "__main__":
    register()
