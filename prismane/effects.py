from .entity import Entity
from .panels import TimeControlPanel

import pygame as pg
import pygame._sdl2.video as sdl2
from collections.abc import Callable

class Fade(Entity):  # can be fadein, fadeout, or whatever else you want. That depends on the function f you pass in
    def __init__(self, duration: int | float, image: sdl2.Texture, f: Callable = lambda x: pg.math.clamp(x, 0, 1)) -> None:
        """
        duration: int | float. How many seconds does the Fade last.
        image: pygame.Surface. What image to fade.
        f: Callable. Default=lambda x: x. Function used to determine how the fade is done. Fadein is lambda x: x and Fadeout is lambda x: 1-x. 
        You can create whatever you want with this
        """
        super().__init__()
        self.image = image
        self.image.alpha = 0
 
        self.size = self.element_tree["Settings"].window_size

        self.duration = duration

        self.time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]
        self.timer_id = self.time_panel.queue_timer(duration)

        self.f = f
        self.done = False

        self.z = 10

    def reset(self):
        self.timer_id = self.time_panel.queue_timer(self.duration)

    def update(self):
        super().update()
        percentage = self.time_panel.check_timer_completion(self.timer_id)
        self.done = (percentage == 1.0)
        
        if not self.done:
            self.image.alpha = int(255 * self.f(percentage))
