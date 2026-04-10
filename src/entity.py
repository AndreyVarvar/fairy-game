import pygame as pg

from prismane import Element


class Entity(Element):
    def __init__(self, singleton: bool = False) -> None:
        super().__init__(singleton)
        self.pos: pg.Vector2 = pg.Vector2()
        self.size: pg.typing.Point = [0, 0]
        self.image: pg.Surface
        self.target: str = "window"
        self.z: int = 0

    @property
    def center(self) -> pg.typing.Point:
        return self.rect.center

    @property
    def rect(self) -> pg.FRect:
        return pg.FRect(*self.pos, *self.size)

    def update(self, *args, **kwargs):
        pass

    def blit(self):
        self.element_tree["Renderer"].blit(self.z, self.target, self.image, self.pos)


class EntityGroup(Element):
    def __init__(self, *entities: Entity) -> None:
        super().__init__()
        self.entities: list[Entity] = list(entities)

    def blit(self) -> None:
        for entity in self.entities:
            entity.blit()

    def __iter__(self):
        for entity in self.entities:
            yield entity
