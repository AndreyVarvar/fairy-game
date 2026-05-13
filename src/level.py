from __future__ import annotations

from prismane import Spritesheet
from prismane import Entity, EntityGroup
import pygame as pg
from pathlib import Path




class LevelEntity(Entity):
    def __init__(self, camera_name, hitbox, singleton: bool = False) -> None:
        super().__init__(singleton)
        self.camera = self.element_tree[camera_name]
        self.hitbox: pg.FRect = hitbox  # NOTE: hitbox is measured in relation to the top-left corner of the entity (its position)

    @property
    def collision_box(self) -> pg.FRect:
        return self.hitbox.move(*self.pos)

    def collides_with(self, entity: LevelEntity):
        return self.collision_box.colliderect(entity.collision_box)
    
    def draw(self):
        self.element_tree["Renderer"].queue_draw(self.image, self.z, self.target, pg.Vector2(self.pos[0] - self.camera.scroll[0], self.pos[1] - self.camera.scroll[1]) + self.draw_offset)



class Tile(LevelEntity):
    def __init__(self, pos: pg.Vector2, image: pg.Surface, hitbox: pg.FRect = pg.FRect(0, 0, 0, 0)) -> None:
        super().__init__("MainCamura", hitbox)
        self.size = pg.Vector2(200, 200)
        self.image = image
        self._image = image

        self.pos = pos
        self.z = 2

        self.hitbox = hitbox if hitbox else pg.FRect(0, 0, *self.image.get_size())
    
    def update(self):
        super().update()
        self.image = self._image.copy()
        pg.draw.rect(self.image, (255, 0, 0), self.hitbox, 5)



class Level(Entity):
    def __init__(self, entities: EntityGroup) -> None:
        super().__init__()
        
        self.entities: EntityGroup = entities

    def get_collision_with(self, entity: LevelEntity):
        for level_entity in self.entities:
            if level_entity.collides_with(entity):
                return level_entity
        return None

    def update(self):
        self.entities.update()

    def draw(self):
        self.entities.draw()


class Level1(Level):
    def __init__(self) -> None:
        w, h = 115, 126  # tile width and tile height, shortened for conveniece in the monstrocity you see below (yes, it was manually written. Every single entry. Every single tile. You could say it woul've been better to write a script to do that for me, but I am too lazy to write the autotiler, and even though it would've taken me 30 minutes I'd rather spend the next 2 hours manually writing everyghing down)
        tileset = Spritesheet(Path("./assets/tiles/pink.json"))
        entities: EntityGroup = EntityGroup(
            Tile(pg.Vector2(0*w, 3*h), tileset["top-left"], pg.FRect(0, 10, 115, 116))
        )
        super().__init__(entities)

