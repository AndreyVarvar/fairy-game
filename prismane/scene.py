from .panels import MasterControlPanel
from .element import ElementGroup
import pygame as pg


class Scene():
    def __init__(self):
        self.elements: ElementGroup = ElementGroup()

        self.change_scenes = False
        self.next_scene: str | None = None
    
    def queue_next_scene(self, next_scene_name):
        self.change_scenes = True
        self.next_scene = next_scene_name
    
    def unload(self):
        pass

    def update(self, master_panel: MasterControlPanel):
        for elem in self.elements:
            elem.update(master_panel, self.elements)

        master_panel.sound_panel.play_sound_queue()

    def draw(self, surface: pg.Surface, master_panel: MasterControlPanel):
        for elem in self.elements:
            elem.draw(surface, master_panel)
