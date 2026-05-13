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
        self.frames: dict = self.load(spritesheet_json_path)
        self.indexes: dict = { idx: key for idx, key in enumerate(list(self.frames.keys())) }
        
    def load(self, spritesheet_json_path: Path) -> dict:
        frames: dict = {}
        with open(spritesheet_json_path, 'r') as file:
            spritesheet_json = json.load(file)
        
        if spritesheet_json["spritesheet-type"] == "single-image":
            frames = self.load_single_image_type(spritesheet_json)
        elif spritesheet_json["spritesheet-type"] == "directory":
            frames = self.load_directory_type(spritesheet_json)
        else:
            raise Exception(f"Unknown spritesheet type: {spritesheet_json['spritesheet-type']}")

        return frames

    def load_single_image_type(self, spritesheet_json: dict) -> dict:
        image = get_image(Path(spritesheet_json["image-path"]))
        sprites = {}
        for name in spritesheet_json["images"]: 
            rect = spritesheet_json["images"][name]
            sprites[name] = image.subsurface(rect)
        return sprites


    def load_directory_type(self, spritesheet_json: dict):
        sprites: dict = {}
        format_type = spritesheet_json["format-type"]
        directory_path = Path(spritesheet_json["directory-path"])

        if format_type == "formatted":
            format = spritesheet_json["format"]
            sprite_count = spritesheet_json["count"]
            for i in range(sprite_count):
                sprites[format.format(i)] = get_image(directory_path / format.format(i))
        elif format_type == "file-names":
            sprite_names = spritesheet_json["images"]
            for name in sprite_names:
                sprites[name] = get_image(directory_path / name)
        else:
            raise Exception(f"Unknown directory spritesheet type formatting: {format_type}")

        return sprites

    def __getitem__(self, i):
        if i in self.frames:
            return self.frames[i]
        
        if not isinstance(i, int):
            raise Exception(f"`{i}` is not in the spritesheet and is not an index.")

        return self.frames[self.indexes[i]]  # get i-th element from the spritesheet

    def __len__(self):
        return len(self.frames)

class Animation(Entity):
    def __init__(self, spritesheet: Spritesheet, fps: float, initial_frame_index: int = 0, loop: bool = True):
        super().__init__()
        self.spritesheet = spritesheet
        self.total_frames = len(self.spritesheet)
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
        return self.spritesheet[self.current_frame]
