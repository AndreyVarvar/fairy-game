from prismane.ui import Button

import pygame as pg

class FButton(Button):
    def __init__(self, pos: tuple[int, int], image: pg.Surface, z=1, pos_anchor: str = "center"):
        """
        pos: tuple[int, int]. Position of the image.
        image: pygame.Surface. Static image that will be drawn.
        pos_anchor: str, default="center", anchor of the rect to which the `pos` will be applied. Any type of anchor supported by pygame.Rect is allowed (such as 'topleft', 'midbottom')
        """
        rect = image.get_rect()
        rect.__setattr__(pos_anchor, pos)
        super().__init__(rect, z)
        self.image = image


