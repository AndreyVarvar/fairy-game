from .panels import MasterControlPanel


class Scene():
    def __init__(self, name: str):
        self.name = name

        self.change_scenes = False
        self.next_scene = None
    
    def queue_next_scene(self, next_scene_name):
        self.change_scenes = True
        self.next_scene = next_scene_name
    
    def unload(self):
        pass

    def load(self):
        pass

    def update(self, master_panel: MasterControlPanel):
        master_panel.sound_panel.play_sound_queue()

    def draw(self, surface, game_data):
        pass