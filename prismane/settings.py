from .element import Element

import pygame as pg

class Settings(Element):
    def __init__(self, window_size, logical_size) -> None:
        super().__init__(singleton=True)

        self.window_size = self.window_width, self.window_height = window_size
        self.logical_size = self.logical_width, self.logical_height = logical_size
        
        self.x_scale = self.logical_width / self.window_width
        self.y_scale = self.logical_height / self.window_height
        self.scale = pg.Vector2(self.x_scale, self.y_scale)

        self.full_screen = True
        self.mouse_visible = True
        self.fps = 60
