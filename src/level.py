from __future__ import annotations

from prismane import Spritesheet, Entity, EntityGroup, Event

import pygame as pg
from pathlib import Path

from .dialogue import DialogueBox


class LevelEntity(Entity):
    def __init__(self, camera_name, hitbox, collision_type: str = "static", singleton: bool = False) -> None:
        super().__init__(singleton)
        self.camera = self.element_tree[camera_name]
        self.hitbox: pg.FRect = hitbox  # NOTE: hitbox is measured in relation to the top-left corner of the entity (its position)
        self.collision_type = collision_type

    @property
    def collision_box(self) -> pg.FRect:
        return self.hitbox.move(*self.pos)

    def collides_with(self, entity: LevelEntity):
        return self.collision_box.colliderect(entity.collision_box)
    
    def draw(self):
        self.element_tree["Renderer"].queue_draw(self.image, self.z, self.target, pg.Vector2(self.pos[0] - self.camera.scroll[0], self.pos[1] - self.camera.scroll[1]) + self.draw_offset)



class Mushroom(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 166, 114), "mushroom")
        hazards = self.element_tree["AssetLoader"].get_spritesheet(Path("./assets/tiles/hazards.json"))
        self.image = hazards["mushroom"]
        self.pos = pos


class Spike(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 57, 74), "spike")
        hazards = self.element_tree["AssetLoader"].get_spritesheet(Path("./assets/tiles/hazards.json"))
        self.image = hazards["spike"]
        self.pos = pos


class Tile(LevelEntity):
    def __init__(self, pos: pg.Vector2, image: pg.Surface, hitbox: pg.FRect = pg.FRect(0, 0, 0, 0)) -> None:
        super().__init__("MainCamura", hitbox)
        self.size = pg.Vector2(200, 200)
        self.image = image

        self.pos = pos
        self.z = 2

        self.hitbox = hitbox if hitbox else pg.FRect(0, 0, *self.image.get_size())


class Butterfly(LevelEntity):
    def __init__(self, pos: pg.Vector2, orientation: str) -> None:
        super().__init__("MainCamura", pg.FRect(0,0, 170, 179), "butterfly")
        self.image = self.element_tree["AssetLoader"].get_image(Path("./assets/entities/butterfly.png"))
        self.pos = pos

        if orientation == "right":
            self.image = pg.transform.flip(self.image, flip_x=True, flip_y=False)


class Level(Entity):
    def __init__(self, player_start_pos: pg.Vector2) -> None:
        super().__init__()
        self.events: list
        self.groups: dict[str, EntityGroup]
        self.singletons: dict[str, Entity]
        self.player_start_pos = player_start_pos

    def get_collision_with(self, entity: LevelEntity, group: str):
        for level_entity in self.groups[group]:
            if level_entity.collides_with(entity):
                return level_entity
        return None

    def update(self):
        for group in self.groups.values():
            group.update()

        for singletone in self.singletons.values():
            singletone.update()
        
        for event in self.events:
            event.update()

    def draw(self):
        for group in self.groups.values():
            group.draw()

        for singleton in self.singletons.values():
            singleton.draw()


class Level1(Level):
    def __init__(self) -> None:
        super().__init__(pg.Vector2(144, 1169))
        
        w, h = 115, 75  # tile width and tile height, shortened for conveniece in the monstrocity you see below (yes, it was manually written. Every single entry. Every single tile. You could say it woul've been better to write a script to do that for me, but I am too lazy to write the autotiler, and even though it would've taken me 30 minutes I'd rather spend the next 2 hours manually writing everyghing down)
        tileset = Spritesheet(Path("./assets/tiles/pink.json"))
        tile_hitbox = pg.FRect(0, 51, 115, 75)

        self.groups: dict[str, EntityGroup] = {
            "tiles": EntityGroup(
                Tile(pg.Vector2(-1*w, 3*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(0*w, 3*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(-1*w, 9*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(0*w, 9*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(1*w, 9*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(-1*w, 10*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(0*w, 10*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(1*w, 10*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(0*w, 11*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(1*w, 11*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(2*w, 11*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(4*w, 7*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(5*w, 7*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(6*w, 7*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(7*w, 7*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(8*w, 7*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(9*w, 5*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(10*w, 5*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(11*w, 5*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(13*w, 5*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(14*w, 5*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(15*w, 5*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(16*w, 5*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(18*w, 7*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(19*w, 7*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(20*w, 7*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(22*w, 6*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(23*w, 6*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(25*w, 5*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(26*w, 5*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(15*w, 10*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(16*w, 10*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(24*w, 11*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(25*w, 11*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(26*w, 11*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(27*w, 11*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(4*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(5*w, 17*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(10*w, 15*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(11*w, 15*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(12*w, 15*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(17*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(18*w, 17*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(19*w, 17*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(20*w, 17*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(21*w, 17*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(22*w, 17*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(1*w, 18*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(2*w, 18*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(1*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(2*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(7*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(8*w, 17*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(9*w, 17*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(7*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(8*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(9*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(7*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(8*w, 19*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(9*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(12*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(13*w, 17*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(13*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(14*w, 18*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(15*w, 18*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(13*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(14*w, 19*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(15*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(24*w, 18*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(25*w, 18*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(26*w, 18*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(24*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(25*w, 19*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(26*w, 19*h+tile_hitbox.y), tileset["bottom-right"])
            ),
            "mushrooms": EntityGroup(
                # MUSHROOMs
                Mushroom(pg.Vector2(4*w, 6*h+10)),
                Mushroom(pg.Vector2(4*w, 16*h+10)),
                Mushroom(pg.Vector2(11.75*w, 14*h+10)),
            ),
            "spikes": EntityGroup(
                # Spikes
                Spike(pg.Vector2(11*w+40, 4*h+50)),
                Spike(pg.Vector2(18*w+40, 6*h+50)),
                Spike(pg.Vector2(11*w+40, 14*h+50)),
            ),
            "butterflies": EntityGroup(
                # Butterflies
                Butterfly(pg.Vector2(-1*w-10, 2*h-50), orientation="right"),
                Butterfly(pg.Vector2(26*w-10, 4*h-50), orientation="left"),
                Butterfly(pg.Vector2(16*w-10, 9*h-50), orientation="left"),
            )
        }

        self.singletons = {}
        self.dialogue_termination_event = None

    def start_dialogue(self, dialogue_json_path: Path):
        self.dialogue = DialogueBox(dialogue_json_path)
        self.dialogue_termination_event = Event(action=lambda: self.stop_dialogue(), condition=lambda: self.dialogue.end)
        
        self.events.append(
            self.dialogue_termination_event
        )

    def stop_dialogue(self):
        if self.dialogue:
            self.dialogue.destroy()
            self.entities.remove(self.dialogue)
            self.dialogue = None

        if self.dialogue_termination_event:
            self.events.remove(self.dialogue_termination_event)
            self.dialogue_termination_event.destroy()
            self.dialogue_termination_event = None

    def update(self):
        super().update()

        if self.dialogue:
            self.dialogue.update()

    def draw(self):
        super().draw()

        if self.dialogue:
            self.dialogue.draw()

