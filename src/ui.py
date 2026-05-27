from prismane.ui import Button
from prismane.entity import Entity

import pygame as pg
import pygame._sdl2.video as sdl2

class HeartUI(Entity):
    def __init__(self, pos: pg.Vector2, idx: int) -> None:
        super().__init__()
        self.z = 10
        self.image = self.element_tree["AssetLoader"].get_image("./assets/ui/heart.png")
        self.pos = pos
        self.idx = idx
        self.size = pg.Vector2(self.image.get_rect().size)
        self.scale = 2

    def draw(self):
        if self.element_tree["CurrentStage"].singletons["level"].singletons["player"].health <= self.idx:
            self.alpha = 100
        else:
            self.alpha = 255
        
        super().draw()


class FButton(Button):
    def __init__(self, pos: tuple[int, int], image: sdl2.Texture, z=1, pos_anchor: str = "center"):
        """
        pos: tuple[int, int]. Position of the image.
        image: pygame.Surface. Static image that will be drawn.
        pos_anchor: str, default="center", anchor of the rect to which the `pos` will be applied. Any type of anchor supported by pygame.Rect is allowed (such as 'topleft', 'midbottom')
        """
        rect = image.get_rect()
        rect.__setattr__(pos_anchor, pos)
        super().__init__(rect, z)
        self.image = image
        self.size = pg.Vector2(rect.size)


