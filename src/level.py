from __future__ import annotations

from prismane import Entity, EntityGroup

import pygame as pg


class LevelEntity(Entity):
    def __init__(self, camera_name, hitbox, collision_type: str = "static", singleton: bool = False) -> None:
        super().__init__(singleton)
        self.camera = self.element_tree[camera_name]
        self.hitbox: pg.FRect = hitbox  # NOTE: hitbox is measured in relation to the top-left corner of the entity (its position)
        self.collision_type = collision_type

    @property
    def collision_box(self) -> pg.FRect:
        return self.hitbox.move(self.pos)

    def collides_with(self, entity: LevelEntity):
        return self.collision_box.colliderect(entity.collision_box)

    def collidepoint(self, point):
        return self.collision_box.collidepoint(point)

    def draw(self):
        self.draw_offset -= pg.Vector2(self.camera.scroll)
        super().draw()
        self.draw_offset += pg.Vector2(self.camera.scroll)





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

    def collidepoint(self, point, group):
        for level_entity in self.groups[group]:
            if level_entity.collidepoint(point):
                return level_entity
        return None

    def update(self):
        for group in self.groups.values():
            group.update()

        for singleton in list(self.singletons.values()):
            singleton.update()
        
        for event in self.events:
            event.update()

    def draw(self):
        for group in self.groups.values():
            group.draw()

        for singleton in self.singletons.values():
            singleton.draw()


