import pygame as pg
import pygame._sdl2.video as sdl2

from .element import Element

# I swear this wasn't stolen
class Renderer(Element):
    def __init__(self) -> None:
        super().__init__(singleton=True)
        self.queue: list = []

        self.order: int = 0

    def clear(self):
        self.order = 0
        self.queue = []

    def queue_draw(self, surface: pg.Surface, z: int, destination: pg.Rect):
        """
        surface: pygame.Surface. The image to be drawn.
        z: int. z-index of the object. Lower values increase the draw priority
        Used by objects to "queue" themselves into the drawing queue, after which they will be drawn alongside every other element
        """

        self.queue.append([z, self.order, surface, destination])
        self.order += 1

    def draw(self, targets: dict[str, sdl2.Renderer]):
        """
        targets: dict[str, pygame.Surface]. A dictonary with keys being the target name and the surface (target meaning where to draw)
        Draws everything queued so far. Should be called once per frame.
        """
        self.order = 0
        self.queue.sort(key = lambda x:x[0])
        for sprite in self.queue:
            sprite[2].draw(dstrect=sprite[3])
            # target.blit(sprite[2], sprite[3])
