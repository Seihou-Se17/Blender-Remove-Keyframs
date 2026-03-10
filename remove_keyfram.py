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


bl_info = {
    "name": "Remove Keyframs",
    "author": "Se17",
    "version": (0, 1),
    "blender": (5, 0, 1),
    "description": "選択した複数のオブジェクトのスケールのキーフレームをクリアする",
    "warning": "まだ開発途中のものです",
    "support": "TESTING",
    "category": "Object",
}

import bpy


class Test_message(bpy.types.Operator): 
    bl_idname = "object.test_message"
    bl_label = "アドオンの使い方"
    bl_options = {'REGISTER'}
    bl_description = "簡易的な説明を表示"

    def execute(self, context):
        self.report({'INFO'}, "選択しているオブジェクトのキーフレームを削除するアドオンです")
        return {'FINISHED'}


class All_Remove_Keyframs(bpy.types.Operator):
    bl_idname = "object.all_remove_keyframs"
    bl_label = "選択したオブジェクトのスケールのキーフレームをクリア"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "複数のオブジェクトのすべてのスケールのキーフレームを一斉にクリアする"

    def execute(self, context):
        if len(context.selected_objects) <= 0:
            self.report({'ERROR'}, "オブジェクトを1つ以上、選んでください")
            return {'CANCELLED'}
    
        for obj in bpy.context.selected_objects:
            if obj.animation_data is not None:
                if obj.animation_data.action is not None:
                    bpy.data.actions.remove(obj.animation_data.action, do_unlink=True)
                else:
                    self.report({'ERROR'}, f"オブジェクト{obj.name}にキーフレームのリンクがありません")
            else:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にアニメーションデータのリンクがありません")

        self.report({'INFO'}, "キーフレームの全削除完了")
        return{'FINISHED'}
    

class Panel_button(bpy.types.Panel): 
    bl_label = "キーフレームを削除しよう"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "キーフレームの削除"

    def draw(self, context):
        layout = self.layout
        layout.operator(Test_message.bl_idname, text = "アドオンの説明")
        layout.operator(All_Remove_Keyframs.bl_idname, text = "キーフレーム全削除")

    
classes = [
    Test_message,
    All_Remove_Keyframs,
    Panel_button,
]

    
def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()