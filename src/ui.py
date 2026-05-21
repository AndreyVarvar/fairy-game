from prismane.ui import Button
from prismane.entity import Entity

import pygame as pg

class HeartUI(Entity):
    def __init__(self, pos: pg.Vector2, idx: int) -> None:
        super().__init__()
        self.z = 10
        self.image = pg.transform.scale_by(self.element_tree["AssetLoader"].get_image("./assets/ui/heart.png"), 2)
        self.pos = pos
        self.idx = idx

    def update(self):
        super().update()
        
        if self.element_tree["CurrentStage"].singletons["player"].health <= self.idx:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)


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


