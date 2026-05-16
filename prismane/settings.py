from .element import Element

import pygame as pg

class Settings(Element):
    def __init__(self, window_size, display_size) -> None:
        super().__init__(singleton=True)

        self.window_size = self.window_width, self.window_height = window_size  # (2880, 1620)
        self.display_size = self.display_width, self.display_height = display_size  # (1920, 1080)
        
        self.x_scale = self.display_width / self.window_width
        self.y_scale = self.display_height / self.window_height
        self.scale = pg.Vector2(self.x_scale, self.y_scale)

        self.full_screen = True
        self.mouse_visible = True
        self.fps = 60
