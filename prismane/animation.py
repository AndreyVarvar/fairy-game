from .entity import Entity
from .element import Element
from .assets import get_image
from .panels import TimeControlPanel

from pathlib import Path

import pygame as pg

class Spritesheet(Element):
    def __init__(self, image_path: Path, frame_size: pg.Vector2, is_horizontal: bool):
        super().__init__()
        self.spritesheet = get_image(image_path)
        self.frame_size = frame_size
        self.is_horizontal = is_horizontal

        self.frame_count: int
        if self.is_horizontal:
            self.frame_count = int(self.spritesheet.get_width() / self.frame_size.x)
        else:
            self.frame_count = int(self.spritesheet.get_height() / self.frame_size.y)
    
    def get_sprite(self, n) -> pg.Surface:
        if n < 0 or n >= self.frame_count:
            raise Exception(f"Frame index {n} out of range.")
        if self.is_horizontal:
            return self.spritesheet.subsurface((self.frame_size[0]*n, 0, self.frame_size[0], self.frame_size[1]))

        return self.spritesheet.subsurface((0, self.frame_size[1]*n, self.frame_size[0], self.frame_size[1]))


class Animation(Entity):
    def __init__(self, spritesheet: Spritesheet, fps: float, initial_frame_index: int = 0, loop: bool = True):
        super().__init__()
        self.spritesheet = spritesheet
        self.total_frames = self.spritesheet.frame_count
        self.fps = fps
        self.loop = loop

        self.end = False

        self.current_frame = initial_frame_index
        self.current_frame_time = 0.0  # sec
        self.spf = 1 / self.fps  # seconds per frame
        
    def reset(self):
        self.current_frame_time = 0.0
        self.current_frame = 0

    def update(self):
        time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]
        self.current_frame_time += time_panel.dt

        while self.current_frame_time > self.spf:
            self.current_frame += 1
        
        if self.loop:
            self.end = (self.current_frame >= self.total_frames-1)
            self.current_frame = self.current_frame % self.total_frames
        else:
            self.current_frame = min(self.current_frame, self.total_frames-1)
            self.end = (self.current_frame == self.total_frames-1)

        self.current_frame_time -= self.spf
    
    def get_frame(self):
        return self.spritesheet.get_sprite(self.current_frame)

