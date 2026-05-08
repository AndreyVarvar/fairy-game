from prismane import Entity
from prismane import TimeControlPanel, InputControlPanel
from prismane.animation import DirectorySpritesheet
from prismane.assets import get_image
from prismane.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from prismane import Animation, DirectorySpritesheet
from prismane import Event

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
        self.on_ground = False

        self.states = {
            "idle left": Animation(DirectorySpritesheet(Path("assets/entities/models/idle_l"), "Timeline 1_{0:04}.png", 22), 10),
            "idle right": Animation(DirectorySpritesheet(Path("assets/entities/models/idle_r"), "Timeline 1_{0:04}.png", 22), 10),
            "walk left": Animation(DirectorySpritesheet(Path("assets/entities/models/walk_l"), "Timeline 1_{0:04}.png", 20), 10),
            "walk right": Animation(DirectorySpritesheet(Path("assets/entities/models/walk_r"), "Timeline 1_{0:04}.png", 20), 10),
            "jump left": Animation(DirectorySpritesheet(Path("assets/entities/models/jump_left"), "Timeline 1_{0:04}.png", 13), 10, loop=False),
            "jump right": Animation(DirectorySpritesheet(Path("assets/entities/models/jump_right"), "Timeline 1_{0:04}.png", 13), 10, loop=False),
        }
        self.current_state = "idle left"
        self.facing = "left"
        # conditions for switching from state A to state B
        self.switch_conditions = [
            Event(action=lambda: self.set_state("walk left"), condition=lambda: self.on_ground and self.velocity.x < 0),
            Event(action=lambda: self.set_state("walk right"), condition=lambda: self.on_ground and self.velocity.x > 0),
            Event(action=lambda: self.set_state("idle left"), condition=lambda: self.velocity.x == 0 and self.facing == "left" and self.on_ground),
            Event(action=lambda: self.set_state("idle right"), condition=lambda: self.velocity.x == 0 and self.facing == "right" and self.on_ground),
            Event(action=lambda: [self.states["jump left"].reset() if self.current_state != "jump left" else None, self.set_state("jump left")], condition=lambda: self.velocity.y < 0 and not self.on_ground and self.facing == "left"),
            Event(action=lambda: [self.states["jump right"].reset() if self.current_state != "jump right" else None, self.set_state("jump right")], condition=lambda: self.velocity.y < 0 and not self.on_ground and self.facing == "right"),
        ]

        self.image = self.states[self.current_state].get_frame()  # TODO: currenly player hitbox is tied to image

        self.z = 1
        self.size = pg.Vector2(self.image.get_size())

    def set_state(self, state: str):
        self.current_state = state

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
        # animations
        self.states[self.current_state].update()
        self.image = self.states[self.current_state].get_frame()

        # movement
        self.acceleration = pg.Vector2(0, 0)
        self.acceleration += self.gravity
        
        self.process_input()

        dt = self.element_tree["TimeControlPanel"].dt
        self.velocity += self.acceleration * dt  # acceleration
        if self.on_ground:
            self.velocity.x /= 5**dt
    
        # collision
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
        

        if abs(self.velocity.x) < 10:
            self.velocity.x = 0
        self.velocity.clamp_magnitude_ip(10_000)

        if self.velocity.x != 0:
            if self.velocity.x > 0:
                self.facing = "right"
            else:
                self.facing = "left"

        # states
        for event in self.switch_conditions:
            event.update()
