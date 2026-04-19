from prismane import Entity, EntityGroup
import pygame as pg



class Tile(Entity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__()

        self.size = pg.Vector2(200, 200)
        self.image = pg.Surface(self.size)
        self.image.fill("white")

        self.pos = pos
        self.z = 2


class Level(Entity):
    def __init__(self) -> None:
        super().__init__()
        
        self.entities: EntityGroup = EntityGroup(
            Tile(pg.Vector2(0, 1000)),
            Tile(pg.Vector2(200, 1000)),
            Tile(pg.Vector2(400, 1000)),
            Tile(pg.Vector2(600, 1000)),
            Tile(pg.Vector2(800, 1000)),
            Tile(pg.Vector2(1000, 1000)),
            Tile(pg.Vector2(1200, 1000)),
        )

    def get_collision_with(self, entity: Entity):
        for level_entity in self.entities:
            if level_entity.collides_with(entity):
                return level_entity
        return None

    def update(self):
        self.entities.update()

    def queue_draw(self):
        self.entities.queue_draw()
