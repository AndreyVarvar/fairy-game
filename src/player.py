from prismane import Entity
from prismane import TimeControlPanel, InputControlPanel
from prismane.assets import get_image

from .level import Level

from pathlib import Path

import pygame as pg

class Player(Entity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__()
        self.pos = pos
        self.velocity: pg.Vector2 = pg.Vector2(0, 0)
        self.acceleration: pg.Vector2 = pg.Vector2(0, 0)

        self.gravity: pg.Vector2 = pg.Vector2(0, 100)

        self.image = get_image(Path("assets/entities/fairy.png"))
        self.z = 1
        self.size = pg.Vector2(self.image.get_size())

    def input(self):
        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]

        input_acceleration = pg.Vector2(0, 0)

        accel = 100

        if input_panel.keys_pressed[pg.K_d]:
            input_acceleration.x = accel
        if input_panel.keys_pressed[pg.K_a]:
            input_acceleration.x = -accel

        if abs(self.acceleration.x) < 10 or input_acceleration.x * self.velocity.x < 0:
            self.acceleration += input_acceleration

    def update(self):
        self.acceleration += self.gravity
        
        dt = self.element_tree["TimeControlPanel"].dt
        self.velocity += self.acceleration * dt

        level: Level = self.element_tree["CurrentStage"].groups["level"][0]

        self.input()
        
        self.pos.x += self.velocity.x * dt
        entity = level.get_collision_with(self)
        if entity is not None:
            self.velocity.x = 0
            self.acceleration.x = 0
            if self.velocity.x > 0:
                self.pos.x = entity.rect.left - self.rect.width
            else:
                self.pos.x = entity.rect.right


        self.pos.y += self.velocity.y * dt
        entity = level.get_collision_with(self)
        if entity is not None:
            self.velocity.y = 0
            self.acceleration.y = 0
            if self.velocity.y >= 0:
                self.pos.y = entity.rect.top - self.rect.height
            else:
                self.pos.y = entity.rect.bottom
        

