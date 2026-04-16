import pygame as pg
import json

from .settings import *
from .assets import images, data
from .common import *
from .renderer import Renderer
from .entity import Entity
from .camera import Camera

def tuple_to_json_pos(coord: tuple[int, int]) -> str:
    return f"{coord[0]};{coord[1]}"

def json_to_tuple_pos(coord: str) -> tuple[int, int]:
    x, y = map(int, coord.split(";"))
    return (x, y)

def convert_pos_to(level_data, convert):
    for layer in level_data["layers"].values():
        layer["chunks"] = {convert(chunk_coord): chunk for chunk_coord, chunk in layer["chunks"].items()}
        for chunk_coord in layer["chunks"]:
            layer["chunks"][chunk_coord] = {convert(tile_coord): tile for tile_coord, tile in layer["chunks"][chunk_coord].items()}


class Level(Entity):
    def __init__(self, file_path: str, camera: Camera) -> None:
        super().__init__()
        self.file = str(file_path)
        self.camera = camera

        self.level_data = {
            "start_pos": [0, 0], # Top and left most tile coordinate
            "height": 0, # Height of world in tiles
            "width": 0, # Width of world in tiles
            "layers": {},
        }

        # Layer anatomy
        # z: {
        #     "chunks": {chunks},
        #     "is_visible": True,
        #     "has_collisions": True,
        # }

        # Tile anatomy
        # (x, y): "type" "id" "spritesheet_id" "off_set" (for tiles that don't exactly fit the grid)

        # Chunk anatomy
        # (x, y): {
        #       tiles (off grid and on grid)
        #     }

        try:
            with open(self.file, "r") as f:
                self.level_data = json.load(f)
        except:
            print(f"Level {self.file} doesn't exist")
            self.level_data["tile_size"] = TILE_SIZE
            self.level_data["chunk_size"] = CHUNK_SIZE
            # with open(self.file, "w") as f:
            #     json.dump(self.level_data, f)


        # changes all the keys from strings to tuples
        convert_pos_to(self.level_data, json_to_tuple_pos)

        # self.level_rects = self.get_level_rects()
        # self.on_grid_tiles = {layer_id: set(layer["tiles"]) for layer_id, layer
        #                       in self.level_data["layers"].items() if
        #                       layer["on_grid"]}
        #
        # self.layer_ids = sorted(list(self.level_data["layers"].keys()), key= lambda x: int(x))

        self.target = "display"

    def get_tile_pos_at(self, x, y) -> tuple[int, int]:
        tile_size = self.level_data["tile_size"]
        return int(x//tile_size[0]), int(y//tile_size[1])

    def get_chunk_pos_at(self, x, y) -> tuple[int, int]:
        chunk_size = self.level_data["chunk_size"]
        return int(x//chunk_size), int(y//chunk_size)

    def greedy_horizontal_merger(self):
        rects = {}
        #FIXME: get rid of this var
        chunk_size = self.level_data["chunk_size"]
        start_x, start_y = self.level_data["start_pos"]
        end_x, end_y = start_x + self.level_data["width"], start_y + self.level_data["height"]

        visited = {(j, i): False for i in range(start_y, end_y) for j in range(start_x, end_x)}

        for layer_id, layer in self.level_data["layers"].items():
            if not layer["has_collisions"]:
                continue

            rects[layer_id] = {}

            for i in range(start_y, end_y):
                for j in range(start_x, end_x):
                    tile_pos = (j, i)
                    chunk_pos = self.get_chunk_pos_at(*tile_pos)

                    chunk = layer["chunks"].get(chunk_pos)
                    if not chunk:
                        visited[tile_pos] = True
                        continue
                    tile = chunk["on_grid_tiles"].get(tile_pos)

                    if visited[tile_pos] or not (chunk and tile):
                        visited[tile_pos] = True
                        continue

                    rect_width = 1
                    rect_height = 1

                    next_tile_pos = (j + rect_width, i)
                    next_chunk_pos = self.get_chunk_pos_at(*next_tile_pos)

                    next_chunk = layer["chunks"].get(next_chunk_pos)
                    next_tile = next_chunk["on_grid_tiles"].get(next_tile_pos)

                    while rect_width + j < end_x and next_chunk and next_tile and not visited[(j + rect_width, i)]:
                        rect_width += 1

                    while i + rect_height < end_y:
                        valid = True
                        k = j
                        while k < j + rect_width:
                            next_tile_pos = (i + rect_height, k)
                            next_chunk_pos = self.get_chunk_pos_at(*next_tile_pos)

                            next_chunk = layer["chunks"].get(next_chunk_pos)
                            next_tile = next_chunk["on_grid_tiles"].get(next_tile_pos)

                            if visited[(i + rect_height, k)] or not (next_chunk and next_tile):
                                valid = False
                                break
                            k += 1
                        if not valid:
                            break
                        rect_height += 1

                    for k in range(i, i + rect_height):
                        for l in range(j, j +rect_width):
                            visited[(l, k)] = True

                    # Real cursed
                    rect = pg.FRect(j, i, rect_width, rect_height)
                    rects[layer_id].update(
                            dict.fromkeys(
                                [(l, k) for k in range(i, i + rect_height) for l in range(j, j + rect_width)], rect
                                )
                            )

        return rects

    def get_off_grid_tiles(self):
        rects = {}

        for layer_id, layer in self.level_data["layers"]:
            if layer["on_grid"] or not layer["has_collisions"]:
                continue

            rects[layer_id] = {}

            for tile_pos, tile in layer["tiles"].items():
                spritesheet_id = tile["spritesheet_id"]
                tile_id = tile["spritesheet_id"]
                tile_rect = data[spritesheet_id]["sprites"][tile_id]["rect"]
                x = round(tile_pos[0], 3) + tile_rect["x"]
                y = round(tile_pos[1], 3) + tile_rect["y"]
                w = tile_rect["w"]
                h = tile_rect["h"]
                rects[layer_id].update({tile_id: pg.FRect(x, y, w, h)})

        return rects

    def get_level_rects(self):
        rects = self.greedy_horizontal_merger()
        rects.update(self.get_off_grid_tiles())
        return rects

    @property
    def drawing_area(self):
        area = {}

        # Drawing area anatomy
        # area = {
        #         layer_id: {
        #             chunk_id_1, chunk_id_2, chunk_id_3
        #             }
        #         }

        chunk_size = self.level_data["chunk_size"]

        start_pos = self.get_chunk_pos_at(*self.get_tile_pos_at(*self.camera.bound_rect.topleft))
        end_pos = self.get_chunk_pos_at(*self.get_tile_pos_at(self.camera.bound_rect.x + DISPLAY_WIDTH, self.camera.bound_rect.y + DISPLAY_HEIGHT))

        positions = {(x, y) for y in range(start_pos[1], end_pos[1] + 1) for x in range(start_pos[0], end_pos[0] + 1)}

        for layer_id, layer in self.level_data["layers"].items():
            if layer["is_visible"] == True:
               area[layer_id] = positions & layer["chunks"].keys()

        return area

    def blit(self) -> None:
        tile_size = self.level_data["tile_size"]
        for layer_id, layer in self.drawing_area.items():
            for chunk_id in layer:
                for tile_pos, tile in self.level_data["layers"][layer_id]["chunks"][chunk_id].items():
                    image = images["tilesets"][tile["spritesheet_id"]][tile["id"]]
                    self.objects["Renderer"].blit(int(layer_id), self.target, image, (tile_pos[0] * tile_size[0] - self.camera.scroll[0], tile_pos[1] * tile_size[1] - self.camera.scroll[1]))

