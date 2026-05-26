import pygame as pg
from pygame._sdl2.video import Renderer, Texture
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

    def texture_from_surface(self, surf: pg.Surface, renderer: Renderer | None = None):
        renderer = renderer if renderer else self.element_tree["Engine"].window_renderer  # default renderer is the window renderer
        
        return Texture.from_surface(renderer, surf)

    def get_spritesheet(self, path: pathlib.Path):
        self.load_spritesheet(path)
        return self.assets["spritesheets"][str(path)]

    def load_spritesheet(self, path: pathlib.Path):
        from .spritesheet import Spritesheet  # to stop circular import. Sadly, no type annotations :(
        if str(path) not in self.assets["spritesheets"]:
            self.assets["spritesheets"][str(path)] = Spritesheet(path)

    # TODO: somehow make this incorporate the "from dir" thing
    def get_image(self, path: pathlib.Path, renderer: Renderer | None = None, transparent: bool = True) -> pg.Surface:
        renderer = renderer if renderer else self.element_tree["Engine"].window_renderer  # default renderer is the window renderer
        self.load_image(path, renderer, transparent)

        return self.assets["images"][str(path)]

    def load_image(self, path: pathlib.Path, renderer: Renderer, transparent: bool):
        if str(path) not in self.assets["images"]:
            if transparent:
                self.assets["images"][str(path)] = Texture.from_surface(renderer, pg.image.load(path))
            else:
                self.assets["images"][str(path)] = Texture.from_surface(renderer, pg.image.load(path).convert())
