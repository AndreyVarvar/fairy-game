from .element import Element
from .assets import AssetLoader

from pathlib import Path
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
        image = self.element_tree["AssetLoader"].get_image(Path(spritesheet_json["image-path"]))
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
                sprites[format.format(i)] = self.element_tree["AssetLoader"].get_image(directory_path / format.format(i))
        elif format_type == "file-names":
            sprite_names = spritesheet_json["images"]
            for name in sprite_names:
                sprites[name] = self.element_tree["AssetLoader"].get_image(directory_path / name)
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

