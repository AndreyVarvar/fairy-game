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

    def update(self):
        for ui_entity in self.groups["ui"]:
            ui_entity.update()

        for entity in self.groups["entities"]:
            entity.update()

    def draw(self):
        for ui_entity in self.groups["ui"]:
            ui_entity.queue_draw()

        for entity in self.groups["entities"]:
            entity.queue_draw()

