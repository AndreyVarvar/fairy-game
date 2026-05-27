from prismane import Stage
from prismane.assets import AssetLoader
from pathlib import Path
from prismane import Event
from prismane.effects import Fade
from prismane.settings import Settings

from .ui import FButton, HeartUI
from .levels import Level1
from .background import Background

import pygame as pg



class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()

        settings: Settings = self.element_tree["Settings"]
        asset_loader: AssetLoader = self.element_tree["AssetLoader"]

        start_button = FButton(pos=(settings.logical_width//2, 200), image=asset_loader.get_image(Path("assets/ui/start_button.png")), z=1)
        rules_button = FButton(pos=(settings.logical_width//2, 500), image=asset_loader.get_image(Path("assets/ui/rules_button.png")), z=1)

        self.populate_group("ui", 
                            start_button,
                            rules_button,
                            Background(asset_loader.get_image(Path("./assets/backgrounds/title.png")))
                            )

        self.populate_events(
            Event(action=lambda: self.transition(), condition=lambda: start_button.pressed, activations_limit=1)
        )

    def update(self):
        super().update()

        pg.display.set_caption(str(self.element_tree["TimeControlPanel"].fps()))

    def transition(self):
        fadeout_image = pg.Surface(self.element_tree["Settings"].window_size, pg.SRCALPHA)
        fadeout_image.fill((0, 0, 0))
        fadeout_image = self.element_tree["AssetLoader"].texture_from_surface(fadeout_image)

        fadeout = Fade(2, fadeout_image, f=lambda x: 1 - (1-x)**2)
        fadeout.z = 2

        self.add_to_group("ui", fadeout)
        self.add_event(Event(action=lambda: self.queue_next_stage("game"), condition=lambda: fadeout.done))



class GameStage(Stage):
    def __init__(self):
        super().__init__()

        self.add_singleton("level", Level1())

        self.populate_group("hearts", *[HeartUI(pg.Vector2(20 + 200*i, 20), idx=i) for i in range(self.singletons["level"].singletons["player"].max_health)])


