from .panels import MasterControlPanel
from .entity import EntityGroup
import pygame as pg


class Scene():
    def __init__(self):
        self.groups: dict[str, EntityGroup] = {
            "ui": EntityGroup(),
            "entities": EntityGroup()
        }

        self.change_scenes = False
        self.next_scene: str
    
    def queue_next_scene(self, next_scene_name):
        self.change_scenes = True
        self.next_scene = next_scene_name
    
    def load(self):
        pass

    def unload(self):
        pass

    def update(self, master_panel: MasterControlPanel):
        for ui_entity in self.groups["ui"]:
            ui_entity.update(master_panel)

        for entity in self.groups["entities"]:
            entity.update(master_panel)

    def draw(self, surface: pg.Surface, master_panel: MasterControlPanel):
        for ui_entity in self.groups["ui"]:
            ui_entity.draw(surface, master_panel)

        for entity in self.groups["entities"]:
            entity.draw(surface, master_panel)

