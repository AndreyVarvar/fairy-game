from prismane import Entity
from prismane.settings import Settings

import pygame as pg

# FIXME: make compatible with Display class
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

        settings: Settings = self.element_tree["Settings"]

        self.offset = offset
        self.mode = mode

        # self.reference = image
        
        self.z = 0  # push it back

        # if self.mode == "stretch":
        #     self.image = pg.transform.scale(self.reference, settings.window_size)
        
        self.image = image
        self.size = settings.window_size

        # self.prev_offset = offset

    # def update(self):
    #     if self.prev_offset != self.offset and self.mode != "stretch":
    #         self.prev_offset = self.offset
    #
    #         if self.mode == "tile":
    #             settings: Settings = self.element_tree["Settings"]
    #             w, h = self.reference.get_size()
    #             for x in range(0, settings.window_width, w):
    #                 for y in range(0, settings.window_height, h):
    #                     self.image.blit(self.reference, (self.offset.x + x, self.offset.y + y))
    #         elif self.mode == "none":
    #             self.image.blit(self.reference, self.offset)

