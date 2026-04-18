from prismane import Scene
from prismane import MasterControlPanel
import pygame as pg

class GameplayScene(Scene):
    def __init__(self):
        super().__init__()
    
    def update(self, master_panel: MasterControlPanel):
        super().update(master_panel)

    def draw(self, surface: pg.Surface, master_panel: MasterControlPanel):
        super().draw(surface, master_panel)
