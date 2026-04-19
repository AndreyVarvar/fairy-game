from prismane import Entity
from prismane import TimeControlPanel

import pygame as pg

class Player(Entity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__()
        self.pos = pos
        self.velocity: pg.Vector2 = pg.Vector2(0, 0)
        self.acceleration: pg.Vector2 = pg.Vector2(0, 0)

        self.gravity: pg.Vector2 = pg.Vector2(0, 100)

        self.image = pg.Surface((200, 100))
        self.image.fill("yellow")

    def update(self):
        self.acceleration += self.gravity
        
        dt = self.element_tree["TimeControlPanel"].dt
        self.velocity += self.acceleration * dt
        self.pos += self.velocity * dt


        

