from prismane import Entity, EntityGroup, camera
import pygame as pg



class LevelEntity(Entity):
    def __init__(self, camera_name, singleton: bool = False) -> None:
        super().__init__(singleton)
        self.camera = self.element_tree[camera_name]

    def draw(self):
        self.element_tree["Renderer"].queue_draw(self.image, self.z, self.target, [self.pos[0] - self.camera.scroll[0], self.pos[1] - self.camera.scroll[1]])



class Tile(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__(camera_name="MainCamura")

        self.size = pg.Vector2(200, 200)
        self.image = pg.Surface(self.size)
        self.image.fill("white")

        self.pos = pos
        self.z = 2



class Level(Entity):
    def __init__(self) -> None:
        super().__init__()
        
        self.entities: EntityGroup = EntityGroup(
            Tile(pg.Vector2(600, 600)),
            Tile(pg.Vector2(400, 800)),
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

    def draw(self):
        self.entities.draw()
