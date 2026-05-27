from __future__ import annotations
import pygame as pg
import pygame._sdl2 as sdl2

from .renderer import Renderer

from .element import Element


class Entity(Element):
    def __init__(self, singleton: bool = False) -> None:
        super().__init__(singleton)
        self.pos: pg.Vector2 = pg.Vector2(0, 0)
        self.size: pg.Vector2 = pg.Vector2(0, 0)
        self.image: sdl2.Texture
        self.z: int = 1
        self.draw_offset: pg.Vector2 = pg.Vector2(0, 0)

        # stuff related to rendering
        self.source: pg.Rect = None
        self.flip_x: bool = False
        self.flip_y: bool = False
        self.angle: float = 0.0
        self.pivot: tuple[int, int] | pg.Vector2 = None

    @property
    def center(self) -> tuple[float, float]:
        return self.frect.center

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)
    
    @property
    def frect(self) -> pg.FRect:
        return pg.FRect(self.pos, self.size)

    def update(self):
        # for all input, sound, or music related stuff (+dt and game_running_time) use "InputControlPanel", "SoundControlPanel", and "MusicControlPanel" (+"GameControlPanel")
        pass

    def draw(self):
        renderer: Renderer = self.element_tree["Renderer"]
        renderer.queue_draw(
            texture=self.image, 
            z=self.z, 
            source=self.source, 
            destination=self.frect.move(self.draw_offset), 
            flip_x=self.flip_x, 
            flip_y=self.flip_y, 
            angle=self.angle, 
            pivot=self.pivot
        )


class EntityGroup(Element):
    def __init__(self, *entities: Entity) -> None:
        super().__init__()
        self.entities: list[Entity] = list(entities)
        self.queue = []

    def add(self, *entities: Entity):
        for entity in entities:
            self.queue.append(entity)

    def remove(self, entity: Entity):
        self.entities.remove(entity)

    def draw(self) -> None:
        for entity in self.entities:
            entity.draw()

    def update(self) -> None:
        # NOTE: we should make this work with chunks
        for entity in self.entities:
            entity.update()

        for entity in self.queue:
            self.entities.append(entity)
        self.queue.clear()

    def __iter__(self):
        for entity in self.entities:
            yield entity

    def __repr__(self):
        return str(self.entities)

    def __str__(self):
        return str(self.entities)

    def __getitem__(self, index):
        return self.entities[index]

    def __len__(self):
        return len(self.entities)
