import pygame as pg

from .element import Element


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

    def update(self):
        # for all input, sound, or music related stuff (+dt and game_running_time) use "InputControlPanel", "SoundControlPanel", and "MusicControlPanel" (+"GameControlPanel")
        pass

    def queue_draw(self):
        self.element_tree["Renderer"].queue_draw(self.image, self.z, self.target, self.pos)


class EntityGroup(Element):
    def __init__(self, *entities: Entity) -> None:
        super().__init__()
        self.entities: list[Entity] = list(entities)
        self.queue = []

    def add(self, *entities: Entity):
        for entity in entities:
            self.queue.append(entity)

    def queue_draw(self) -> None:
        for entity in self.entities:
            entity.queue_draw()

    def update(self) -> None:
        # NOTE: we should make this work with chunks
        for entity in self.entities:
            entity.update()

        for entity in self.queue:
            self.entities.append(entity)

    def __iter__(self):
        for entity in self.entities:
            yield entity

    def __getitem__(self, index):
        return self.entities[index]
