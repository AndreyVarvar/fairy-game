import pygame as pg
import pathlib



assets = {
    "spritesheets": {},
    "images": {},
    "sounds": {}
}


def get_spritesheet(path: pathlib.Path):
    load_spritesheet(path)
    return assets["spritesheets"][path.name]

def load_spritesheet(path: pathlib.Path):
    from .spritesheet import Spritesheet  # to stop circular import. Sadly, no type annotations :(
    if path.name not in assets["spritesheets"]:
        assets["spritesheets"][path.name] = Spritesheet(path)

# TODO: somehow make this incorporate the "from dir" thing
def get_image(path: pathlib.Path) -> pg.Surface:
    load_image(path)
    return assets["images"][path.stem]

def load_image(path: pathlib.Path):
    if path.name not in assets["images"]:
       assets["images"][path.stem] = pg.image.load(path).convert_alpha()
