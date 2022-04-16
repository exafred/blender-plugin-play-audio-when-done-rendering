bl_info = {
    "name": "Blender Render Complete? Play Sound!",
    "author": "Cat's Paw Studios",
    "version": (1, 0, 5),
    "blender": (3, 0, 0),
    "location": "Everywhere",
    "description": "Plays a user-defined audio file when a render finishes",
    "warning": "",
    "doc_url": "",
    "category": "Render",
}
import bpy
import os
import aud
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, BoolProperty
from bpy.app.handlers import persistent

class BRCPSPreferences(AddonPreferences):
    bl_idname = __name__
    scriptdir = bpy.path.abspath(os.path.dirname(__file__))

    filepath: StringProperty(
        name = "Audio File Path",
        subtype = 'FILE_PATH',
        default = scriptdir + '/Assets/Audio/blender-render-success-express.mp3'
    )
    soundOn: BoolProperty(
        name = "Play Sound When Render Finishes",
        default = True,
    )

    def draw(self, context):
        layout = self.layout
        # layout.label(text="Additional text without any inputs")
        layout.prop(self, "soundOn")
        layout.prop(self, "filepath")

class BRCPSCoreOperator(Operator):
    """Play the sound and such"""
    bl_idname = "object.brcps_run"
    bl_label = "BRCPS: Do it."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        if __name__ != "__main__":
            addon_prefs = preferences.addons[__name__].preferences
            path = addon_prefs.filepath
            playSound = addon_prefs.soundOn
        else:
            addon_prefs = []
            path = ""
            playSound = False

        print(path)
        
        # load the sound, IF we're out of __main__ and we're allowed to
        if path != "" and playSound == True:
            snd = aud.Sound(path)
            dev = aud.Device()
            dev.play(snd)
        else:
            self.report({'INFO'}, 'Please choose an audio file to play')

        print("Render Finished")

        return {'FINISHED'}


@persistent
def finish_render(scene, context):
    bpy.ops.object.brcps_run()    
    return None

bpy.app.handlers.render_complete.clear()
bpy.app.handlers.render_complete.append(finish_render)

def register():
    bpy.utils.register_class(BRCPSPreferences)
    bpy.utils.register_class(BRCPSCoreOperator)

    print("registered addon: Blender Render Complete? Play Sound!")
    

def unregister():
    bpy.utils.unregister_class(BRCPSPreferences)
    bpy.utils.unregister_class(BRCPSCoreOperator)
    print("unregistered addon: Blender Render Complete? Play Sound!")
    
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()