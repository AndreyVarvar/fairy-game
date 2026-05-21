import pygame as pg
import pathlib

from .element import Element
from .settings import Settings


class AssetLoader(Element):
    def __init__(self):
        super().__init__(singleton=True)
        
        self.assets = {
            "spritesheets": {},
            "images": {},
            "sounds": {}
        }

    def get_spritesheet(self, path: pathlib.Path):
        self.load_spritesheet(path)
        return self.assets["spritesheets"][str(path)]

    def load_spritesheet(self, path: pathlib.Path):
        from .spritesheet import Spritesheet  # to stop circular import. Sadly, no type annotations :(
        if str(path) not in self.assets["spritesheets"]:
            self.assets["spritesheets"][str(path)] = Spritesheet(path)

    # TODO: somehow make this incorporate the "from dir" thing
    def get_image(self, path: pathlib.Path) -> pg.Surface:
        self.load_image(path)
        return self.assets["images"][str(path)]

    def load_image(self, path: pathlib.Path):
        if str(path) not in self.assets["images"]:
            self.assets["images"][str(path)] = pg.image.load(path).convert_alpha()
