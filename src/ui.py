from prismane.ui import Button
from prismane.entity import Entity
from prismane.renderer import Renderer

import pygame as pg
import pygame._sdl2.video as sdl2

from pathlib import Path

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

class InventoryUI(Entity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__()
        self.z = 10
        self.image = self.element_tree["AssetLoader"].get_image("./assets/ui/inventory.png")
        self.pos = pos
        self.size = pg.Vector2(self.image.get_rect().size)
        self.scale = 1
        self.alpha = 0

    def draw(self):
        renderer: Renderer = self.element_tree["Renderer"]
        maximum = 0
        for i in range(self.element_tree["CurrentStage"].singletons["level"].singletons["player"].butterflies_collected):
            maximum = i + 1
            dst = pg.FRect(self.pos.x + 130 * i + 50, self.pos.y + 50, 170, 179)
            renderer.queue_draw(
                texture=self.element_tree["AssetLoader"].get_image("./assets/entities/butterfly.png"),
                z=11,
                source=None,
                destination=dst,
                flip_x=False,
                flip_y=False,
                angle=0,
                pivot=pg.Vector2(),
                color=pg.Color(255, 255, 255),
                alpha=self.alpha,
                blend_mode=self.blend_mode
            )

        for i in range(maximum, maximum + self.element_tree["CurrentStage"].singletons["level"].singletons["player"].books_collected):
            dst = pg.FRect(self.pos.x + 130 * i + 50, self.pos.y + 130, 97, 70)
            renderer.queue_draw(
                texture=self.element_tree["AssetLoader"].get_image("./assets/objects/book.png"),
                z=11,
                source=None,
                destination=dst,
                flip_x=False,
                flip_y=False,
                angle=0,
                pivot=pg.Vector2(),
                color=pg.Color(255, 255, 255),
                alpha=self.alpha,
                blend_mode=self.blend_mode
            )

        super().draw()


class FButton(Button):
    def __init__(self, pos: pg.Vector2, image: sdl2.Texture, z=1, pos_anchor: str = "center"):
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

        self.click_sound = self.element_tree["AssetLoader"].get_sound(Path("./assets/sfx/novoe-soobschenie--myagkiy-ping.ogg"))

    def update(self):
        super().update()

        if self.pressed:
            self.element_tree["SoundControlPanel"].queue_sound(self.click_sound, 0)


