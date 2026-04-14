from prismane.ui import Button

import pygame as pg


class StartButton(Button):
    def __init__(self, rect: pg.Rect, z=1):
        super().__init__(rect, z)

