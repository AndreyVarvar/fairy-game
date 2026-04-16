from prismane import Stage
from prismane.assets import get_image
from pathlib import Path
from prismane.settings import WINDOW_SIZE, WINDOW_WIDTH
from prismane import Event
from prismane.effects import Fade

from .ui import FButton

import pygame as pg



class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()

        start_button = FButton(pos=(WINDOW_WIDTH//2, 200), image=get_image(Path("assets/ui/start_button.png")), z=1)
        

        self.populate_group("ui", start_button)

        self.populate_events(
            Event(action=lambda: self.transition(), condition=lambda: start_button.pressed, activations_limit=1)
        )

    def transition(self):
        fadeout_image = pg.Surface(WINDOW_SIZE, pg.SRCALPHA)
        fadeout_image.fill((0, 0, 0))

        fadeout = Fade(2, fadeout_image, f=lambda x: x*x)

        self.add_to_group("ui", fadeout)
        self.add_event(Event(action=lambda: self.queue_next_stage("game"), condition=lambda: fadeout.done))

    def draw(self):
        super().draw()
        window = self.element_tree["Engine"].window
        window.fill("white")
        self.element_tree["Renderer"].draw({"window": window})

class GameStage(Stage):
    def __init__(self):
        super().__init__()
        pass

    def draw(self):
        super().draw()
        window = self.element_tree["Engine"].window
        window.fill("blue")
