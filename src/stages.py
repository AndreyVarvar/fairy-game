from prismane import Stage
from prismane.assets import get_image
from pathlib import Path
from prismane.settings import WINDOW_SIZE, WINDOW_WIDTH
from prismane import Event
from prismane.effects import Fade
from prismane.misc import Background

from .ui import FButton

import pygame as pg



class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()

        start_button = FButton(pos=(WINDOW_WIDTH//2, 200), image=get_image(Path("assets/ui/start_button.png")), z=1)
        rules_button = FButton(pos=(WINDOW_WIDTH//2, 500), image=get_image(Path("assets/ui/rules_button.png")), z=1)

        self.populate_group("ui", 
                            start_button,
                            rules_button,
                            Background(get_image(Path("assets/backgrounds/title.png")))
                            )

        self.populate_events(
            Event(action=lambda: self.transition(), condition=lambda: start_button.pressed, activations_limit=1)
        )

    def transition(self):
        fadeout_image = pg.Surface(WINDOW_SIZE, pg.SRCALPHA)
        fadeout_image.fill((0, 0, 0))

        fadeout = Fade(2, fadeout_image, f=lambda x: x*x)
        fadeout.z = 2

        self.add_to_group("ui", fadeout)
        self.add_event(Event(action=lambda: self.queue_next_stage("game"), condition=lambda: fadeout.done))

    def draw(self):
        super().draw()

        display = self.element_tree["Engine"].display
        display.fill("black")

        self.element_tree["Renderer"].draw({"display": display})

class GameStage(Stage):
    def __init__(self):
        super().__init__()
        pass

    def draw(self):
        super().draw()
        display = self.element_tree["Engine"].display
        display.fill("blue")
