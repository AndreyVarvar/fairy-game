from prismane import Stage
from prismane import Entity
from prismane.ui import Button
from prismane.assets import get_image
from prismane.settings import DISPLAY_SIZE

import pygame as pg
from pathlib import Path


# for special effects if you want
def ease_in_quart(x) -> float:
    return pg.math.clamp(x * x * x * x, 0, 1)


class FadeOut(Entity):
    def __init__(self, time) -> None:
        super().__init__(singleton=False)
        self.image = pg.Surface(self.element_tree["Engine"].screen_size)
        self.image.fill((0, 255, 0, 255))
        self.end_time = time * 1000 # Time in seconds
        self.start_time = pg.time.get_ticks()
        self.opacity = 0
        self.z = 10000000000

    def update(self):
        self.image.set_alpha(self.opacity)
        self.opacity = int(pg.math.remap(0, self.end_time, 0, 255, min(pg.time.get_ticks() - self.start_time, self.end_time)))


class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()
        self.populate_group("ui",
                            Button(
                                pg.Rect(100, 100, 100, 100),
                                z=1,
                                on_press=lambda: (
                                    self.groups["ui"].add(FadeOut(4)),
                                    self.element_tree["GameControlPanel"].register_timed_event(4, lambda: self.queue_next_scene("game"))
                                                  ),
                                image=get_image(Path("assets/ui/start_button.png"))
                                   )
        )

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
