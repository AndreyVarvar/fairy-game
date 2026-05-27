from .element import Element

import pygame as pg

# TODO: dynamic access of window and logical size
class Settings(Element):
    def __init__(self) -> None:
        super().__init__(singleton=True)
        self.full_screen = True
        self.mouse_visible = True
        self.max_fps = 60

    @property
    def scale(self) -> pg.Vector2:
        return pg.Vector2(
            self.logical_width / self.window_width,
            self.logical_height / self.window_height
        )

    @property
    def window_size(self) -> pg.Vector2:
        return pg.Vector2(self.element_tree["Engine"].window.size)

    @property
    def window_width(self) -> int | float:
        return self.window_size.x

    @property
    def window_height(self) -> int | float:
        return self.window_size.y

    @property
    def logical_size(self) -> pg.Vector2:
        return pg.Vector2(self.element_tree["Engine"].window_renderer.logical_size)

    @property
    def logical_width(self) -> int | float:
        return self.logical_size.x

    @property
    def logical_height(self) -> int | float:
        return self.logical_size.y
