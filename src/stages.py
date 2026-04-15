from prismane import Stage
from prismane.panels import TimeControlPanel
from prismane.ui import Button
from prismane.assets import get_image

import pygame as pg
from pathlib import Path


class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()

        self.transition_timer_id = None
        self.transition_effect = pg.Surface(self.element_tree["Engine"].screen_size, pg.SRCALPHA)
        self.transition_time = 1  # second

        self.time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]

        self.populate_group("ui", 
                            Button(
                                pg.Rect(100, 100, 100, 100), 
                                z=1, 
                                on_press=lambda: self.__setattr__("transition_timer_id", self.time_panel.queue_timer(self.transition_time)), 
                                image=get_image(Path("assets/ui/start_button.png"))
                            )
        )

    def update(self):
        super().update()


        if self.transition_timer_id is not None:
            remaining_time = self.time_panel.check_timer(self.transition_timer_id)
            if remaining_time == 0.0:
                self.queue_next_stage("game")
            else:
                self.transition_effect.fill((0, 0, 0, int(255 - 255 * remaining_time // self.transition_time)))

    def draw(self):
        super().draw()
        self.element_tree["Renderer"].queue_draw(self.transition_effect, 1, "window", (0, 0))

class GameStage(Stage):
    def __init__(self):
        super().__init__()
        pass

    def draw(self):
        super().draw()


