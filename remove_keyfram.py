bl_info = {
    "name": "Remove Keyframs",
    "author": "Se17",
    "version": (1, 0),
    "blender": (5, 0, 1),
    "description": "選択した複数のオブジェクトのスケールのキーフレームをクリアする",
    "warning": "まだ開発途中のものです",
    "support": "TESTING",
    "category": "Object",
}

import bpy


class TestMessage(bpy.types.Operator): 
    bl_idname = "object.test_message"
    bl_label = "アドオンの使い方"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "簡易的な説明を表示"


    def execute(self, context):
        self.report({'INFO'}, "選択しているオブジェクトのキーフレームを削除するアドオンです")
        return {'FINISHED'}



class NowRemoveKeyframs(bpy.types.Operator):
    bl_idname = "object.now_remove_keyframs"
    bl_label = "現在のキーフレームの削除"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "選択中のオブジェクトの、現在のキーフレームを一斉に削除する"


    def execute(self, context):
        # 現在のキーフレームを取得
        frame_now = bpy.context.scene.frame_current

        # 選択中のオブジェクトがない場合、処理をキャンセル
        if len(context.selected_objects) <= 0:
            self.report({'ERROR'}, "オブジェクトを1つ以上、選んでください")
            return {'CANCELLED'}
    
        for obj in bpy.context.selected_objects:
            if obj.animation_data is not None:
                if obj.animation_data.action is not None:
                    paths = ['location', 'rotation_euler', 'scale']
                    for p in paths:
                        obj.keyframe_delete(data_path=p, frame=frame_now)
                else:
                    self.report({'ERROR'}, f"オブジェクト{obj.name}にキーフレームのリンクがありません")
            else:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にアニメーションデータのリンクがありません")

        self.report({'INFO'}, "現在のキーフレームの削除完了")
        return{'FINISHED'}



class AllRemoveKeyframs(bpy.types.Operator):
    bl_idname = "object.all_remove_keyframs"
    bl_label = "キーフレーム全削除"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "選択中のオブジェクトの、すべてのキーフレームを一斉に削除する"

    
    def execute(self, context):
        # 選択中のオブジェクトがない場合、処理をキャンセル
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
    

class PanelUI(bpy.types.Panel): 
    bl_label = "キーフレームを削除しよう"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "キーフレームの削除"

    def draw(self, context):
        layout = self.layout
        layout.operator(TestMessage.bl_idname, text = "アドオンの説明")
        layout.operator(NowRemoveKeyframs.bl_idname, text = "現在のキーフレームを削除")
        layout.operator(AllRemoveKeyframs.bl_idname, text = "キーフレーム全削除")

    
classes = [
    TestMessage,
    NowRemoveKeyframs,
    AllRemoveKeyframs,
    PanelUI,
]

    
def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
