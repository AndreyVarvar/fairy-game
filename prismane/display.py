import pygame as pg

from .element import Element


class Display(Element):
    def __init__(self, window: pg.Surface, width: int, height: int, **kwargs) -> None:
        super().__init__(singleton=True)
        self.window = window
        self.image = pg.Surface((width, height), kwargs["flags"] if "flags" in kwargs else 0)
        self.size = pg.Vector2()
        self.pos = pg.Vector2()
        self.scale: float = min(self.window.width/self.image.width, self.window.height/self.image.height)
        self.frame: pg.Surface
        self.z = -1

    def update(self) -> None:
        # scales up the display up to the window size.
        self.scale = min(self.window.get_width() / self.image.get_width(), self.window.get_height() / self.image.get_height())
        self.frame = pg.transform.scale_by(self.image, self.scale)
        self.pos.x, self.pos.y = (self.window.get_width() - self.frame.get_width()) // 2, (self.window.get_height() - self.frame.get_height()) // 2
        self.size.update(*self.frame.size)

    def queue_draw(self) -> None:
        self.element_tree["Renderer"].queue_draw(self.frame, self.z, "window", self.pos)

