from prismane import Stage
from .ui import StartButton

import pygame as pg


class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()
        self.populate_group("ui", StartButton(pg.Rect(100, 100, 100, 100), 1))



