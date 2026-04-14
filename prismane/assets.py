import pygame as pg
import pathlib, json

from .settings import *


images = {
    "spritesheets": {},
    "tilesets": {}
}
data = {
    "spritesheets": {},
    "tilesets": {}
}


# TODO: somehow make this incorporate the "from dir" thing
def get_image(path: pathlib.Path) -> pg.Surface:
    load_image(path)
    return images[path.stem]


def load_image(path: pathlib.Path):
    if path.name not in images:
        images[path.stem] = pg.image.load(path).convert_alpha()

def clip_img(surf, x: int, y: int, width: int, height: int):
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())

def load_images_from_dir(path: pathlib.Path):
    path.iterdir()
    image_paths = [i for i in path.iterdir() if i.is_file()]

    for image_path in image_paths:
        load_image(image_path)

def is_transparent(surface: pg.Surface):
    for y in range(0, surface.get_height()):
        for x in range(0, surface.get_width()):
            if surface.get_at((x, y))[3] > 0:
                return False
    return True

def load_tileset_from_dir(path: pathlib.Path):
    tileset_data = {}

    with open(str(path / "data.json"), "r") as f:
        tileset_data = json.load(f)

    tile_size = tileset_data["tile_size"]

    tileset = {}
    tileset_image = pg.image.load(path / "spritesheet.png").convert_alpha()
    for y in range(0, tileset_image.get_height(), tile_size[1]):
        for x in range(0, tileset_image.get_width(), tile_size[0]):
            img = clip_img(tileset_image, x, y, tile_size[0], tile_size[1])
            if not is_transparent(img):
                tileset[y//tile_size[1] * tileset_image.get_width()//tile_size[0] + x//tile_size[0]] = img

    data["tilesets"].update({tileset_data["id"]: tileset_data})
    images["tilesets"].update({tileset_data["id"]: tileset})

def load_spritesheet_from_dir(path: pathlib.Path):
    spritesheet_data = {}

    with open(str(path / "data.json"), "r") as f:
        spritesheet_data = json.load(f)

    spritesheet = {}
    spritesheet_image = pg.image.load(path / "spritesheet.png").convert_alpha()
    for sprite_id, sprite in spritesheet_data["sprites"].items():
        outline = sprite["outline"]
        x = outline["x"]
        y = outline["y"]
        w = outline["w"]
        h = outline["h"]
        spritesheet[sprite_id] = clip_img(spritesheet_image, x, y, w, h)

    data["spritesheets"].update({spritesheet_data["id"]: spritesheet_data})
    images["spritesheets"].update({spritesheet_data["id"]: spritesheet})

