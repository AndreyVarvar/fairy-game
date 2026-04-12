import pygame as pg

from .settings import *
from .display import Display
from prismane import Element
# use MasterControlPanel from prismane for the mouse thingy

def ease_in_quart(x) -> float:
    return pg.math.clamp(x * x * x * x, 0, 1)

class Camera(Element):
    def __init__(self, top: int, left: int, bottom: int, right: int) -> None:
        super().__init__()
        self.display: Display = self.element_tree["Display"]
        self.bound_rect: pg.FRect = pg.FRect(left, top, self.display.image.width - left - right, self.display.image.height - top - bottom)
        self.view_rect: pg.FRect = pg.FRect(0, 0, self.display.image.width, self.display.image.height)

        self.target_sprite = None
        self.target_pos = None

        self.scroll: pg.Vector2 = pg.Vector2()

    @property
    def target(self) -> pg.typing.Point:
        if self.target_sprite:
            return self.target_sprite.center
        elif self.target_pos:
            return self.target_pos
        else:
            return (self.display.image.width//2, self.display.image.height//2)

    @target.setter
    def target(self, value) -> None:
        if hasattr(value, "center"):
            self.target_sprite = value
            self.target_pos = None
        elif hasattr(value, "pos"):
            self.target_sprite = None
            self.target_pos = value
        else:
            self.target_pos = (self.display.image.width//2, self.display.image.height//2)

    def follow_target(self, dt: float) -> None:
        self.view_rect.center = self.target
        self.bound_rect.center = self.view_rect.center
        self.scroll.x += (self.bound_rect.x - self.scroll.x)
        self.scroll.y += (self.bound_rect.y - self.scroll.y)

    @property
    def mouse_pos_in_world(self) -> tuple[float, float]:
        mouse_display_pos = self.element_tree["Mouse"].display_pos
        return mouse_display_pos[0] + self.bound_rect.x, mouse_display_pos[1] + self.bound_rect.y

