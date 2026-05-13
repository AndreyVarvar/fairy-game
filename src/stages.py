from prismane import Stage
from prismane.assets import get_image
from pathlib import Path
from prismane.settings import WINDOW_SIZE, WINDOW_WIDTH
from prismane import Event
from prismane.effects import Fade
from prismane.misc import Background
from prismane.camera import Camera

from .ui import FButton
from .player import Player
from .level import Level1

import pygame as pg



class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()

        start_button = FButton(pos=(WINDOW_WIDTH//2, 200), image=get_image(Path("assets/ui/start_button.png")), z=1)
        rules_button = FButton(pos=(WINDOW_WIDTH//2, 500), image=get_image(Path("assets/ui/rules_button.png")), z=1)

        print(start_button.pos)

        self.populate_group("ui", 
                            start_button,
                            rules_button,
                            Background(get_image(Path("assets/backgrounds/title.png")))
                            )

        self.populate_events(
            Event(action=lambda: self.transition(), condition=lambda: start_button.pressed, activations_limit=1)
        )

    def update(self):
        super().update()

        pg.display.set_caption(str(self.element_tree["TimeControlPanel"].fps()))

    def transition(self):
        fadeout_image = pg.Surface(WINDOW_SIZE, pg.SRCALPHA)
        fadeout_image.fill((0, 0, 0))

        fadeout = Fade(2, fadeout_image, f=lambda x: 1 - (1-x)**2)
        fadeout.z = 2

        self.add_to_group("ui", fadeout)
        self.add_event(Event(action=lambda: self.queue_next_stage("game"), condition=lambda: fadeout.done))

    def draw(self):
        super().draw()
        window = self.element_tree["Engine"].window
        display = self.element_tree["Engine"].display
        display.image.fill("black")
        window.fill("black")
        self.element_tree["Renderer"].draw({"display": display.image})


class GameStage(Stage):
    def __init__(self):
        super().__init__()

        self.camera = Camera("MainCamura", 0, 0, 0, 0)
        
        self.populate_group("player", Player(pg.Vector2(-200, -500)))
        self.populate_group("entities",
                            Background(get_image(Path("assets/backgrounds/pink.png"))),
                            )

        self.camera.target = self.groups["player"][0]
        
        self.populate_group("level", Level1())


    def draw(self):
        super().draw()
        super().clear()
        display = self.element_tree["Engine"].display
        self.element_tree["Renderer"].draw({"display": display.image})

    def update(self):
        super().update()
        self.camera.follow_target()
