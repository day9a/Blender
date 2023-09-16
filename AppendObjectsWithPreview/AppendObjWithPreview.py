
import os
import bpy
from bpy.types import Panel

preview_collections = {}

# for auto scanning directory check example here:  
# Blender > Text Editor > Templates > Python > Ui Previews Dynamic Enum
thumbs = ['thumb00.png', 'thumb01.png', 'thumb02.png', 'thumb03.png',
          'thumb04.png', 'thumb05.png', 'thumb06.png', 'thumb07.png',
          'thumb08.png', 'thumb09.png', 'thumb10.png', 'thumb11.png',
          'thumb12.png', 'thumb13.png', 'thumb14.png', 'thumb15.png',
         ]

# generate previews from directory
def enum_previews(self, context):
    
    enum_items = []
    pcoll = preview_collections["main"]
    #directory = 'C:\folder\thumbs'
    directory = os.path.join(os.path.dirname(__file__), "thumbs")

    
    for i, name in enumerate(thumbs):
        filepath = os.path.join(directory, name)
        icon = pcoll.get(name)  
        if not icon:
            thumb = pcoll.load(name, filepath, 'IMAGE') 
        else:
            thumb = pcoll[name]
        enum_items.append((name, name, "", thumb.icon_id, i))
        
    pcoll.my_previews = enum_items
    return pcoll.my_previews

# make append object on select preview from panel
def update_selected(self, context):

    wm = context.window_manager
    #file_path = 'C:/folder/blender_bundle.blend'
    file_path = os.path.join(os.path.dirname(__file__), "blender_bundle.blend") 
    inner_path = 'Object'   
    object_name = 'Plane'
    
    for i, name in enumerate(thumbs):
        if wm.my_previews == name:
            object_name += str(i)
            
    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, object_name),
        directory=os.path.join(file_path, inner_path),
        filename=object_name
        )
        
    bpy.data.objects[object_name].location.xyz = 0    
    context.view_layer.objects.active = bpy.data.objects[object_name]
    
    if wm.my_toggle:  
        bpy.ops.transform.translate('INVOKE_REGION_WIN',
            snap=True, snap_elements={'FACE'}, snap_target='CENTER', snap_align=True, snap_normal=(0.5, 0.5, 0.5),)

    return None

# panel with enum property with stored previews
class APPEND_PT_Panel(Panel):
    bl_label = "Append Panel"
    bl_idname = "OBJECT_PT_previews"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Append object"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.template_icon_view(wm, "my_previews", show_labels=False, scale=6, scale_popup=6)
        
        row = layout.row()
        row.prop(wm, 'my_toggle', text='Use snap')

def register():
    from bpy.types import WindowManager
    from bpy.props import (BoolProperty, EnumProperty)
    
    # store properties
    WindowManager.my_toggle = BoolProperty(default=True,) 
    WindowManager.my_previews = EnumProperty(
        items=enum_previews,
        description="",
        default=None,
        update=update_selected,
    )

    # blender makes previews using this util
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews = ()

    preview_collections["main"] = pcoll

    bpy.utils.register_class(APPEND_PT_Panel)


def unregister():
    from bpy.types import WindowManager
    
    del WindowManager.my_toggle
    del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    thumbs.clear()

    bpy.utils.unregister_class(APPEND_PT_Panel)

if __name__ == "__main__":
    register()
