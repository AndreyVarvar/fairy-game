from .entity import Entity
from .element import Element
from .assets import get_image
from .panels import TimeControlPanel

from pathlib import Path
from enum import Enum

import pygame as pg
import json


class Spritesheet(Element):
    def __init__(self, spritesheet_json_path: Path):
        super().__init__()

        self.frames: list = self.load(spritesheet_json_path)
        self.frame_count: int = len(self.frames)
    
        
    def load(self, spritesheet_json_path: Path) -> list:
        frames: list = []
        with open(spritesheet_json_path, 'r') as file:
            spritesheet_json = json.load(file)
        
        if spritesheet_json["spritesheet-type"] == "single-image":
            frames = self.load_single_image_type(spritesheet_json)
        elif spritesheet_json["spritesheet-type"] == "directory":
            frames = self.load_directory_type(spritesheet_json)
        else:
            raise Exception(f"Unknown spritesheet type: {spritesheet_json['spritesheet-type']}")

        return frames

    def load_single_image_type(self, spritesheet_json: dict):
        image = get_image(Path(spritesheet_json["image-path"]))
        sprites = []
        for rect in spritesheet_json["images"]: 
            sprites.append(image.subsurface(rect))
        return sprites


    def load_directory_type(self, spritesheet_json: dict):
        sprites = []
        format_type = spritesheet_json["format-type"]
        directory_path = Path(spritesheet_json["directory-path"])

        if format_type == "formatted":
            format = spritesheet_json["format"]
            sprite_count = spritesheet_json["count"]
            for i in range(sprite_count):
                sprites.append(get_image(directory_path / format.format(i)))
        elif format_type == "file-names":
            sprite_names = spritesheet_json["images"]
            for name in sprite_names:
                sprites.append(get_image(directory_path / name))
        else:
            raise Exception(f"Unknown directory spritesheet type formatting: {format_type}")

        return sprites

    def get_sprite(self, n: int) -> pg.Surface:
        return self.frames[n]

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
            self.current_frame_time -= self.spf
        
        if self.loop:
            self.end = (self.current_frame >= self.total_frames-1)
            self.current_frame = self.current_frame % self.total_frames
        else:
            self.current_frame = min(self.current_frame, self.total_frames-1)
            self.end = (self.current_frame == self.total_frames-1)
        
    
    def get_frame(self):
        return self.spritesheet.get_sprite(self.current_frame)

