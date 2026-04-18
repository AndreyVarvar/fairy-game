from .entity import Entity
from .settings import WINDOW_HEIGHT, WINDOW_SIZE, WINDOW_WIDTH

import pygame as pg

class Background(Entity):
    def __init__(self, image: pg.Surface, mode: str = "stretch", offset: pg.Vector2 = pg.Vector2(0, 0)):
        """
        image: pygame.Surface. Image that will be used for the background.
        mode: str. Default='stretch'. Is used to determine how the image will be handled.
            - stretch: if the image is not of the same size as the display, scale it to fit. The offset parameter is ignored for this one.
            - tile: if the image is smaller that the display, it will be tiled to fill in the gaps.
            - none: draw the image at (0, 0) untouched
        """
        super().__init__()

        self.offset = offset
        self.mode = mode

        self.reference = image
        self.image = pg.Surface(WINDOW_SIZE, pg.SRCALPHA)
        
        self.z = 0  # push it back

        if self.mode == "stretch":
            self.image = pg.transform.scale(self.reference, WINDOW_SIZE)
        
        self.prev_offset = offset

    def update(self):
        if self.prev_offset != self.offset and self.mode != "stretch":
            self.prev_offset = self.offset

            if self.mode == "tile":
                w, h = self.reference.get_size()
                for x in range(0, WINDOW_WIDTH, w):
                    for y in range(0, WINDOW_HEIGHT, h):
                        self.image.blit(self.reference, (self.offset.x + x, self.offset.y + y))
            elif self.mode == "none":
                self.image.blit(self.reference, self.offset)


