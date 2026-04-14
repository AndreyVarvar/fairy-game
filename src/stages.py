from prismane import Stage
from prismane.ui import Button

import pygame as pg


class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()
        self.populate_group("ui", Button(pg.Rect(100, 100, 100, 100), 1, lambda: self.queue_next_scene("game")))


class GameStage(Stage):
    def __init__(self):
        super().__init__()
        pass
