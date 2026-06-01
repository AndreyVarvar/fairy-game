from os import pardir
from prismane import Stage
from prismane.assets import AssetLoader
from pathlib import Path
from prismane import Event
from prismane.effects import Fade
from prismane.settings import Settings

from .ui import FButton, HeartUI, InventoryUI
from .levels import Level1, Level2
from .background import Background

import pygame as pg



class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()

        settings: Settings = self.element_tree["Settings"]
        asset_loader: AssetLoader = self.element_tree["AssetLoader"]

        start_button = FButton(pos=pg.Vector2(settings.logical_width//2, 200), image=asset_loader.get_image(Path("assets/ui/start_button.png")), z=1)
        rules_button = FButton(pos=pg.Vector2(settings.logical_width//2, 600), image=asset_loader.get_image(Path("assets/ui/rules_button.png")), z=1)

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

        music = "./assets/sfx/FAIRY_GAME.ogg"
        self.element_tree["MusicControlPanel"].set_music(music)

        settings: Settings = self.element_tree["Settings"]
        asset_loader: AssetLoader = self.element_tree["AssetLoader"]


        self.add_singleton("inventory", InventoryUI(pg.Vector2(settings.logical_width//2 - 656, 456)))

        # UI shinanigans
        inventory_button = FButton(pos=pg.Vector2(settings.logical_width - 186, 180), image=asset_loader.get_image(Path("assets/ui/inventory_icon.png")), z=100)
        settings_button = FButton(pos=pg.Vector2(settings.logical_width - 186, 366), image=asset_loader.get_image(Path("assets/ui/settings_icon.png")), z=100)
        self.populate_group("ui", *[inventory_button, settings_button])

        self.populate_events(
            Event(action=lambda: setattr(self.singletons["inventory"], "alpha", 255 if self.singletons["inventory"].alpha == 0 else 0), condition=lambda: inventory_button.pressed, activations_limit=-1) # -1 so that we have infinite activations
        )

        self.populate_group("hearts", *[HeartUI(pg.Vector2(20 + 200*i, 20), idx=i) for i in range(self.singletons["level"].singletons["player"].max_health)])

    def update(self):
        super().update()

        if pg.K_n in self.element_tree["InputControlPanel"].keys_just_pressed:
            self.next_level(2)

    def delete_fade_effect(self):
        del self.singletons["fade"]

    def transition(self, level):
        self.singletons["level"] = level

        pitch_black = pg.Surface(self.element_tree["Settings"].logical_size, pg.SRCALPHA)
        pitch_black.fill("black")
        pitch_black = self.element_tree["AssetLoader"].texture_from_surface(pitch_black)
        transition_effect = Fade(1, pitch_black, lambda x: 1-x)

        self.singletons["fade"] = transition_effect
        self.events.append(
            Event(action=lambda: self.delete_fade_effect(), condition=lambda: transition_effect.done, activations_limit=1)
        )


    def next_level(self, n):
        self.singletons["level"].destroy()

        if n == 1:
            next_level = Level1()
        elif n == 2:
            next_level = Level2()
        elif n == 3:
            raise NotImplementedError
        else:
            raise Exception("THERE ARE ONLY 3 LEVELS")

        pitch_black = pg.Surface(self.element_tree["Settings"].logical_size, pg.SRCALPHA)
        pitch_black.fill("black")
        pitch_black = self.element_tree["AssetLoader"].texture_from_surface(pitch_black)
        transition_effect = Fade(1, pitch_black)

        self.singletons["fade"] = transition_effect

        self.events.append(
            Event(action=lambda: self.transition(next_level), condition=lambda: transition_effect.done, activations_limit=1)
        )

