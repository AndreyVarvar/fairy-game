from prismane import Entity
from prismane import TimeControlPanel, InputControlPanel
from prismane.assets import get_image
from prismane.settings import WINDOW_HEIGHT, WINDOW_WIDTH

from .level import Level, LevelEntity

from pathlib import Path

import pygame as pg

class Player(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__(camera_name="MainCamura")
        self.pos = pos
        self.velocity: pg.Vector2 = pg.Vector2(0, 0)
        self.acceleration: pg.Vector2 = pg.Vector2(0, 0)

        self.gravity: pg.Vector2 = pg.Vector2(0, 2000)

        self.image = get_image(Path("assets/entities/fairy.png"))
        self.z = 1
        self.size = pg.Vector2(self.image.get_size())

        self.on_ground = False

    def process_input(self):
        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]

        input_acceleration = pg.Vector2(0, 0)

        accel = 5000

        if input_panel.keys_pressed[pg.K_d]:
            input_acceleration.x = accel
        if input_panel.keys_pressed[pg.K_a]:
            input_acceleration.x = -accel

        if abs(self.velocity.x) < 1000 or input_acceleration.x * self.velocity.x < 0:
            self.acceleration += input_acceleration

        if pg.K_SPACE in input_panel.keys_just_pressed and self.on_ground:
            self.velocity.y = -1000

    def update(self):
        self.acceleration = pg.Vector2(0, 0)
        self.acceleration += self.gravity
        
        self.process_input()

        dt = self.element_tree["TimeControlPanel"].dt
        self.velocity += self.acceleration * dt  # acceleration
        if self.on_ground:
            self.velocity.x /= 5**dt

        level: Level = self.element_tree["CurrentStage"].groups["level"][0]
        
        self.pos.x += self.velocity.x * dt
        entity = level.get_collision_with(self)
        if entity is not None:
            if self.velocity.x > 0:
                self.pos.x = entity.rect.left - self.rect.width
            else:
                self.pos.x = entity.rect.right
            self.velocity.x = 0
            self.acceleration.x = 0


        self.pos.y += self.velocity.y * dt
        self.on_ground = False
        entity = level.get_collision_with(self)
        if entity is not None:
            if self.velocity.y >= 0:
                self.on_ground = True
                self.pos.y = entity.rect.top - self.rect.height
            else:
                self.pos.y = entity.rect.bottom
            self.velocity.y = 0
            self.acceleration.y = 0
        

        self.velocity.clamp_magnitude_ip(10_000)
