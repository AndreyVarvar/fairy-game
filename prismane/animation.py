from .entity import Entity
from .element import Element
from .assets import get_image
from .panels import TimeControlPanel

from pathlib import Path
from enum import Enum

import pygame as pg


class SpritesheetType(Enum):
    IMAGE_HORIZONTAL = 0  # a single image contains all frames in horizontal layout
    IMAGE_VERTICAL = 1  # a single image contains all frames in vertical layout
    DIRECTORY = 2  # all frames are in a directory


class Spritesheet(Element):
    def __init__(self, sprites: list[pg.Surface]):
        super().__init__()
        self.frames = sprites
        self.frame_count = len(self.frames)
    
    def get_sprite(self, n) -> pg.Surface:
        return self.frames[n]

class DirectorySpritesheet(Spritesheet):
    def __init__(self, directory_path: Path, file_format: str, frame_count: int):
        """
        directory_path: pathlib.Path. Location of the directory
        file_format: str. Format in which files are formatted. Example: 'Frame{0:04}' (Frame0000, Frame0001, Frame0002, ...)
        frame_count: int. Number of such files.
        """
        sprites = []
        for i in range(frame_count):
            sprites.append(get_image(directory_path / file_format.format(i)))
        super().__init__(sprites)

class ImageSpritesheet(Spritesheet):
    def __init__(self, image_path: Path, frame_size: tuple[int, int], is_horizontal: bool):
        image: pg.Surface = get_image(image_path)
        sprites = []
        if is_horizontal:
            for i in range(image.get_width() // frame_size[0]):
                sprites.append(image.subsurface(frame_size[0] * i, 0, frame_size[0], frame_size[1]))
        else:
            for i in range(image.get_height() // frame_size[1]):
                sprites.append(image.subsurface(0, frame_size[1] * i, frame_size[0], frame_size[1]))
        super().__init__(sprites)

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

