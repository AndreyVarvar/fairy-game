from prismane import Stage
from prismane.ui import Button
from prismane.assets import get_image
from prismane import Display

import pygame as pg
from pathlib import Path


class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()
        self.populate_group("ui", 
                            Button(pg.Rect(100, 100, 100, 100), z=1, on_press=lambda: self.queue_next_scene("game"), image=get_image(Path("assets/ui/start_button.png")))
        )
        self.populate_group("window", 
                            Display()
        )

class GameStage(Stage):
    def __init__(self):
        super().__init__()
        pass
