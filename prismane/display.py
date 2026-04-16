import pygame as pg

from .entity import Entity
from .panels import InputControlPanel, TimeControlPanel

class Mover(Entity):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.pos.update(x, y)

    def move(self) -> None:
        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]
        game_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]
        dt = game_panel.dt
        self.pos.y -= input_panel.keys_pressed[pg.K_UP] * 500 * dt
        self.pos.y += input_panel.keys_pressed[pg.K_DOWN] * 500 * dt
        self.pos.x += input_panel.keys_pressed[pg.K_RIGHT] * 500 * dt
        self.pos.x -= input_panel.keys_pressed[pg.K_LEFT] * 500 * dt


class Display(Entity):
    def __init__(self, window: pg.Surface, width: int, height: int, **kwargs) -> None:
        super().__init__(True)
        self.window = window
        self.image = pg.Surface((width, height), kwargs["flags"] if "flags" in kwargs else 0)
        self.scale: float = min(self.window.width/self.image.width, self.window.height/self.image.height)
        self.frame: pg.Surface
        self.z = -1

    def update(self) -> None:
        # scales up the display up to the window size.
        self.scale = min(self.window.get_width() / self.image.get_width(), self.window.get_height() / self.image.get_height())
        self.frame = pg.transform.scale_by(self.image, self.scale)
        self.size = self.frame.size
        self.pos.x, self.pos.y = (self.window.get_width() - self.frame.get_width()) // 2, (self.window.get_height() - self.frame.get_height()) // 2

    def queue_draw(self) -> None:
        self.element_tree["Renderer"].queue_draw(self.frame, self.z, self.target, self.pos)

