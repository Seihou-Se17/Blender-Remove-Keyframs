bl_info = {
    "name": "Remove Keyframs",
    "author": "Se17",
    "version": (1, 2),
    "blender": (5, 0, 1),
    "description": "選択した複数のオブジェクトのキーフレームを削除する",
    "warning": "まだ開発途中のものです",
    "support": "TESTING",
    "category": "Object",
}


import bpy


class AddonProperties(bpy.types.PropertyGroup):
    location_x: bpy.props.BoolProperty(name="location_x", default=False)
    location_y: bpy.props.BoolProperty(name="location_y", default=False)
    location_z: bpy.props.BoolProperty(name="location_z", default=False)
    
    rotation_x: bpy.props.BoolProperty(name="rotation_x", default=False)
    rotation_y: bpy.props.BoolProperty(name="rotation_y", default=False)
    rotation_z: bpy.props.BoolProperty(name="rotation_z", default=False)
    
    scale_x: bpy.props.BoolProperty(name="scale_x", default=False)
    scale_y: bpy.props.BoolProperty(name="scale_y", default=False)
    scale_z: bpy.props.BoolProperty(name="scale_z", default=False)


class TestMessage(bpy.types.Operator): 
    bl_idname = "object.test_message"
    bl_label = "アドオンの使い方"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "簡易的な説明を表示"

    def execute(self, context):
        self.report({'INFO'}, "選択しているオブジェクトのキーフレームを削除するアドオンです")
        return {'FINISHED'}


class AllTransformKeyframs(bpy.types.Operator): 
    bl_idname = "object.all_transform_keyframs"
    bl_label = "選択したトランスフォームのキーフレームの削除"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "トグルボタンが押されたトランスフォームのキーフレームを全て削除する"

    def execute(self, context):
        props = context.scene.my_addon_props
        transform = []

        if props.location_x:
            transform.append(("location", 0))
        if props.location_y:
            transform.append(("location", 1))
        if props.location_z:
            transform.append(("location", 2))

        if props.rotation_x:
            transform.append(("rotation_euler", 0))
        if props.rotation_y:
            transform.append(("rotation_euler", 1))
        if props.rotation_z:
            transform.append(("rotation_euler", 2))

        if props.scale_x:
            transform.append(("scale", 0))
        if props.scale_y:
            transform.append(("scale", 1))
        if props.scale_z:
            transform.append(("scale", 2))

        if not transform:
            self.report({'ERROR'}, "何も選択されていません")
            return {'CANCELLED'}
        
        for obj in bpy.context.selected_objects:
            if obj.animation_data is None:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にアニメーションデータのリンクがありません")
                continue

            if obj.animation_data.action is None:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にキーフレームのリンクがありません")
                continue

            if obj.rotation_mode == 'QUATERNION':
                self.report({'ERROR'}, f"オブジェクト{obj.name}はクォータニオンです。現在クォータニオンには対応していません。")
                continue

            for path, idx in transform:
                obj.keyframe_delete(data_path=path, index=idx)

        self.report({'INFO'}, "選択したトランスフォームのキーフレームの削除")
        return{'FINISHED'}


class NowRemoveKeyframs(bpy.types.Operator):
    bl_idname = "object.now_remove_keyframs"
    bl_label = "現在のキーフレームの削除"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "選択中のオブジェクトの、現在のキーフレームを一斉に削除する"


    def execute(self, context):
        if len(context.selected_objects) <= 0:
            self.report({'ERROR'}, "オブジェクトを1つ以上、選んでください")
            return {'CANCELLED'}
    
        for obj in bpy.context.selected_objects:
            if obj.animation_data is None:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にアニメーションデータのリンクがありません")
                continue

            if obj.animation_data.action is None:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にキーフレームのリンクがありません")
                continue

            bpy.ops.anim.keyframe_delete_v3d()

        self.report({'INFO'}, "現在のキーフレームの全削除完了")
        return{'FINISHED'}



class AllRemoveKeyframs(bpy.types.Operator):
    bl_idname = "object.all_remove_keyframs"
    bl_label = "キーフレーム全削除"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "選択中のオブジェクトの、すべてのキーフレームを一斉に削除する"

    
    def execute(self, context):
        if len(context.selected_objects) <= 0:
            self.report({'ERROR'}, "オブジェクトを1つ以上、選んでください")
            return {'CANCELLED'}
    
        for obj in bpy.context.selected_objects:
            if obj.animation_data is None:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にアニメーションデータのリンクがありません")
                continue

            if obj.animation_data.action is None:
                self.report({'ERROR'}, f"オブジェクト{obj.name}にキーフレームのリンクがありません")
                continue

            bpy.ops.anim.keyframe_clear_v3d()

        self.report({'INFO'}, "キーフレームの全削除完了")
        return{'FINISHED'}
    

class PanelUI(bpy.types.Panel): 
    bl_label = "キーフレームを削除しよう"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "キーフレームの削除"

    def draw(self, context):
        layout = self.layout
        props = context.scene.my_addon_props

        row = layout.row(align=False)
        layout.operator(TestMessage.bl_idname, text = "アドオンの説明")
        
        layout.separator()

        layout.label(text="位置 :")
        row = layout.row(align=True)
        row.prop(props, "location_x", toggle=True)
        row.prop(props, "location_y", toggle=True)
        row.prop(props, "location_z", toggle=True)

        layout.label(text="回転 :")
        row = layout.row(align=True)
        row.prop(props, "rotation_x", toggle=True)
        row.prop(props, "rotation_y", toggle=True)
        row.prop(props, "rotation_z", toggle=True)

        layout.label(text="スケール :")
        row = layout.row(align=True)
        row.prop(props, "scale_x", toggle=True)
        row.prop(props, "scale_y", toggle=True)
        row.prop(props, "scale_z", toggle=True)

        layout.operator(AllTransformKeyframs.bl_idname, text = "選択したキーフレームを削除")

        layout.separator()

        layout.operator(NowRemoveKeyframs.bl_idname, text = "現在のキーフレームを全削除")
        layout.operator(AllRemoveKeyframs.bl_idname, text = "キーフレーム全削除")

    
classes = [
    AddonProperties,
    TestMessage,
    AllTransformKeyframs,
    NowRemoveKeyframs,
    AllRemoveKeyframs,
    PanelUI,
]

    
def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=AddonProperties)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_addon_props

if __name__ == "__main__":
    register()
